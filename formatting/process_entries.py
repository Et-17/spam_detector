import os
import csv

os.chdir('../data/')

words = []

with open('words_tally.csv') as tally_file:
    tally_reader = csv.reader(tally_file, delimiter=',', quotechar='\"')
    for row in tally_reader:
        words.append(row[1])

# takes in a subject line and returns the words in it
def get_words(subject: str):
    subject = subject.lower()
    split_tokens = subject.split() # empty deliminator defaults to any whitespace
    alpha_tokens = list(filter(lambda x: x.isalpha(), split_tokens))
    return alpha_tokens

subjects = open("subject lines.train")
subjects_reader = csv.reader(subjects, delimiter='\t', quotechar="\"")
output = open("subject lines words.csv", "w")

output.write("is_spam," + ",".join(words) + "\n")

for row in subjects_reader:
    output.write(row[0] + ",")
    words_usage = map(lambda word: str(row[1].count(word)), words)
    output.write(",".join(words_usage) + "\n")

subjects.close()
output.close()
