import os
import csv
from training import *

os.chdir("..\\data")

train_file_path = "subject_lines.train"
test_file_path = "subject_lines.test"
prediction_output_path = "predictions.csv"

# takes in a subject line and returns the words in it
def get_words(subject: str):
    return subject.lower().split()

def raw_training_data():
    lines_file = open(train_file_path, encoding="utf8")
    return csv.reader(lines_file, delimiter="\t")

def training_data():
    proc_line = lambda line: (line[0] == "1", get_words(line[1]))
    return map(proc_line, raw_training_data())

print("Spam Detector by L Kilborn")
print()
print(f"Training file: {train_file_path}")
print(f"Testing file: {test_file_path}")
print(f"Predictions file: {prediction_output_path}")
print()
print("Tallying word usage ...", end="")

tally = process_data(training_data())
subject_line_counts = tally[0]

print(" done")
print(f"{tally[0][1]} subject lines are spam out of {sum(tally[0])}")
print(f"{len(tally[3])} words were collected")
print()
print("Computing word probabilities ...", end="")

probs = calc_word_probs(*tally)

print(" done")