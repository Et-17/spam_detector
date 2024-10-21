from functools import reduce
from collections import defaultdict

# takes in a ham count and a spam count, and increments one of them
# depending on the bool inc_spam
def increase_ht_tally(inc_spam: bool, ham: int, spam: int, amount = 1) -> tuple[float, float]:
    if inc_spam:
        return ham, spam + amount
    else:
        return ham + amount, spam

# updates the unique words tally 
def tally_unique_word(word, is_spam, unique_word_counts, word_counts):
    if word_counts[word][int(is_spam)] == 0: #int(is_spam) returns 1 for spam, 0 for ham
        return increase_ht_tally(is_spam, *unique_word_counts)
    else:
        return unique_word_counts

# this just updates the word_counts count. it's essentially a functional
# wrapper for dict's imperative api
def tally_word(word, is_spam, word_counts):
    word_counts.update([(
        word,
        increase_ht_tally(is_spam, *word_counts[word])
    )])
    return word_counts

# returns a tuple of (new unique_word_counts, new word_counts)
def process_word(word, is_spam, unique_word_counts, word_counts):
    return tally_unique_word(word, is_spam, unique_word_counts, word_counts), \
           tally_word(word, is_spam, word_counts)

# adds a new subject line to a running tally
# note: word_counts is expected to be a defaultdict with a
# default_factory that returns (0, 0)
def process_subject(line_words, is_spam, subject_line_counts, total_word_counts, unique_word_counts, word_counts):
    process_word_acc = lambda tallies, word: process_word(word, is_spam, *tallies)
    new_unique_counts, new_word_counts = reduce(process_word_acc, line_words, (unique_word_counts, word_counts))
    return increase_ht_tally(is_spam, *subject_line_counts), \
           increase_ht_tally(is_spam, *total_word_counts, amount = len(line_words)), \
           new_unique_counts, \
           new_word_counts

# tallies up everything given by the data iterator, which can be any
# iterator but will most likely be a list or a generator
# expects data in the form of (is spam, list of tokens)
def process_data(data_iter):
    initial_val = ((0, 0), (0, 0), (0, 0), defaultdict(lambda: (0, 0)))
    proc_acc = lambda tally, line: process_subject(
        line[1],
        line[0],
        *tally
    )
    return reduce(proc_acc, data_iter, initial_val)

def calc_probs(total_word_counts, unique_word_counts, ham_count, spam_count):
    ham_prob = (ham_count + 1) / (total_word_counts[0] + unique_word_counts[0])
    spam_prob = (spam_count + 1) / (total_word_counts[1] + unique_word_counts[1])
    return ham_prob, spam_prob

# returns a tuple of ((unknown_ham, unknown_spam), {word: (ham, spam)})
# the initial argument is a discard so that you can pass the output of 
# process_data into this function
def calc_word_probs(_, total_word_counts, unique_word_counts, word_counts):
    return calc_probs(total_word_counts, unique_word_counts, 0,0), \
           {word: calc_probs(total_word_counts, unique_word_counts, *word_counts[word]) \
            for word in word_counts}

# calculates the probabilities of an entire subject line
def calc_subject_probs(tokens, subject_line_counts, unknown_token_probs, word_probs):
    tuple_mul = lambda a, b: (a[0] * b[0], a[1] * b[1])
    get_prob = lambda word: word_probs[word] if word in word_probs else unknown_token_probs
    base = reduce(lambda a, b: tuple_mul(a, get_prob(b)), tokens, (1, 1))
    prior = (
        subject_line_counts[0] / sum(subject_line_counts),
        subject_line_counts[1] / sum(subject_line_counts)
    )
    return tuple_mul(base, prior)

# picks a choice between two probabilities
def pick_classification(ham_prob, spam_prob):
    return spam_prob > ham_prob

# classifies a subject line given as a list of tokens
def classify(subject, subject_line_counts, unknown_token_probs, word_probs):
    return pick_classification(*calc_subject_probs(subject, subject_line_counts, unknown_token_probs, word_probs))