import csv
import sys, os


csvfile = sys.argv[1]


def get_tags(text):
    if text:
        text = text.split()
        for word in text:
            if word.startswith('#'):
                word = word.strip('#')
                yield word


def norm_tags(csvfile):
    with open(csvfile, 'r') as fin, open('tags'+csvfile, 'w') as fout:
        reader = csv.reader(fin, lineterminator='\n')

        writer = csv.writer(fout, lineterminator='\n')

        read = list(reader)
        titles = read[0]

        owner_id = int(titles.index('owner.id'))
        timestamp = int(titles.index('taken_at_timestamp'))
        loc_id = int(titles.index('location.id'))
        desc_id = int(titles.index('insta_description'))

        titles_new = [titles[owner_id], titles[timestamp], titles[loc_id], titles[desc_id]]
        writer.writerow(titles_new)

        for row in read:
            # loc = row[location]
            description = row[desc_id]
            tags = set(get_tags(description))

            for tag in tags:
                row_new = [row[owner_id], row[timestamp].replace(',', ''), row[loc_id], tag]
                writer.writerow(row_new)


norm_tags(csvfile)
