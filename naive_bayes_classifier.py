import os
import csv

os.chdir('data')

train_file = "subject lines.train"
test_file = "subject lines.test"

print("Spam Detector by L Kilborn")
print()
print(f"Training file: {train_file}")
print(f"Testing file: {test_file}")
print()

print("Tallying word usage ...", end='')

# a count of how many subject lines are spam and how many total
spam_subjects = 0
total_subjects = 0

# a count of how many words the subject lines use and a total
spam_words = 0
total_words = 0

# a tally of all words and how often they are used in the format [total, spam]
words = {}

# increases the words tally
def tally_word(word, is_spam):
    global words
    global spam_words
    global total_words
    if word in words:
        words[word][0] += 1
        if is_spam:
            words[word][1] += 1
    else:
        words[word] = [1, 0]
        if is_spam:
            words[word][1] = 1
    total_words += 1
    if is_spam:
        spam_words += 1

# takes in a subject line and returns the words in it
def get_words(subject: str):
    subject = subject.lower()
    split_tokens = subject.split() # empty deliminator defaults to any whitespace
    return split_tokens

lines_file = open('subject lines.train', encoding='utf8')
lines_reader = csv.reader(lines_file, delimiter='\t', quotechar='\"')

for line in lines_reader:
    # line is in format [is_spam, subject]
    is_spam = int(line[0]) == 1
    total_subjects += 1
    if is_spam:
        spam_subjects += 1
    for word in get_words(line[1]):
        tally_word(word, is_spam)

lines_file.close()

print(" done")
print(f"{spam_subjects} subject lines are spam out of {total_subjects} total")
print(f"{len(words)} words were collected")
