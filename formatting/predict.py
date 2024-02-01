import os
import csv
import json
import random

os.chdir('../data/')

# pull the extra data
extra_data = json.load(open("extra_data.json"))
spam_prob = float(extra_data["spam_subjects"]) / float(extra_data["total_subjects"])
ham_prob = 1.0 - spam_prob

# stores the probabilities in the format [spam_prob, ham_prob]
probabilities = {}

probabilities_list = open("word_probs.csv", newline="\n")
probabilities_reader = csv.reader(probabilities_list, delimiter=",", quotechar="\"")
probabilities_reader.__next__() # skip header

for prob in probabilities_reader:
    probabilities[prob[2]] = [float(prob[0]), float(prob[1])]

probabilities_list.close()

# takes in a subject line and returns the words in it
def get_words(subject: str):
    subject = subject.lower()
    split_tokens = subject.split() # empty deliminator defaults to any whitespace
    alpha_tokens = list(filter(lambda x: x.isalpha(), split_tokens))
    return alpha_tokens

# calculate the confidence that a subject is spam
def calc_spam_conf(words):
    result = 1
    for word in words:
        result *= probabilities[word][0]
    return result * spam_prob

# calculate the confidence that a subject is ham
def calc_ham_conf(words):
    result = 1
    for word in words:
        result *= probabilities[word][1]
    return result * ham_prob

# pick a choice
def pick_classification(spam_conf, ham_conf):
    if spam_conf > ham_conf:
        return 1
    elif ham_conf > spam_conf:
        return 0
    else: # if the probabilities are equal, then we make a random selection based on the overal probs
        return int(random.random() > spam_prob)

# predicts the result of a subject line
def predict(subject: str):
    words = get_words(subject)
    spam_conf = calc_spam_conf(words)
    ham_conf = calc_ham_conf(words)
    return pick_classification(spam_conf, ham_conf)

subjects = open("subject lines.train", newline="\n")
subjects_reader = csv.reader(subjects, delimiter="\t", quotechar="\"")

output = open("predictions.train", mode ="w", newline="\n")
output_writer = csv.writer(output, delimiter=",", quotechar="\"")
output_writer.writerow(["spam", "pred", "subject"])

for subject in subjects_reader:
    output_writer.writerow([subject[0], predict(subject[1]), subject[1]])

output.close()
