import sys

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




