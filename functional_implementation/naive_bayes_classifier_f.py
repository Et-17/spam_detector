import os
import csv
import random
from functools import reduce
from collections import defaultdict

os.chdir("data")

train_file_path = "subject_lines.train"
test_file_path = "subject_lines.test"
prediction_output_path = "predictions.csv"

print("Spam Detector by L Kilborn")
print()
print(f"Training file: {train_file_path}")
print(f"Testing file: {test_file_path}")
print(f"Predictions file: {prediction_output_path}")
print()

print("Tallying word usage ...", end="")

def raw_training_data():
    lines_file = open(train_file_path, encoding="utf8")
    return csv.reader(lines_file, delimiter="\t")

# students: i don't know if they covered yield in the python classes
# essentially, yielding returns a value and then continues execution
# allowing you to "iterate over" the function like a list
def training_data():
    proc_line = lambda line: (line[0] == "1", line[1])
    return map(proc_line, raw_training_data())
    # for line in raw_training_data():
    #     is_spam = line[0] == "1"
    #     yield is_spam, line[1]

# takes in a subject line and returns the words in it
def get_words(subject: str):
    return subject.lower().split()

# this takes in a ham count and a spam count, and increments one of them
# depending on the bool inc_spam
def increase_ht_tally(inc_spam: bool, ham: int, spam: int, amount = 1) -> tuple[float, float]:
    if inc_spam:
        return ham, spam + amount
    else:
        return ham + amount, spam

def tally_unique_word(word, is_spam, unique_word_counts, word_counts):
    if word_counts[word][int(is_spam)] == 0: #int(is_spam) returns 1 for spam, 0 for ham
        return increase_ht_tally(is_spam, *unique_word_counts)
    else:
        return unique_word_counts

# this just updates the word_counts count. it's essentially a functional
# wrapper for dict's imperative api
def tally_word(word, is_spam, word_counts):
    word_counts.update([(
        word,
        increase_ht_tally(is_spam, *word_counts[word])
    )])
    return word_counts

# returns a tuple of (new unique_word_counts, new word_counts)
def process_word(word, is_spam, unique_word_counts, word_counts):
    return tally_unique_word(word, is_spam, unique_word_counts, word_counts), \
           tally_word(word, is_spam, word_counts)

# this will add a new subject line to a running tally
# note: word_counts is expected to be a defaultdict with a
# default_factory that returns (0, 0)
def process_subject(line_words, is_spam, subject_line_counts, total_word_counts, unique_word_counts, word_counts):
    process_word_acc = lambda tallies, word: process_word(word, is_spam, *tallies)
    new_unique_counts, new_word_counts = reduce(process_word_acc, line_words, (unique_word_counts, word_counts))
    return increase_ht_tally(is_spam, *subject_line_counts), \
           increase_ht_tally(is_spam, *total_word_counts, amount = len(line_words)), \
           new_unique_counts, \
           new_word_counts

# this will tally up everything given by the data iterator, which can be any
# iterator but will most likely be a list or a generator
def process_data(data_iter):
    initial_val = ((0, 0), (0, 0), (0, 0), defaultdict(lambda: (0, 0)))
    proc_acc = lambda tally, line: process_subject(
        get_words(line[1]),
        line[0],
        *tally
    )
    return reduce(proc_acc, data_iter, initial_val)

