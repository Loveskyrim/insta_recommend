import csv, os, sys
from langdetect import detect, detect_langs
from langdetect import DetectorFactory
import re
import emoji
DetectorFactory.seed = 0
csvfile = sys.argv[1]
# reg = re.compile('[^a-zA-Z ]')

def extract_emojis(str):
  return ''.join(c for c in str if c not in emoji.UNICODE_EMOJI)

# def remove_emoji(string):
#     emoji_pattern = re.compile("["
#                            u"\U0001F600-\U0001F64F"  # emoticons
#                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
#                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                            u"\U00002702-\U000027B0"
#                            u"\U000024C2-\U0001F251"
#                            u"\U0001f926-\U0001f937"
#                            u"\u200d"
#                            u"\u2640-\u2642" 
#                            "]+", flags=re.UNICODE)
#     return emoji_pattern.sub(r'', string)

def deSign(inputString):
    return inputString.encode('utf-8', 'ignore').decode('utf-8')
    # return reg.sub('', inputString)

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
                    print(len(list_of_langs))
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
