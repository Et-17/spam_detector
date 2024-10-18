import os
import csv
import random
import give_an_example

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

# a count of how many subject lines are spam and how many are ham
spam_subjects = 0
ham_subjects = 0

# a count of how many words the subject lines use
spam_words = 0
ham_words = 0

# a count of how many unique words there are
spam_unique_words = 0
ham_unique_words = 0

# a tally of all words and how often they are used, in the format [ham, spam]
words = {}

# increased the words tally
def increase_tally(word, is_spam):
    global words
    global spam_words
    global ham_words
    global total_words
    global spam_unique_words
    global ham_unique_words

    if not word in words:
        words[word] = [0, 0]
    if is_spam:
        if words[word][1] == 0:
            spam_unique_words += 1
        words[word][1] += 1
        spam_words += 1
    else:
        if words[word][0] == 0:
            ham_unique_words += 1
        words[word][0] += 1
        ham_words += 1

# takes in a subject line and returns the words in it
def get_words(subject: str):
    subject = subject.lower()
    split_tokens = subject.split() # empty deliminator defaults to any whitespace
    return split_tokens

def tally_words():
    global spam_subjects
    global ham_subjects

    lines_file = open(train_file_path, encoding="utf8")
    lines_reader = csv.reader(lines_file, delimiter="\t")

    for line in lines_reader:
        # line is in format [is_spam, subject]
        is_spam = line[0] == "1"
        if is_spam:
            spam_subjects += 1
        else:
            ham_subjects += 1
        for word in get_words(line[1]):
            increase_tally(word, is_spam)
    
    lines_file.close()

tally_words()
print(" done")
print(f"{spam_subjects} subject lines are spam out of {spam_subjects + ham_subjects} total")
print(f"{len(words)} words were collected")
print()

print("Computing word probabilities ...", end="")

def calc_probs(ham_count: int, spam_count: int):
    spam_prob = (spam_count + 1) / (spam_words + spam_unique_words)
    ham_prob = (ham_count + 1) / (ham_words + ham_unique_words)
    return ham_prob, spam_prob

# the probs that will be used for unknown tokens
unknown_word_probs = calc_probs(0, 0)

# this holds the computed word probabilities in the format [ham_prob, spam_prob]
word_probs = {word: calc_probs(words[word][0], words[word][1]) for word in words}

print(" done")
print()

# What follows is the code for classification

spam_prob = float(spam_subjects) / float(spam_subjects + ham_subjects)
ham_prob = float(ham_subjects) / float(spam_subjects + ham_subjects)

# calculate the probability that a subject is spam
def calc_spam_prob(subject_line_words):
    prob = 1
    for word in subject_line_words:
        if not word in word_probs:
            prob *= unknown_word_probs[1]
        else:
            prob *= word_probs[word][1]
    return prob * spam_prob

# calculate the probability that a subject is ham
def calc_ham_prob(subject_line_words):
    prob = 1
    for word in subject_line_words:
        if not word in word_probs:
            prob *= unknown_word_probs[0]
        else:
            prob *= word_probs[word][0]
    return prob * ham_prob

# pick a choice
def pick_classification(ham_conf, spam_conf):
    if spam_conf > ham_conf:
        return True
    else:
        return False

# classifies a subject line
def classify(subject: str):
    subject_line_words = get_words(subject)
    spam_conf = calc_spam_prob(subject_line_words)
    ham_conf = calc_ham_prob(subject_line_words)
    return pick_classification(ham_conf, spam_conf)

print("Evaluating performance ...", end="")

# a tally of how many test subjects there are so that we can select one for the example
test_subjects = 0

false_positives = 0
false_negatives = 0
true_positives = 0
true_negatives = 0

test_file = open(test_file_path, newline="\n", encoding="utf8")
test_reader = csv.reader(test_file, delimiter="\t", quotechar="\"")

output = open(prediction_output_path, mode="w", newline="\n", encoding="utf8")
output_writer = csv.writer(output, delimiter="\t")
output_writer.writerow(["spam", "pred", "subject"])

for test in test_reader:
    actual = test[0] == "1"
    guess = classify(test[1])
    if actual == True and guess == True:
        true_positives += 1
    elif actual == True and guess == False:
        false_negatives += 1
    elif actual == False and guess == True:
        false_positives += 1
    elif actual == False and guess == False:
        true_negatives += 1
    test_subjects += 1
    output_writer.writerow([int(actual), int(guess), test[1]])

test_file.close()
output.close()

print(" done")
print(f"{true_positives + false_negatives} subject lines are spam and {true_negatives + false_positives} are ham")
print()
print(f"True Positives: {true_positives}")
print(f"True Negatives: {true_negatives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")
print()
print(f"Precision: {float(true_positives) / float(true_positives + false_positives)}")
print(f"Recall: {float(true_positives) / float(true_positives + false_negatives)}")
print(f"F1: {(2 * true_positives) / (2 * true_positives + false_positives + false_negatives)}")
print()

print("Would you like an example? (y/N) ", end="")
answer = input()
while (answer.strip().lower() != "y" and answer.strip().lower() != "n" and answer.strip() != ""):
    print("Please answer either y or n")
    print("Would you like an example? (y/N) ", end="")
    answer = input()
if answer.strip().lower() == "y":
    print()
    give_an_example.show_example(test_file_path, test_subjects, get_words, word_probs, spam_prob, ham_prob, unknown_word_probs[0], unknown_word_probs[1])