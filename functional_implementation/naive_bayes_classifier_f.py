import os
import csv
from training import process_data, calc_word_probs, classify
from functools import partial
from evaluation import evaluate, precision, recall, f1

os.chdir("..\\data")

train_file_path = "subject_lines.train"
test_file_path = "subject_lines.test"
prediction_output_path = "predictions.csv"

# takes in a subject line and returns the words in it
def get_words(subject: str):
    return subject.lower().split()

def raw_data(path):
    lines_file = open(path, encoding="utf8")
    return csv.reader(lines_file, delimiter="\t")

def read_data(path):
    proc_line = lambda line: (line[0] == "1", get_words(line[1]))
    return map(proc_line, raw_data(path))

print("Spam Detector by L Kilborn")
print()
print(f"Training file: {train_file_path}")
print(f"Testing file: {test_file_path}")
print(f"Predictions file: {prediction_output_path}")
print()
print("Tallying word usage ...", end="")

tally = process_data(read_data(train_file_path))
subject_line_counts = tally[0]

print(" done")
print(f"{tally[0][1]} subject lines are spam out of {sum(tally[0])}")
print(f"{len(tally[3])} words were collected")
print()
print("Computing word probabilities ...", end="")

probs = calc_word_probs(*tally)

print(" done")
print("Evaluating performance ...", end="")

classification_function = partial(classify, subject_line_counts, *probs)
confusion_matrix = evaluate(read_data(test_file_path), classification_function)

print(" done")
print()
print(f"True Positives: {confusion_matrix[0]}")
print(f"True Negatives: {confusion_matrix[1]}")
print(f"False Positives: {confusion_matrix[2]}")
print(f"False Negatives: {confusion_matrix[3]}")
print()
print(f"Precision: {precision(*confusion_matrix)}")
print(f"Recall: {recall(*confusion_matrix)}")
print(f"F1: {f1(*confusion_matrix)}")