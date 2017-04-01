# michigan-uni-sports-scrapper

A simple scrapper for Michigan University sport teams results

Used for assignment 4 of "Applied Plotting, Charting & Data Representation in Python" course:
https://www.coursera.org/learn/python-plotting/

### Requirements

Also see requirements.txt

- Python 3.5+ (tested with Python 3.5 and 3.6)
- pandas
- pyparsing
- requests

### Usage

```
usage: scrape.py [-h] [-o OUT_FILE] discipline_code

positional arguments:
  discipline_code       Discipline code, e.g. `m-baskbl', `m-basebl' etc.

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_FILE, --out-file OUT_FILE
                        Path to write the result CSV file. Defaults to
                        `<discipline_code>_<current_datetime>.csv'
```