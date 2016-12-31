import sys
import random

class Utilities:

    # Splits a graph into its immediate branches
    # Examples:
    # split("XXXX") = ["XXXX"]
    # split("[X,XXX]") = ["X","XXX"]
    @staticmethod
    def split(graph):
        if len(graph) == 0 or graph[0] != "[":
            return [graph]
        graphs = [""]
        depth = 0
        for c in graph[1:-1]:
            if c == "," and depth == 0:
                graphs += [""]
            else:
                graphs[-1] += c
                depth += 1 if c == "[" else -1 if c == "]" else 0
        return graphs

    # Returns a random key using the given weights
    # Data must be inputed as a dictionary, with choices as keys and weights as values.
    @staticmethod
    def randomWeightedChoice(data):
        cumulative = [sum(data.values()[:i+1]) for i in range(len(data.values()))]
        value = random.uniform(0, cumulative[-1])
        index = next(i for i in range(len(cumulative)) if cumulative[i] > value)
        return data.keys()[index]




