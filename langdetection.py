import csv, os, sys
from langdetect import detect, detect_langs
from langdetect import DetectorFactory
import emoji
DetectorFactory.seed = 0
csvfile = sys.argv[1]
# reg = re.compile('[^a-zA-Z ]')

def extract_emojis(str):
  return ''.join(c for c in str if c not in emoji.UNICODE_EMOJI)


def add_language(csvfile):

    with open(csvfile, 'r') as fin, open('new_'+csvfile, 'w') as fout:
        reader = csv.reader(fin, lineterminator='\n')

        writer = csv.writer(fout, lineterminator='\n')

        incl_col = 19


        writer.writerow(next(reader) + ['languages'])
        counter = 0
        bad_text = 0
        for row in reader:
            de_row = extract_emojis(row[incl_col])

            if len(de_row) > 0:
                try:
                    list_of_langs = detect_langs(de_row)
                    # print(len(list_of_langs))
                    l = list_of_langs[0]
                    if l.lang == 'en' and l.prob > 0.9:
                        row.append(list_of_langs)
                        counter += 1
                        writer.writerow(row)
                except:
                    print(de_row, 'Something wrong:', row[incl_col])
                    bad_text += 1
                
                    # col.append(list(row[incl_col]))
        print('Good english labels: ', counter)
        print('Bad labels: ', bad_text)


add_language(csvfile)
