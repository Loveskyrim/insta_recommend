import requests
import json
import csv
import sys, os
import numpy as np
csvfile = sys.argv[1]


def location_tags(csvfile):
	"""
	location_tags(csvfile)
	parses location to the columns from csvfile and writes it to the new file
	"""
    with open(csvfile, 'r') as fin, open('new_'+csvfile, 'w') as fout:
        reader = csv.reader(fin, lineterminator='\n')

        writer = csv.writer(fout, lineterminator='\n')

        read = list(reader)
        titles = read[0]

        location = int(titles.index('location'))
        has_public_page = int(titles.index('location.has_public_page'))
        loc_id = int(titles.index('location.id'))
        name = int(titles.index('location.name'))
        slug = int(titles.index('location.slug'))

        writer.writerow(titles)
        for row in read:
            loc = row[location]
            try:
                locate = json.loads(row[location])
            except:
                locate = {}

            if len(locate) > 0:
                row[has_public_page] = locate['has_public_page']
                row[loc_id] = locate['id']
                row[name] = locate['name']
                row[slug] = locate['slug']

                writer.writerow(row)


location_tags(csvfile)