"""
Main program.
"""
from explore_page import explore_page_crawler, search_page_crawler
from package_page import package_page_crawler
from tools import print_progression, log_progression
import threading
import time
import sys
import os

def main(number_of_pages):
    """Run main program."""
    to_be_explored = {}
    explored = {}

    #download 10 pages from http://hub.docker.com/explore
    for i in range(1, number_of_pages+1):
        explore_page_crawler(i, to_be_explored)

    # TODO implement a search function
    #search link looks like this :
    # WARNING! package names containing a "/" are not referenced the same...
    # https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=1&pullCount=0&q=alpine&starCount=0
    # almost done

    # TODO store pages and packages differently
    # pages can contain more than one package

    # TODO implement multi-thread search and crawl
    # one for explore page, one for package page

    while to_be_explored:
        log_progression(to_be_explored, explored)
        page, link = to_be_explored.popitem()
        #search_page_crawler(page, to_be_explored)
        with open("log.txt", "a") as myfile:
            myfile.write("\nCrawling " + page)
        explored[page] = link
        package_page_crawler(page, link, to_be_explored, explored)

    print(str(len(explored)) + " packages explored")

if __name__ == "__main__":
    """Catch main function."""
    clear_console = 'clear'
    os.system(clear_console)
    #delete log file
    log_file = 'log.txt'
    if os.path.isfile(log_file):
        os.remove(log_file)
    # Start main as a process
    p = threading.Thread(target=main, args=(2,))
    p.start()

    # While main is running, show the program is not dead
    anim = ('-', '\\', '|', '/')
    i = 0;
    while p.is_alive():
        os.system(clear_console)
        print("Crawling... " + anim[i])
        sys.stdout.flush()
        i=(i+1)%4
        time.sleep(0.5)


    # Cleanup
    p.join()
    print("Crawl finished. Goodbye")
