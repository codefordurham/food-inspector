#!/usr/bin/env python
import sys
import csv
import requests
import pprint
import json

LIMIT = 100

def main():
    premises = []
    path = sys.argv[1]
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for index, row in enumerate(reader):
            if row['Transitional Type Desc'] == 'FOOD':
                premise = {'name': row['Premise Name'].title(),
                           'address': row['Premise Address1'].title()}
                premises.append(premise)
            if index == LIMIT:
                break
    print json.dumps(premises, indent=4)


if __name__ == '__main__':
    main()
