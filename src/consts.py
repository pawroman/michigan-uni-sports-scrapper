import re

import pyparsing


# Seasons available for scrapping
EARLIEST_SEASON = 2007
LATEST_SEASON = 2016

# URLs
BASE_SCHEDULE_URL = "http://www.mgoblue.com/sports/{code}/sched/data/mich-{code}-sched-{year}.html"
BASE_XML_DATA_URL = "http://www.mgoblue.com/data/xml/events/{code}/{year}/{event_id}.xml"

# The Michigan team uses this team code
MICHIGAN_TEAM_CODE = "mich"

# Maps outcode "code" to human-readable string
OUTCOMES = {
    "L": "Lost",
    "W": "Won"
}

# Regex used to extract scores from outcome_score data, e.g. "L, 20-10"
SCORE_RE = re.compile("(?P<score1>\d+)\s*-\s*(?P<score2>\d+)")

# pyparsing definitions for parsing schedule data
TR_START, TR_END = pyparsing.makeHTMLTags("tr")
TR_EVENT_LISTING = TR_START().setParseAction(pyparsing.withClass("event-listing"))

TR_EVENT_LISTING_EXPR = TR_EVENT_LISTING + pyparsing.SkipTo(TR_END)("tr_content") + TR_END
