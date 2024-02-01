import os
import csv

os.chdir('../data/')

probabilities = {}

probabilities_list = open("words_frequency.csv", newline="\n")
probabilities_reader = csv.reader(probabilities_list, delimiter=",", quotechar="\"")
probabilities_reader.__next__() # skip header

for prob in probabilities_reader:
    probabilities[prob[1]] = float(prob[0])

probabilities_list.close()

# takes in a subject line and returns the words in it
def get_words(subject: str):
    subject = subject.lower()
    split_tokens = subject.split() # empty deliminator defaults to any whitespace
    alpha_tokens = list(filter(lambda x: x.isalpha(), split_tokens))
    return alpha_tokens

# predicts the result of a subject line
def predict(subject: str):
    words = get_words(subject)
    result = 1
    for word in words:
        result *= probabilities[word]
    return result * len(words)

subjects = open("subject lines.train", newline="\n")
subjects_reader = csv.reader(subjects, delimiter="\t", quotechar="\"")

output = open("predictions.train", mode ="w", newline="\n")
output_writer = csv.writer(output, delimiter=",", quotechar="\"")
output_writer.writerow(["spam", "pred", "subject"])

for subject in subjects_reader:
    output_writer.writerow([subject[0], predict(subject[1]), subject[1]])

output.close()
