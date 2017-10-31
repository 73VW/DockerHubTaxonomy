import re
from datetime import datetime

def filter(regexp, text):
    """
    Returns lines matching regexp in file
    """
    lines = text.splitlines()
    prog = re.compile(regexp, re.IGNORECASE)
    for k in [line for line in lines if prog.search(line)]:
        return k

filter("^FROM.+", "FROM scratch\nFROM foo\nFROM bar")




def print_progression(to_be_explored_pages, explored_pages,to_be_explored_images,explored_images, duration):
    log = "\n\n["+str(datetime.now())+ "]\n\tNumber of explored pages : {}\n\tExplored pages :\n".format(len(explored_pages))

    #the following is needed to loop over the dict. Why? Because manager dict...
    good_d = dict(explored_pages)
    for page in good_d:
        log += "\t" + page + '\t--\t' + explored_pages[page] + '\n'
    log += "\n\tNumber of pages to be explored: {}\n\tTo be Explored pages :\n".format(len(to_be_explored_pages))

    good_d = dict(to_be_explored_pages)
    for page in good_d:
        log += "\t" + page + '\t--\t' + to_be_explored_pages[page] + '\n'
    log += "\n\tNumber of explored images : {}".format(len(explored_images))
    log += "\n\tNumber of images to be explored: {}".format(len(to_be_explored_images))
    log += "\n\tCrawl round duration : {}s".format(duration)

    with open("log.txt", "a") as myfile:
        myfile.write(log)

def log_progression(to_be_explored_pages, explored_pages,to_be_explored_images,explored_images, duration):
    log = "\n\n["+str(datetime.now())+ "]\nNumber of explored pages : {}".format(len(explored_pages))
    log += "\nNumber of pages to be explored: {}".format(len(to_be_explored_pages))
    log += "\nNumber of explored images : {}".format(len(explored_images))
    log += "\nNumber of images to be explored: {}".format(len(to_be_explored_images))
    log += "\nCrawl round duration : {}s".format(duration)

    with open("log.txt", "a") as myfile:
        myfile.write(log)
