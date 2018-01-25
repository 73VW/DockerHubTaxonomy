"""Project tools."""
import re
from datetime import datetime

timestamps = []


def filter(regexp, text):
    """Return lines matching regexp in file."""
    lines = text.splitlines()
    prog = re.compile(regexp, re.IGNORECASE)
    for k in [line for line in lines if prog.search(line)]:
        return k


filter("^FROM.+", "FROM scratch\nFROM foo\nFROM bar")


def log_progression(to_be_explored_pages, explored_pages,
                    to_be_explored_images, explored_images, duration, cvt):
    """Log progression."""
    log(to_be_explored_pages, explored_pages, to_be_explored_images,
        explored_images, duration, cvt)


def print_log(to_be_explored_pages, explored_pages, to_be_explored_images,
              explored_images, duration, cvt):
    """Log progression."""
    log = "\n\n[" + str(datetime.now()) + "]\n\t\
    Number of explored pages : {}\n\t\
    Explored pages :\n".format(len(explored_pages))

    # the following is needed to loop over the dict.
    # Why? Because manager dict...
    good_d = dict(explored_pages)
    for page in good_d:
        log += "\t" + page + '\t--\t' + explored_pages[page] + '\n'
    log += "\n\tNumber of pages to be explored: {}\n\
    To be Explored pages :\n".format(len(to_be_explored_pages))

    good_d = dict(to_be_explored_pages)
    for page in good_d:
        log += "\t" + page + '\t--\t' + to_be_explored_pages[page] + '\n'
    log += "\n\tNumber of explored images : {}".format(len(explored_images))
    log += "\n\tNumber of images to be explored: \
    {}".format(len(to_be_explored_images))
    log += "\n\tCrawl round duration : {}s".format(duration)

    with open("log.txt", "a") as myfile:
        myfile.write(log)


def log(to_be_explored_pages, explored_pages, to_be_explored_images,
        explored_images, duration, cvt):
    """Log progression."""
    global timestamps

    # avoid duplicates
    cvt.acquire()
    dt = datetime.now().time()
    millis = dt.microsecond + dt.second * 1000000
    millis += dt.minute * 1000000 * 60 + dt.hour * 1000000 * 60 * 60
    while millis in timestamps:
        millis += 1
    timestamps.append(millis)
    cvt.release()

    log = "\n\n[" + str(millis) + "]\n\
    Explored_pages = {}".format(len(explored_pages))
    log += "\n\tTo_be_explored_pages = {}".format(len(to_be_explored_pages))
    log += "\n\tExplored_images = {}".format(len(explored_images))
    log += "\n\tImages_to_be_explored = {}".format(len(to_be_explored_images))
    log += "\n\tDuration = {}".format(duration)

    with open("log.txt", "a") as myfile:
        myfile.write(log)
