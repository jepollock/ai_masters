#!/usr/bin/env python3
import os
import argparse

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

ACTIVATION_FUNCTIONS = ['identity', 'logistic', 'tanh', 'relu']

MAX_EPOCH = 800
HIDDEN_LAYER_SIZES = [(100,), (5,2), (10,5), (16,8), (20,10), (20,10,5), (5,10)]
# 3 - 94%.
# 40 - 95%
LEARNING_RATE = 0.01
# https://xkcd.com/221/ - 4 is overused, as is 42
RANDOM_SEED = 221

RING_SYN_TRAIN_CSV = "data/RingSynTrain.csv"
RING_SYN_TEST_CSV = "data/RingSynTest.csv"

enable_debug = False

def debug(string):
    if (enable_debug):
        print(string)

def toXy(df):
    X = df.drop(columns="Class")
    y = df.drop(columns=["feature1", "feature2"])
    return X, y

def report(string):
    print(string)

class Table:
    def header(self, *fields):
        self.doc = "|"
        for field in fields:
            self.doc += f" {field} |"
        self.doc += "\n"
        self.doc += "|"
        for field in fields:
            self.doc += " --- |"
        self.doc += "\n"
        return self

    def __init__(self):
        self.doc = ""

    def row(self, *values):
        self.doc += "|"
        for value in values:
            self.doc += f" {value} |"
        self.doc += "\n"
        return self

    def report(self):
        report(self.doc)

def start_table():
    table = Table()
    table.header("Activation Function", "Epoch", "Sizes", "Accuracy")
    return table

parser = argparse.ArgumentParser(description="Multi-layer Perceptron")
parser.add_argument("--enable_debug", action='store_true')
parser.add_argument("--max_epoch", type=int, default=MAX_EPOCH)

args = parser.parse_args()
enable_debug=args.enable_debug
max_epoch = args.max_epoch
# Data format:
# feature1, feature2, class
# x* => float
# class -> {0,1}
training_pd = None
test_pd = None
if os.path.exists(RING_SYN_TRAIN_CSV) and os.path.exists(RING_SYN_TEST_CSV):
    print("Loading datasets...")
    training_pd = pd.read_csv(RING_SYN_TRAIN_CSV)
    test_pd = pd.read_csv(RING_SYN_TEST_CSV)
    # example_pd = pd.read_csv("example.csv")

# assert that the data was loaded.
debug(training_pd)
debug(test_pd)

# Fix python keyword collision
def fixClass(df):
    df["Class"] = df["class"]
    df.drop(columns="class", inplace=True)

fixClass(training_pd)
fixClass(test_pd)

(X_train, y_train) = toXy(training_pd)
(X_test, y_test) = toXy(test_pd)
debug(f"y_train shape: {y_train.shape}")

table = start_table()
for sizes in HIDDEN_LAYER_SIZES:
    for activation_function in ACTIVATION_FUNCTIONS:
        debug(f"ACTIVATION: {activation_function}")
        clf = MLPClassifier(hidden_layer_sizes=sizes,
                            learning_rate_init=LEARNING_RATE,
                            max_iter=max_epoch,
                            activation=activation_function,
                            solver='adam',
                            random_state=RANDOM_SEED)
        clf.fit(X_train, y_train.Class)
        y_pred = clf.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        table.row(activation_function, max_epoch, sizes, f"{accuracy:.3f}")

table.report()