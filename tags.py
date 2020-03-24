import csv
import sys, os
import emoji

path = sys.argv[1]


def get_tags(text):
    if text:
        text = text.split()
        for word in text:
            if word.count('#') == 1 and word.startswith('#'):
                word = word.strip('#')
                yield word


def norm_tags(path):
    items = os.listdir(path)
    print(items)
    os.system('mkdir tags')
    for csvfile in items:
        with open(path + '/' + csvfile, 'r') as fin, open('tags/tags_'+csvfile, 'w') as fout:
            reader = csv.reader(fin, lineterminator='\n')

            writer = csv.writer(fout, lineterminator='\n')

            read = list(reader)
            titles = read[0]

            owner_id = int(titles.index('owner.id'))
            timestamp = int(titles.index('taken_at_timestamp'))
            loc_id = int(titles.index('location.id'))
            desc_id = int(titles.index('insta_description'))

            titles_new = [titles[owner_id], titles[loc_id], titles[timestamp],
            'hashtag1', 'hashtag2', 'hashtag3', 'hashtag4', 'hashtag5', 'hashtag6',
            'hashtag7', 'hashtag8', 'hashtag9', 'hashtag10']
            writer.writerow(titles_new)

            for row in read[1:]:
                # loc = row[location]
                description = row[desc_id]
                description = ''.join(c for c in description if c not in emoji.UNICODE_EMOJI)
                row_new = [row[owner_id], row[loc_id], row[timestamp].replace(',', '')]
                tags = list(get_tags(description))

                for tag in range(10):
                    if tag < len(tags):
                        row_new.append(tags[tag])
                    else:
                        row_new.append(0)
                writer.writerow(row_new)


norm_tags(path)
