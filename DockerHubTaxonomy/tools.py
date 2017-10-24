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




def print_progression(to_be_explored, explored):
    log = "\n\nAt "+str(datetime.now())+ " :\nNumber of explored pages : {}\nExplored pages :\n".format(len(explored))
    for page in explored:
        log += page + '\t--\t' + explored[page] + '\n'
    log += "\nNumber of pages to be explored: {}\nTo be Explored pages :\n".format(len(to_be_explored))
    for page in to_be_explored:
        log += page + '\t--\t' + to_be_explored[page] + '\n'
    with open("log.txt", "a") as myfile:
        myfile.write(log)

def log_progression(to_be_explored, explored):
    log = "\n\nAt "+str(datetime.now())+ " :\nNumber of explored pages : {}".format(len(explored))
    log += "\nNumber of pages to be explored: {}".format(len(to_be_explored))
    with open("log.txt", "a") as myfile:
        myfile.write(log)
