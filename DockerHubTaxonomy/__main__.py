"""
Main program.
"""
from explore_page import explorePageProcess
from package_page import packagePageProcess
from tools import print_progression, log_progression
import multiprocessing
import time
import sys
import os

def main(number_of_pages):
    """Run main program."""
    explore_jobs = []
    package_jobs = []
    try:
        with multiprocessing.Manager() as manager:
            start_time = time.time()

            to_be_explored_pages = manager.dict()
            explored_pages = manager.dict()

            to_be_explored_images = manager.dict()
            explored_images = manager.dict()

            cv = manager.Condition()

            #get links in pages from http://hub.docker.com/explore
            for i in range(1, number_of_pages+1):
                p = explorePageProcess(i,to_be_explored_pages,explored_pages,to_be_explored_images,explored_images,cv)
                explore_jobs.append(p)
                p.start()
            #now go through all pages contained in the to_be_explored_pages dict using processes
            for i in range(10):
                p = packagePageProcess(to_be_explored_pages,explored_pages,to_be_explored_images,explored_images,cv)
                package_jobs.append(p)
                p.start()

            #Cleanup
            for job in explore_jobs:
                job.join()

            print("explore join!")

            #Cleanup
            for job in package_jobs:
                job.join()

            print("package join")

            stop_time = time.time()
            duration = stop_time - start_time

            print("Total duration : {}s".format(duration))
    except KeyboardInterrupt:
        #Cleanup
        for job in explore_jobs:
            job.shutdown()
            job.join()

        #Cleanup
        for job in package_jobs:
            job.shutdown()
            job.join()

    # TODO implement a search function
    #search link looks like this :
    # WARNING! package names containing a "/" are not referenced the same...
    # https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=1&pullCount=0&q=alpine&starCount=0
    # almost done

    # TODO store pages and packages differently
    # pages can contain more than one package

    # TODO implement multi-thread search and crawl
    # one for explore page, one for package page
    """
    while to_be_explored:
        log_progression(to_be_explored, explored)
        page, link = to_be_explored.popitem()
        #search_page_crawler(page, to_be_explored)
        with open("log.txt", "a") as myfile:
            myfile.write("\nCrawling " + page)
        explored[page] = link
        package_page_crawler(page, link, to_be_explored, explored)

    print(str(len(explored)) + " packages explored")
    """

if __name__ == "__main__":
    #WARNING only 10 pages are offered under explore
    number_of_pages = 10

    clear_console = 'clear'
    os.system(clear_console)
    #delete log file
    log_file = 'log.txt'
    if os.path.isfile(log_file):
        os.remove(log_file)
    # Start main as a process
    try:
        p = multiprocessing.Process(target=main, args=(number_of_pages,))
        p.start()

        # While main is running, show the program is not dead
        anim = ('-', '\\', '|', '/')
        i = 0;
        while p.is_alive():
            #os.system(clear_console)
            print("Crawling... " + anim[i])
            sys.stdout.flush()
            i=(i+1)%4
            time.sleep(0.5)

    finally:
        # Cleanup
        p.join()
        print("Crawl finished. Goodbye")
