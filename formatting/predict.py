import os
import csv
import json
import random

os.chdir('../data/')

false_positives = 0
false_negatives = 0
true_positives = 0
true_negatives = 0

# pull the extra data
extra_data = json.load(open("extra_data.json"))
spam_prob = float(extra_data["spam_subjects"]) / float(extra_data["total_subjects"])
ham_prob = 1.0 - spam_prob

# stores the probabilities in the format [spam_prob, ham_prob]
probabilities = {}

probabilities_list = open("word_probs.csv", newline="\n", encoding='utf8')
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
        try:
            result *= probabilities[word][0]
        except:
            pass
    return result * spam_prob

# calculate the confidence that a subject is ham
def calc_ham_conf(words):
    result = 1
    for word in words:
        try:
            result *= probabilities[word][1]
        except:
            pass
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

# adds up to the false/true pos/neg counters
def tally(actual, guess):
    global true_positives
    global true_negatives
    global false_negatives
    global false_positives
    if actual == 1 and guess == 1:
        #print("true pos")
        true_positives += 1
    elif actual == 0 and guess == 0:
        true_negatives += 1
    elif actual == 1 and guess == 0:
        #print("false neg")
        false_negatives += 1
    elif actual == 0 and guess == 1:
        #print("false pos")
        false_positives += 1

subjects = open("subject lines.test",newline="\n", encoding='utf8')
subjects_reader = csv.reader(subjects, delimiter="\t", quotechar="\"")

output = open("predictions.train", mode ="w", newline="\n", encoding='utf8')
output_writer = csv.writer(output, delimiter=",", quotechar="\"")
output_writer.writerow(["spam", "pred", "subject"])

for subject in subjects_reader:
    actual = int(subject[0])
    guess = int(predict(subject[1]))
    tally(actual, guess)
    output_writer.writerow([actual, guess, subject[1]])

output.close()

print(f"True Positives: {true_positives}")
print(f"True Negatives: {true_negatives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")
print()
print(f"Precision: {float(true_positives) / float(true_positives + false_positives)}")
print(f"Recall: {float(true_positives) / float(true_positives + false_negatives)}")
