"""Plot hiveplot graph."""
import collections
import math
import random
import sys

import networkx as nx
from pyveplot import Axis, Hiveplot, Node


def main(filename, alter_position, nb_axis):
    """Catch main function."""
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

    # make as many axes as requested

    radius = len(g.nodes())
    margin = 100
    center = (radius + margin, radius + margin)
    delta = float((math.pi * 2) / nb_axis)
    angle = 0

    if alter_position is 0:
        fname = 'hiveplot' + str(nb_axis) + 'axes.svg'
    else:
        fname = 'hiveplot' + str(nb_axis) + 'axesAlteredPositions.svg'

    h = Hiveplot(fname)
    h.axes = []

    print("Computing axes")
    for i in range(nb_axis):
        x = radius + margin + math.cos(angle) * radius
        y = radius + margin - math.sin(angle) * radius
        end = (x, y)
        axis = Axis(center,  # start
                    end,   # end
                    stroke="black",
                    stroke_width=0.05)
        angle += delta
        h.axes.append(axis)

    c = 0
    nbtot = 0
    for x in stats:
        nbtot += x * stats[x]

    print("Computing nodes")
    for n in g.nodes():
        nd = Node(n)
        deg = degrees[n]
        # use cumulated pop
        index = math.ceil((c / nbtot) * nb_axis) - 1
        c += deg
        a = h.axes[int(index)]
        if alter_position is 0:
            node_pos = random.random()
        elif stats[deg] > 1:
            node_pos = random.random() * (math.sqrt(deg / max_degree))
        else:
            node_pos = math.sqrt(deg / max_degree)
        a.add_node(nd, node_pos)
        red = str(int(255 / deg))
        green = str(abs(int(math.cos(deg) * 255)))
        blue = str(abs(int(math.sin(deg) * 255)))
        color = "rgb(" + red + ", " + green + ", " + blue + ")"

        # alter node drawing after adding it to axis to keep coordinates
        nd.dwg = nd.dwg.circle(center=(nd.x, nd.y),
                               r=deg / 3 + 2,
                               fill=color,
                               fill_opacity=0.6,
                               stroke=random.choice(
                                   ['red', 'crimson', 'coral', 'purple']),
                               stroke_width=0.1)

    print("Computing edges")
    opacity = 1
    angle = 45
    # edges from h.axes[0] to h.axes[1]
    for e in g.edges():
        color = random.choice(
            ['blue', 'red', 'purple', 'green', 'magenta', 'cyan', 'crimson'])
        node0 = e[0]
        node1 = e[1]
        axis0 = axis1 = h.axes[0]
        for axe in h.axes:
            if node0 in axe.nodes:
                axis0 = axe
            if node1 in axe.nodes:
                axis1 = axe
        angle0 = (axis0.angle() if axis0.angle() >= 0
                  else axis0.angle() + 2 * math.pi)
        angle1 = axis1.angle()

        cond = (len(h.axes) - 2) * delta and angle0 - angle1 > 0
        if axis0 == axis1:
            dest_angle0 = angle
            dest_angle1 = angle

        # don't why you have to compute like that but this is the only way
        # to have edges ploted properly.
        elif angle0 - angle1 <= cond:
            dest_angle0 = -angle
            dest_angle1 = angle
        else:
            dest_angle0 = angle
            dest_angle1 = -angle

        h.connect(axis0,
                  node0,
                  # angle of invisible axis for source control points
                  dest_angle0,
                  axis1,
                  node1,
                  # angle of invisible axis for target control points
                  dest_angle1,
                  stroke_width=0.1,  # pass any SVG attributes to an edge
                  stroke_opacity=opacity,
                  stroke=color,
                  )
    print("Writing svg")
    h.save()
    print("Wrote file as ", fname)


if __name__ == '__main__':
    filename = sys.argv[1]

    if len(sys.argv) > 2:
        alter_position = int(sys.argv[2])
    else:
        alter_position = 0

    if len(sys.argv) > 3:
        nb_axis = int(sys.argv[3])
    else:
        nb_axis = 3

    main(filename, alter_position, nb_axis)
