import json
import csv
import sys, os

path = sys.argv[1]


def location_tags(path):
    """
    location_tags(csvfile)
    parses location to the columns from csvfile and writes it to the new file
    """
    items = os.listdir(path)
    print(items)
    os.system('mkdir loc')
    for csvfile in items:
        with open(path + '/' + csvfile, 'r') as fin, open('loc/new_'+csvfile, 'w') as fout:
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


location_tags(path)