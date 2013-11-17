#!/usr/bin/env python
import sys
import csv
import requests
import pprint
import json


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
    print json.dumps(premises, indent=4)


if __name__ == '__main__':
    main()
