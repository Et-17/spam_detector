import os
import csv
import json

os.chdir('../data/')

# get extra word data
extra_data = json.load(open("extra_data.json"))
spam_subjects = extra_data["spam_subjects"]
total_subjects = extra_data["total_subjects"]
word_count = extra_data["word_count"] + 1 # +1 for the dummy
spam_total_count = extra_data["spam_words_total"]
total_total_count = extra_data["total_words_total"]

# prepare files
words_file = open("words_tally.csv", newline="\n")
words_reader = csv.reader(words_file, delimiter=",", quotechar="\"")
words_reader.__next__() # skip the header

output_file = open("word_probs.csv", "w", newline="\n")
output_writer = csv.writer(output_file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
output_writer.writerow(["spam_prob", "ham_prob", "word"])

def calc_spam_freq(spam_count):
    return spam_count / spam_total_count

def calc_ham_freq(total_count, spam_count):
    return (total_count - spam_count) / (total_total_count - spam_total_count)

for word in words_reader:
    output_writer.writerow([str(calc_spam_freq(float(word[1]))), str(calc_ham_freq(float(word[0]), float(word[1]))), word[2]])

words_file.close()
output_file.close()