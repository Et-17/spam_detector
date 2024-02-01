import os
import csv

os.chdir('../data/')

# a tally of all wods and how often they are useda
words = {}

# increases the words tally
def tally_word(word):
    global words
    if word in words:
        words[word] += 1
    else:
        words[word] = 1

# takes in a subject line and returns the words in it
def get_words(subject: str):
    subject = subject.lower()
    split_tokens = subject.split() # empty deliminator defaults to any whitespace
    alpha_tokens = list(filter(lambda x: x.isalpha(), split_tokens))
    return alpha_tokens

print("Tallying words ...", end="")

lines_file = open('subject lines.test')

for line in lines_file:
    for word in get_words(line):
        tally_word(word)

lines_file.close()

print(" done")
print("Storing ...", end="")

with open('words_tally.csv', 'w', newline='\n') as tally_file:
    tally_writer = csv.writer(tally_file, delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)
    for word in words:
        tally_writer.writerow([words[word], word])

print(" done")
