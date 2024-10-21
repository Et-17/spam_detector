from functools import reduce

# adds a new subject line to the confusion matrix
def evaluate_subject(subject, classification_function, tp, tn, fp, fn):
    a = subject[0]
    p = classification_function(subject[1])
    return tp + (1 if     a and     p else 0), \
           tn + (1 if not a and not p else 0), \
           fp + (1 if not a and     p else 0), \
           fn + (1 if     a and not p else 0)

# returns a tupple of (true pos, true neg, false pos, false neg)
# classification_function is a single argument function that takes in
# a list of tokens and returns a boolean of whether or not it is spam
def evaluate(data_iter, classification_function):
    eval_acc = lambda matrix, subject: evaluate_subject(subject, classification_function, *matrix)
    return reduce(eval_acc, data_iter, (0, 0, 0, 0))

def precision(tp, tn, fp, fn):
    return float(tp) / float(tp + fp)

def recall(tp, tn, fp, fn):
    return float(tp) / float(tp + fn)

def f1(tp, tn, fp, fn):
    return (2 * tp) / (2 * tp + fp + fn)
    