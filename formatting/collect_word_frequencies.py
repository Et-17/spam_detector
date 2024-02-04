import os
import csv
import json

os.chdir('../data/')

# a count of how many subject lines are spam and how many total
spam_subjects = 0
total_subjects = 0

# a count of how many words the subject lines use a word
spam_words = 0
total_words = 0

# a tally of all words and how often they are used in [total, spam]
words = {}

# increases the words tally
def tally_word(word, spam):
    global words
    global spam_words
    global total_words
    if word in words:
        words[word][0] += 1
        if spam:
            words[word][1] += 1
    else:
        words[word] = [1, 0]
        if spam:
            words[word][1] = 1
    total_words += 1
    if spam:
        spam_words += 1

# takes in a subject line and returns the words in it
def get_words(subject: str):
    subject = subject.lower()
    split_tokens = subject.split() # empty deliminator defaults to any whitespace
    alpha_tokens = list(filter(lambda x: x.isalpha(), split_tokens))#
    return split_tokens

print("Tallying words ...", end="")

lines_file = open('subject lines.train', encoding='utf8')
lines_reader = csv.reader(lines_file, delimiter='\t', quotechar='\"')

for line in lines_reader:
    try:
        is_spam = int(line[0]) == 1
        total_subjects += 1
        if is_spam:
            spam_subjects += 1
        for word in get_words(line[1]):
            tally_word(word, is_spam)
    except:
        print(f"fail on line \"{line}\"")
        

lines_file.close()

print(" done")
print("Storing word frequencies ...", end="")

with open('words_tally.csv', 'w', newline='\n', encoding='utf8') as tally_file:
    tally_writer = csv.writer(tally_file, delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)
    tally_writer.writerow(["total_usage", "spam_usage",  "word"])
    for word in words:
        tally_writer.writerow([words[word][0], words[word][1], word])

print(" done")
print("Storing extra data ...", end="")

with open("extra_data.json", "w") as extra_data_file:
    json.dump({
        "total_subjects": total_subjects,
        "spam_subjects": spam_subjects,
        "word_count": len(words.keys()),
        "spam_words_total": spam_words,
        "total_words_total": total_words
    }, extra_data_file)

print(" done")
