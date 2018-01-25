"""Plot graph stats."""
import collections
import sys

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import networkx as nx


def plotStats(stats):
    """Plot the graph from stats."""
    line_width = 1

    font = {'family': 'DejaVu Sans',
            'weight': 'bold',
            'size': 10}

    matplotlib.rc('font', **font)

    plt.figure(1)
    aw = plt.subplot(211)
    aw.set_title("Graph grouping nodes by their number of relationships")

    aw.plot(list(stats.keys()), list(stats.values()), 'r', linewidth=line_width)
    aw.grid(True)

    plt.xlabel('Number of edges')
    plt.ylabel('Number of nodes')
    plt.savefig("edgesStats.pdf",
                dpi=300, format='pdf', papertype='a0')


def main(filename):
    """Catch main function."""
    dotG = nx.drawing.nx_pydot.read_dot(filename)
    nx.write_edgelist(dotG, filename + ".edgelist")
    try:
        fh = open(filename + ".edgelist", 'r')
    except IOError:
        print(filename + ".edgelist not found")
        raise

    g = nx.Graph()

    for line in fh.readlines():
        (head, tail, *c) = line.split()
        g.add_edge(int(head, 16), int(tail, 16))

    min_degree = 1
    max_degree = min_degree
    degrees = {}
    for n in g:
        degrees[n] = nx.degree(g, n)
        max_degree = degrees[n] if degrees[n] > max_degree else max_degree

    values = list(degrees.values())
    stats = {x: values.count(x) for x in values}
    stats = dict(collections.OrderedDict(sorted(stats.items())))

    plotStats(stats)


if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)
