#!/usr/bin/env python3
"""Creates various plots from the serialized DataFrame made in scrape.py."""
import pickle

frame = pickle.load(open("frame.p", "rb"))
investors = {}
for index, row in frame.iterrows():
    vestors = row["Select Investors"]
    for investor in vestors:
        if investor not in investors:
            investors[investor] = 0
        investors[investor] += 1
    
print(investors)
print(investors["Accel Partners"])
print(max(investors, key=lambda x: investors[x]))
