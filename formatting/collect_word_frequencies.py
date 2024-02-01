import os
import csv

os.chdir('../data/')

# a tally of all wods and how often they are used in [total, spam]
words = {}

# increases the words tally
def tally_word(word, spam):
    global words
    if word in words:
        words[word][0] += 1
        if spam == 1:
            words[word][1] += 1
    else:
        words[word] = [1, 0]
        if spam == 1:
            words[word][1] = 1
        else:
            words[word][0] = 0

# takes in a subject line and returns the words in it
def get_words(subject: str):
    subject = subject.lower()
    split_tokens = subject.split() # empty deliminator defaults to any whitespace
    alpha_tokens = list(filter(lambda x: x.isalpha(), split_tokens))
    return alpha_tokens

print("Tallying words ...", end="")

lines_file = open('subject lines.train')
lines_reader = csv.reader(lines_file, delimiter='\t', quotechar='\"')

for line in lines_reader:
    for word in get_words(line[1]):
        tally_word(word, int(line[0]))

lines_file.close()

print(" done")
print("Storing ...", end="")

with open('words_tally.csv', 'w', newline='\n') as tally_file:
    tally_writer = csv.writer(tally_file, delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)
    tally_writer.writerow(["total_usage", "spam_usage",  "word"])
    for word in words:
        tally_writer.writerow([words[word][0], words[word][1], word])

print(" done")
