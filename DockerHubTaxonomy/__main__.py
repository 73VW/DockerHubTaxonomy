"""Main program."""
import multiprocessing
import os
import sys
import time

from explore_page import explorePageProcess
from package_page import packagePageProcess


def main(number_of_pages, duration):
    """Run main program."""
    explore_jobs = []
    package_jobs = []
    dockerfile_jobs = []
    start_time = time.time()

    try:
        with multiprocessing.Manager() as manager:

            to_be_explored_pages = manager.dict()
            explored_pages = manager.dict()

            to_be_explored_images = manager.list()
            explored_images = manager.list()

            cv = manager.Condition()  # condition for pages
            cvi = manager.Condition()  # condition for dockerfiles
            cvd = manager.Condition()  # condition for dockerfiles_jobs

            # get links in pages from http://hub.docker.com/explore
            for i in range(1, number_of_pages+1):
                p = explorePageProcess(i, to_be_explored_pages, explored_pages,
                                       to_be_explored_images, explored_images,
                                       cv)
                explore_jobs.append(p)
                p.start()

            # now go through all pages contained in the to_be_explored_pages
            # dict using processes
            for i in range(number_of_pages*5):
                p = packagePageProcess(to_be_explored_pages, explored_pages,
                                       to_be_explored_images, explored_images,
                                       cv, cvi, cvd, dockerfile_jobs)
                package_jobs.append(p)
                p.start()

            # Cleanup
            for job in explore_jobs:
                job.join()

            # Cleanup
            for job in package_jobs:
                job.join()

            # Cleanup
            for job in dockerfile_jobs:
                job.join()

    except (KeyboardInterrupt, RuntimeError) as e:
        # Cleanup
        for job in explore_jobs:
            job.shutdown()
            job.join()

        # Cleanup
        for job in package_jobs:
            job.shutdown()
            job.join()

        # Cleanup
        for job in dockerfile_jobs:
            job.shutdown()
            job.join()

    finally:
        stop_time = time.time()
        duration.value = stop_time - start_time

    # TODO implement a search function
    # search link looks like this :
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
    # WARNING only 10 pages are offered under explore
    number_of_pages = 10
    duration = multiprocessing.Value('d', 0)
    clear_console = 'clear'
    os.system(clear_console)
    # delete log file
    log_file = 'log.txt'
    if os.path.isfile(log_file):
        os.remove(log_file)
    # Start main as a process
    try:
        p = multiprocessing.Process(target=main,
                                    args=(number_of_pages, duration, ))
        p.start()

        # While main is running, show the program is not dead
        anim = ('-', '\\', '|', '/')
        i = 0
        while p.is_alive():
            os.system(clear_console)
            print("Crawling... " + anim[i])
            sys.stdout.flush()
            i = (i + 1) % 4
            try:
                time.sleep(0.5)
            except (Exception, KeyboardInterrupt) as e:
                pass

    finally:
        # Cleanup
        p.join()
        os.system(clear_console)
        print("Crawl finished.\nTotal duration :\
              {}s\nGoodbye".format(duration.value))
