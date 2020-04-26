import sys, os
import re
import csv
import emoji

csvfile = "TagsMerged.csv"


def get_tags(text, tag=True):
    if text:
        text = text.split()
        temp_text = []
        temp_tags = set()
        for word in text:
            count = word.count('#')
            if count == 1: temp_tags.add(word)
            elif count > 1:
                temp_word = set(word.strip('#').split('#'))
                temp_tags.union(temp_word)
            elif count == 0:
                temp_text.append(word)
        
        if tag == False:
            for word in temp_text:
                yield word
        else:
            for word in temp_tags:
                yield word


def norm_tags(csvfile):
    with open(csvfile, 'r', encoding="cp1251") as fin, open('tags'+csvfile, 'w') as fout:
        reader = csv.reader(fin, lineterminator='\n')

        writer = csv.writer(fout, lineterminator='\n')

        read = list(reader)
        titles = read[0]
        # print(titles)
        owner_id = int(titles.index('owner.id'))
        timestamp = int(titles.index('taken_at_timestamp'))
        loc_id = int(titles.index('location.id'))
        desc_id = int(titles.index('insta_description'))
        # print(owner_id, timestamp, loc_id, desc_id)
        titles_new = [titles[owner_id], titles[loc_id], titles[timestamp],
            'hashtag1', 'hashtag2', 'hashtag3', 'hashtag4', 'hashtag5', 'hashtag6',
            'hashtag7', 'hashtag8', 'hashtag9', 'hashtag10']
        writer.writerow(titles_new)

        for row in read[1:]:
            # loc = row[location]
            try:
                description = row[desc_id]
                description = ''.join(c for c in description if c not in emoji.UNICODE_EMOJI)
                description = ''.join(_ for _ in description if _ not in '()<>?!@*')
                tags = list(get_tags(description))
                # print(tags)
            except:
                tags = []
            if len(tags) > 0:
                row_new = []
                try:
                    row_new.append(row[owner_id])
                except:
                    row_new.append(0)
                    # print(row[0])
                try:
                    row_new.append(row[timestamp].replace(',', ''))
                except:
                    row_new.append(0)
                    # print(row[0])
                try:
                    row_new.append(row[loc_id])
                except:
                    row_new.append(0)
                    # print(row[0])
                
                for tag in range(10):
                    if tag < len(tags):
                        row_new.append(tags[tag])
                    else:
                        row_new.append(0)
                        # print(row[0])
                # print(row_new)
                writer.writerow(row_new)

def norm_desc(csvfile):
    with open(csvfile, 'r', encoding="cp1251") as fin, open('description_'+csvfile, 'w') as fout:
        reader = csv.reader(fin, lineterminator='\n')

        writer = csv.writer(fout, lineterminator='\n')

        read = list(reader)
        titles = read[0]
        # print(titles)
        owner_id = int(titles.index('owner.id'))
        timestamp = int(titles.index('taken_at_timestamp'))
        loc_id = int(titles.index('location.id'))
        desc_id = int(titles.index('insta_description'))
        # print(owner_id, timestamp, loc_id, desc_id)
        titles_new = [titles[owner_id], titles[loc_id], titles[timestamp], titles[desc_id]]
        writer.writerow(titles_new)

        for row in read[1:]:
            # loc = row[location]
            try:
                description = row[desc_id]
                description = ''.join(c for c in description if c not in emoji.UNICODE_EMOJI)
                description = ''.join(_ for _ in description if _ not in '()<>?!@*')
                desc_wo_tags = list(get_tags(description, False))
                print(desc_wo_tags)
            except:
                desc_wo_tags = []
            if len(desc_wo_tags) > 0:
                row_new = []
                try:
                    row_new.append(row[owner_id])
                except:
                    row_new.append(0)
                    # print(row[0])
                try:
                    row_new.append(row[timestamp].replace(',', ''))
                except:
                    row_new.append(0)
                    # print(row[0])
                try:
                    row_new.append(row[loc_id])
                except:
                    row_new.append(0)
                    # print(row[0])
                try:
                    row_new.append(' '.join(desc_wo_tags))
                except:
                    row_new.append(0)
                # print(row_new)
                writer.writerow(row_new)

norm_desc(csvfile)
# norm_tags(csvfile)