#re-imports for ide stuff
import os
import csv
import random

digits = 10

# this script will be called from naive_bayes_classifier.py so we don't
# need to move to the data directory

# pick a choice
# 0: spam, 1: spam, 2: tie
def pick_classification(spam_conf, ham_conf):
    if spam_conf < ham_conf:
        return 1
    elif spam_conf > ham_conf:
        return 0
    else: # if the probs are equal, then we make a random selection based on the overal probs
        return 2

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
    longest_word_length = max(len(word) for word in example_words)
    # let's go double formatting
    header_template = f"{{:^{longest_word_length}}}   {{:^{digits+1}}}   {{:^{digits+1}}}"
    table_template = f"{{:<{longest_word_length}}}   {{:<{digits+1}g}}   {{:<{digits+1}g}}"
    print(header_template.format("Word", "Spam", "Ham"))
    subject_spam_prob = 1
    subject_ham_prob = 1
    for word in example_words:
        word_spam_prob = 0
        word_ham_prob = 0
        if word in word_probs.keys():
            word_spam_prob = word_probs[word][0]
            word_ham_prob = word_probs[word][1]
        else:
            word_spam_prob = 1
            word_ham_prob = 1
        print(table_template.format(word, word_spam_prob, word_ham_prob))
        subject_spam_prob *= word_spam_prob
        subject_ham_prob *= word_ham_prob
    subject_spam_prob *= spam_prob
    subject_ham_prob *= ham_prob
    print("-"*(longest_word_length + digits + digits + 6))
    print(table_template.format("Full", spam_prob, ham_prob))
    print(header_template.format("", "↧", "↧"))
    print(table_template.format("Total", subject_spam_prob, subject_ham_prob))
    num_result = pick_classification(subject_spam_prob, subject_ham_prob)
    comp_char = ""
    text_result = ""
    if num_result == 1:
        comp_char = "<"
        text_result = "Ham"
    elif num_result == 0:
        comp_char = ">"
        text_result = "Spam"
    elif num_result == 2:
        comp_char = "="
        text_result = "Tie"
    # move the beginning of the previous row, then move to the calculated absolute horizontal
    # print the comparison char, move to the end, then print the text result
    print(f"\033[1F\033[{longest_word_length + digits + 5}C{comp_char}\033[13C→ {text_result}")

    