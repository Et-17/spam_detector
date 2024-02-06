#re-imports for ide stuff
import os
import csv
import random

# this script will be called from naive_bayes_classifier.py so we don't
# need to move to the data directory

# selected an example and then returns (subject, words)
def select_an_example(test_file_path, total_subject_count, get_word_func):
    selected_subject_num = random.randint(1, total_subject_count - 1)
    test_file = open(test_file_path, encoding='utf8')
    test_file_reader = csv.reader(test_file, delimiter="\t", quotechar="\"")
    example_subject = ""
    for (num, line) in enumerate(test_file_reader):
        if num == selected_subject_num:
            example_subject = line[1]
            break
    return (example_subject, get_word_func(example_subject))

def show_example(test_file_path, total_subject_count, get_word_func, word_probs, spam_prob, ham_prob):
    (example_subject, example_words) = select_an_example(test_file_path, total_subject_count, get_word_func)
    print(f"Subject: {example_subject}")
    print(f"Words: {example_words}")
    print()