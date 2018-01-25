"""Plot tool."""
import sys
from collections import OrderedDict

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import toml


def plotLog(filename):
    """Plot log file."""
    datas = {}
    with open(filename, 'r', encoding='utf-8') as fp:
        datas.update(toml.load(fp))

    datas = OrderedDict(sorted(datas.items(), key=lambda t: float(t[0])))

    keys = list()
    to_be_explored_pages = list()
    explored_pages = list()
    to_be_explored_images = list()
    explored_images = list()
    duration = list()

    for key, val in datas.items():
        keys.append(float(key))
        to_be_explored_pages.append(val.get('To_be_explored_pages'))
        explored_pages.append(val.get('Explored_pages'))
        to_be_explored_images.append(val.get('Images_to_be_explored'))
        explored_images.append(val.get('Explored_images'))
        duration.append(val.get('Duration'))

    line_width = 0.05

    font = {'family': 'DejaVu Sans',
            'weight': 'bold',
            'size': 3}

    matplotlib.rc('font', **font)

    plt.figure(1)
    aw = plt.subplot(211)

    aw.plot(keys, duration, 'r', linewidth=line_width)
    aw.grid(True)

    plt.xlabel('Time elapsed [s]')
    plt.ylabel('Crawl round duration[s]')

    ax = plt.subplot(212)

    ax.plot(keys, to_be_explored_pages, 'b',
            linewidth=line_width, label='to_be_explored_pages')
    ax.plot(keys, explored_pages, 'g',
            linewidth=line_width, label='explored_pages')
    ax.plot(keys, to_be_explored_images, 'r',
            linewidth=line_width, label='to_be_explored_images')
    ax.plot(keys, explored_images, 'y',
            linewidth=line_width, label='explored_images')

    ax.legend()

    plt.xlabel('Time elapsed [s]')
    plt.ylabel('Number of pages')
    ax.grid(True)

    # plt.show()
    plt.savefig(filename + "-crawlingStats.pdf",
                dpi=300, format='pdf', papertype='a0')


if __name__ == "__main__":

    filename = sys.argv[1]
    plotLog(filename)
