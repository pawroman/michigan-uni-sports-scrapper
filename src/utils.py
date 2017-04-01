import xml.etree.ElementTree as ElementTree

import requests
import pandas as pd

import consts


def scrape_michigan_uni_sport_results(discipline_code):
    results = []
    session = requests.Session()

    for season_year in range(consts.EARLIEST_SEASON, consts.LATEST_SEASON + 1):
        schedule_url = consts.BASE_SCHEDULE_URL.format(code=discipline_code, year=season_year)
        print("Scrapping: ", schedule_url)

        resp = session.get(schedule_url)
        resp.raise_for_status()

        html = resp.text

        event_data = scrape_michigan_uni_season(session, html, discipline_code, season_year)
        results.extend(event_data)

        print("Scrapped", len(event_data), "events in season", season_year)

    df = pd.DataFrame(results)
    df["date"] = pd.to_datetime(df["date"])

    return df.set_index("date")


def scrape_michigan_uni_season(session, schedule_html, discipline_code, season_year):
    event_data = []

    for num, tr in enumerate(consts.TR_EVENT_LISTING_EXPR.searchString(schedule_html), start=1):
        event_id = tr.id

        event_url = consts.BASE_XML_DATA_URL.format(code=discipline_code, year=season_year,
                                                    event_id=event_id)

        event_resp = session.get(event_url)
        event_resp.raise_for_status()

        event = ElementTree.fromstring(event_resp.text)

        detail = event.find("detail").attrib

        try:
            home = event.find("home").attrib
        except AttributeError:
            print("ERROR SCRAPPING (no home team data):", event_url)
            continue

        away = event.find("away").attrib
        tournament = event.find("tournament").attrib
        headtohead = event.find("headtohead").attrib

        if home["code"] == consts.MICHIGAN_TEAM_CODE:
            played_at_home = True
            opponent = away["opp"]
        else:
            played_at_home = False
            opponent = home["opp"]

        result, score, opponent_score = parse_outcome_score(event)

        event_data.append({
            "discipline"    : discipline_code,
            "event_id"      : event_id,
            "date"          : detail["date"],
            "season"        : season_year,
            "time"          : detail["time"],
            "day"           : detail["day"],
            "location"      : detail["location"],

            "tournament"    : tournament["flag"] == "yes",
            "headtohead"    : headtohead["flag"] == "yes",
            "opponent"      : opponent,
            "played_at_home": played_at_home,

            "result"        : result,
            "score"         : score,
            "opponent_score": opponent_score,
        })

    return event_data


def parse_outcome_score(event):
    try:
        outcome_score = event.find("outcome_score").attrib
    except AttributeError:
        # Unknown result
        return None, None, None

    try:
        result_code = outcome_score["data"][0]
        result = consts.OUTCOMES[result_code]
    except KeyError:
        # Postponed etc - won't have scores
        result = outcome_score.get("data")
        score = None
        opponent_score = None
    else:
        scores = consts.SCORE_RE.search(outcome_score["data"]).groupdict()

        if result == consts.OUTCOMES["W"]:
            # win
            score = scores["score1"]
            opponent_score = scores["score2"]
        else:
            score = scores["score2"]
            opponent_score = scores["score1"]

    return result, score, opponent_score
