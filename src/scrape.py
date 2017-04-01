#!env python3

import argparse
from datetime import datetime

import utils


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("discipline_code",
                        help="Discipline code, e.g. `m-baskbl', `m-basebl' etc.")
    parser.add_argument("-o", "--out-file", required=False,
                        help="Path to write the result CSV file. "
                             "Defaults to `<discipline_code>_<current_datetime>.csv'")

    args = parser.parse_args()

    if not args.out_file:
        args.out_file = ("{}_{}.csv"
                         .format(args.discipline_code,
                                 datetime.now().replace(microsecond=0))
                         .replace(" ", "_"))

    results_df = utils.scrape_michigan_uni_sport_results(args.discipline_code)

    results_df.to_csv(args.out_file)

    print("Wrote results to:", args.out_file)


if __name__ == "__main__":
    main()
