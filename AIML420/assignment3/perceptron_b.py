#!/usr/bin/env python3

import os
import random

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd


LEARNING_RATE = 0.001
# https://xkcd.com/221/ - 4 is overused, as is 42
RANDOM_SEED = 221
random.seed(a=RANDOM_SEED)

RING_SYN_TRAIN_CSV = "data/RingSynTrain.csv"
RING_SYN_TEST_CSV = "data/RingSynTest.csv"

enable_debug = False
enable_plot = False

def debug(string):
    if (enable_debug):
        print(string)

def report(string):
    print(string)

# Markdown table accumulator
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
    table.header("Model", "Epoch", "Accuracy")
    return table

cluster_colours = ['red', 'green', 'blue', 'orange', 'violet', 'yellow']

# plot the starting cut
def plot(df=None, title=None, filename=None):
    fig = plt.figure(figsize=(10,4))
    ax = fig.add_subplot(projection='3d')
    #cmap="Set1"
    #cmap="tab10"
    cmap=mpl.colors.ListedColormap(cluster_colours)
    norm=mpl.colors.BoundaryNorm(range(0,len(cluster_colours)), cmap.N)
    ax.scatter(df.feature1, df.feature2, c=df.Class, s=20, cmap=cmap, norm=norm)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    if filename is not None:
        print(f"Saving file - {filename}")
        plt.savefig(filename + ".png")
    plt.show()

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

# Fix python keyword collision
def fixClass(df):
    df["Class"] = df["class"]
    df.drop(columns="class", inplace=True)

fixClass(training_pd)
fixClass(test_pd)
# fixClass(example_pd)

# assert that the data was loaded.
debug(training_pd)
debug(test_pd)

if enable_plot:
    plot(test_pd, "test data", "test")
    plot(training_pd, "train data", "train")

# Keep the activation functions separate from the Perceptron.
def threshold(value):
    return 1 if value >= 0 else 0

def update_weight(weight, error, learning_rate, input):
    return weight + learning_rate * error * input

# Perceptron supporting 2 inputs.
class Perceptron:
    def __init__(self, activation_fn, learning_rate):
        self.doc=""
        self.activation_fn = activation_fn
        self.weight_bias = random.uniform(-1,1)
        self.weight_a = random.uniform(-1,1)
        self.weight_b = random.uniform(-1,1)
        self.learning_rate = learning_rate

    def _activation(self, value):
        return self.activation_fn(value)

    def apply(self, a,b):
        return self._activation(-1 * self.weight_bias +
                                a * self.weight_a +
                                b * self.weight_b)

    def learn(self, a, b, y_true, y_pred):
        error = y_true - y_pred
        debug(f"error: {error}")
        debug(f"before: ({self.weight_bias}, {self.weight_a}, {self.weight_b})")
        self.weight_bias = update_weight(self.weight_bias, error, self.learning_rate, -1)
        self.weight_a = update_weight(self.weight_a, error, self.learning_rate, a)
        self.weight_b = update_weight(self.weight_b, error, self.learning_rate, b)
        debug(f"after:  ({self.weight_bias}, {self.weight_a}, {self.weight_b})")

def train(dataset, perceptron, num_epochs):
    for i in range(num_epochs):
        for row in dataset.itertuples():
            y_true = row.Class
            a = row.feature1
            b = row.feature2
            y_pred = perceptron.apply(a, b)
            perceptron.learn(a, b, y_true, y_pred)

def test(dataset, perceptron):
    correct = 0
    for row in dataset.itertuples():
        y_true = row.Class
        y_pred = perceptron.apply(row.feature2, row.feature2)
        if y_true == y_pred:
            correct += 1
    return correct / dataset.shape[0]


print("Perceptron, Non-Linearly Separable")

table = start_table()
perceptron = Perceptron(lambda value: threshold(value), LEARNING_RATE)
total_epochs = 0
# Run a single training pass, stopping at epoch checkpoints and reporting
# test accuracy.
for report_epochs in (1, 5, 10, 15, 20, 50, 60, 80, 100, 120, 150, 200):
    train(training_pd, perceptron, report_epochs - total_epochs)
    test_accuracy = test(test_pd, perceptron)
    total_epochs = report_epochs
    table.row("Non-Separable", report_epochs, test_accuracy)

table.report()