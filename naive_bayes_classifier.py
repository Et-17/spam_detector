import os
import csv
import random
import give_an_example

os.chdir('data')

train_file_path = "subject_lines.train"
test_file_path = "subject_lines.test"
prediction_output_path = "predictions.csv"

print("Spam Detector by L Kilborn")
print()
print(f"Training file: {train_file_path}")
print(f"Testing file: {test_file_path}")
print(f"Predictions file: {prediction_output_path}")
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

lines_file = open(train_file_path, encoding='utf8')
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
print()

print("Computing word probabilities ...", end='')

# this will hold the compute word probabilities in the format [spam_prob, ham_prob]
word_probs = {}

# we need to find not just the overall word usage but the unique words in each
# category for the additive smoothing
spam_unique_words = 0
ham_unique_words = 0

for word in words.keys():
    if words[word][1] > 0:
        spam_unique_words += 1
    if words[word][0] - words[word][1] > 0:
        ham_unique_words += 1

def calc_spam_prob(spam_count: int) -> float:
    return (spam_count + 1) / (spam_words + spam_unique_words)

def calc_ham_prob(total_count: int, spam_count: int) -> float:
    return (total_count - spam_count + 1) / (total_words - spam_words + spam_unique_words)

unknown_word_spam_prob = calc_spam_prob(0)
unknown_word_ham_prob = calc_ham_prob(0, 0)

for word in words.keys():
    spam_prob = calc_spam_prob(words[word][1])
    ham_prob = calc_ham_prob(words[word][0], words[word][1])
    word_probs[word] = [spam_prob, ham_prob]

print(" done")
print()

print("Evaluating performance ...", end='')

# a tally of how many test_subjects there aer so that we can select one for the example
test_subjects = 0

false_positives = 0
false_negatives = 0
true_positives = 0
true_negatives = 0

spam_prob = spam_subjects / total_subjects
ham_prob = 1 - spam_prob

# calculate the confidence that a subject is spam
def calc_spam_conf(words):
    result = 1
    for word in words:
        if not (word in word_probs.keys()): 
            result *= unknown_word_spam_prob
            continue
        result *= word_probs[word][0]
    return result * spam_prob

# calculate the confidence that a subject is ham
def calc_ham_conf(words):
    result = 1
    for word in words:
        if not (word in word_probs.keys()):
            result *= unknown_word_ham_prob
            continue
        result *= word_probs[word][1]
    return result * ham_prob

# pick a choice
def pick_classification(spam_conf, ham_conf):
    if spam_conf > ham_conf:
        return 1
    elif ham_conf > spam_conf:
        return 0
    elif spam_prob > ham_prob: # uh oh the probs are equal, we have to choose the overall prob
        return 1
    elif ham_prob > spam_prob:
        return 0
    else: # the confs are a tie, and the probs are a tie. it's 50/50
        return random.randint(0,1)

# predicts the result of a subject line
def predict(subject: str):
    words = get_words(subject)
    spam_conf = calc_spam_conf(words)
    ham_conf = calc_ham_conf(words)
    return pick_classification(spam_conf, ham_conf)

# adds up to a false/true pos/neg counters
def tally(actual, guess):
    global true_positives
    global true_negatives
    global false_negatives
    global false_positives
    if actual == 1 and guess == 1:
        true_positives += 1
    elif actual == 0 and guess == 0:
        true_negatives += 1
    elif actual == 1 and guess == 0:
        false_negatives += 1
    elif actual == 0 and guess == 1:
        false_positives += 1

test_file = open(test_file_path, newline="\n", encoding="utf8")
test_reader = csv.reader(test_file, delimiter="\t", quotechar="\"")

output = open(prediction_output_path, mode="w", newline="\n", encoding="utf8")
output_writer = csv.writer(output, delimiter=",", quotechar="\"")
output_writer.writerow(["spam", "pred", "subject"])

for test in test_reader:
    actual = int(test[0])
    guess = predict(test[1])
    tally(actual, guess)
    output_writer.writerow([actual, guess, test[1]])
    test_subjects += 1

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

# MESSAGE TO STUDENTS:
# What follows is just the example stuff. It's the exact same as the rest of the
# script but less documented and with tons of text processing in it. Those
# who do not worship Our Lady of Discord will not understand the deep magic, but
# analysis would yield nothing anyway.

answer = input()
while (answer.strip().lower() != 'y' and answer.strip().lower() != 'n' and answer.strip() != ''):
    print("Please answer either y or n")
    print("Would you like an example? (y/N) ")
    answer = input()
if answer.strip().lower() == 'y':
    print()
    give_an_example.show_example(test_file_path, test_subjects, get_words, word_probs, spam_prob, ham_prob, unknown_word_spam_prob, unknown_word_ham_prob)