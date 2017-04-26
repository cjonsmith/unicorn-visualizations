#!/usr/bin/env python3
"""Scrapes webpage for unicorn company data and creates serialized DataFrame."""
import re
import sys
import pickle
import os.path
import requests
import numpy as np
from datetime import date
from pandas import DataFrame
from bs4 import BeautifulSoup

url = "https://www.cbinsights.com/research-unicorn-companies"

# Send get request to website and store its contents.
r = requests.get(url)
c = r.content

# Make a BeautifulSoup DOM parser.
try:
    soup = BeautifulSoup(c, "lxml")
except bs4.FeatureNotFound:
    print("lxml parser not found: install using following command:\n"
          "pip install lxml", file=sys.stderr)
    exit(-1)

# Columns of the DataFrame should be the header of the webpage's table.
table = soup.find("table")
columns = [h.get_text() for h in table.find_all("th")][1:]

# Index of DataFrame should be the name of each company.
# Data should correspond to the associated values between a company and the
# data found at each column.
index = []
data = []
# Regular expression to determine a data field represents a date.
date_object_re = re.compile(
    "^(?P<month>[1-9]|10|11|12)/"
    "(?P<day>[1-9]|1[0-9]|2[0-9]|3[0-1])/"
    "(?P<year>\d{1,4})$")
for row in table.find("tbody").find_all("tr"):
    # Some table rows on the webpage are empty. If one is encountered,
    # continue to the next row.
    try:
        company = row.find("a").get_text().strip()
    except AttributeError:
        continue

    # Some companies (mostly ones with more than one word in their name)
    # have several whitespace characters between words. To combat this, split
    # all companies on whitespace and join them together on a single space to
    # replace multiple instances of whitespace characters with a single space.
    company = " ".join(company.split())
    index.append(company)

    # The first table data element contains the anchor tag that contains the
    # name of the company; we will concern ourselves with everything but the
    # company name since we've already extracted that data.
    row_data = []
    for i, td in enumerate(row.find_all("td")[1:], 1):
        text = td.get_text().strip()
        text = " ".join(text.split())
        # The first table data element contains net worth of the company.
        # Remove the dollar sign and convert it to a float.
        if i == 1:
            net_worth = float(text.lstrip("$"))
            row_data.append(net_worth)
        # The second table data element contains the date the company was
        # founded. Check it's validity against the regular expression and
        # convert it to a datetime.date object.
        elif i == 2:
            match = date_object_re.search(text)
            if match:
                year = int(match.group("year"))
                month = int(match.group("month"))
                day = int(match.group("day"))
                start_date = date(year, month, day)
                row_data.append(start_date)
            else:
                row_data.append(None)
        # The fifth table data element contains a list of investors separated
        # by commas. For fast lookup later, store the investors in a list.
        elif i == 5:
            row_data.append(text.split(","))
        else:
            row_data.append(text)
    data.append(row_data)

# Construct the DataFrame and write it to a binary file.
frame = DataFrame(data, index, columns)
if os.path.isfile("frame.p"):
    delete = input("File named 'frame.p' already found in current directory. "
                   "Delete it? [y/N]: ")
    if delete.lower() != "y":
        print("Operation aborted.")
        exit()
pickle.dump(frame, open("frame.p", "wb"))
