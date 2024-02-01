import os
import csv

os.chdir('../data/')

# find word counts
words_file = open("words_tally.csv", newline="\n")
words_reader = csv.reader(words_file, delimiter=",", quotechar="\"")
words_reader.__next__() # skip header

total_word_count = 0
spam_word_uses = 0
for row in words_reader:
    total_word_count += 1
    spam_word_uses += int(row[1])
total_word_count += 1 # dummy 

# reset for reading
words_file.close()
words_file = open("words_tally.csv", newline="\n")
words_reader = csv.reader(words_file, delimiter=",", quotechar="\"")
words_reader.__next__() # skip header

output_file = open("words_frequency.csv", "w", newline="\n")
output_writer = csv.writer(output_file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
output_writer.writerow(["probability", "word"])

def calc_freq(spam_count):
    return (spam_count + 1) / (spam_word_uses + total_word_count)

for word in words_reader:
    output_writer.writerow([str(calc_freq(int(word[1]))), word[2]])

words_file.close()
output_file.close()
