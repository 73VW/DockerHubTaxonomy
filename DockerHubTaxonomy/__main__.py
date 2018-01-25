"""Main program."""
import multiprocessing
import os
import sys
import time
from datetime import datetime
from multiprocessing import Process

from explore_page import explorePageProcess
from graph_builder import GraphBuilder
from logger import Logger
from package_page import packagePageProcess


def main(number_of_pages, stop_time):
    """Run main program."""
    # declare process lists
    package_jobs = []
    explore_jobs = []

    directory_name = time.strftime("%Y-%m-%d_%H-%M")
    current_crawl = "./generated/crawl-" + directory_name
    if not os.path.exists(current_crawl):
        os.makedirs(current_crawl)
    graph_target_file = current_crawl + "/graph.dot"
    log_target_file = current_crawl + "/log.txt"

    try:
        with multiprocessing.Manager() as manager:

            to_be_explored_pages = manager.dict()
            explored_pages = manager.dict()

            to_be_explored_images = manager.list()
            explored_images = manager.list()

            cv = manager.Condition()  # condition for pages
            cvi = manager.Condition()  # condition for dockerfiles
            cvt = manager.Condition()  # condition for timestamps

            gq = manager.Queue()
            lq = manager.Queue()

            logger = Logger(lq, log_target_file)
            logger.start()

            # get links in pages from http://hub.docker.com/explore
            for i in range(1, number_of_pages + 1):
                p = explorePageProcess(i, to_be_explored_pages, explored_pages,
                                       to_be_explored_images, explored_images,
                                       cv, cvt, lq)
                explore_jobs.append(p)
                p.start()

            # now go through all pages contained in the to_be_explored_pages
            # dict using processes
            for i in range(number_of_pages * 5):
                p = packagePageProcess(to_be_explored_pages, explored_pages,
                                       to_be_explored_images, explored_images,
                                       cv, cvi, cvt, gq, lq)
                package_jobs.append(p)
                p.start()

            graph_builder = GraphBuilder(gq, graph_target_file)
            graph_builder.start()

            # Cleanup
            for job in explore_jobs:
                job.join()

            # Cleanup
            for job in package_jobs:
                job.join()

            graph_builder.join()
            logger.join()

    except (KeyboardInterrupt, RuntimeError) as e:
        # Cleanup
        for job in explore_jobs:
            job.shutdown()
            job.join()

        # Cleanup
        for job in package_jobs:
            job.shutdown()
            job.join()

        graph_builder.shutdown()
        graph_builder.join()
        logger.shutdown()
        logger.join()

    finally:
        stop_time.value = time.time()


if __name__ == "__main__":
    # WARNING only 10 pages are offered under explore
    start_time = time.time()
    number_of_pages = 10
    stop_time = multiprocessing.Value('d', 0)
    clear_console = 'clear'
    os.system(clear_console)
    # delete log file
    log_file = 'log.txt'

    # start log file
    with open(log_file, "w") as myfile:
        myfile.write("# " + str(datetime.now()))

    # Start main as a process
    try:
        p = Process(target=main,
                    args=(number_of_pages, stop_time, ))
        p.start()

        # While main is running, show the program is not dead
        anim = ('-', '\\', '|', '/')
        i = 0
        while p.is_alive():
            os.system(clear_console)
            print("Crawling... " + anim[i])
            print("time elapsed ", time.time() - start_time, "s")
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
              {}s\nGoodbye".format(stop_time.value - start_time))
