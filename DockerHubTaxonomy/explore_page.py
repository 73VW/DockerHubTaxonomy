"""Explore page explorer process."""
import multiprocessing
import time
from html.parser import HTMLParser

import requests

from tools import log_progression


# create a subclass and override the handler methods
class ExplorePageParser(HTMLParser):
    """Parser class."""

    links = list()

    def handle_starttag(self, tag, attrs):
        """
        Return link matching a class name.

        Fucked up but only way found for the moment.
        """
        target_link = 'RepositoryListItem__flexible___3R0Sg'
        attrs = dict(attrs)
        if tag == "a":
            if 'class' in attrs and attrs['class'] == target_link:
                self.links.append(attrs['href'])


class explorePageProcess(multiprocessing.Process):
    """Process class."""

    def __init__(self, page_number, to_be_explored_pages, explored_pages,
                 to_be_explored_images, explored_images, cv):
        """Init process."""
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.page_number = page_number
        self.to_be_explored_pages = to_be_explored_pages
        self.explored_pages = explored_pages
        self.to_be_explored_images = to_be_explored_images
        self.explored_images = explored_images
        self.cv = cv
        self.parser = ExplorePageParser()

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            try:
                self.explore_page_crawler()
            finally:
                self.shutdown()
        print("You exited explore!")

    def shutdown(self):
        """Shut down process."""
        print("Shutdown initiated")
        self.exit.set()

    def explore_page_crawler(self):
        """
        Return a list containing number_of_pages html pages.

        Pages are found in docker hub explore pages
        """
        start_time = time.time()

        base_link = 'http://hub.docker.com/explore'
        link = base_link+'?page={p_n}'.format(p_n=self.page_number)
        self.download_and_get_new_packages(link)
        stop_time = time.time()
        duration = stop_time - start_time

        log_progression(self.to_be_explored_pages, self.explored_pages,
                        self.to_be_explored_images, self.explored_images,
                        duration)

        print("Crawled page {}, duration : {}s".format(self.page_number,
                                                       duration))

    def download_and_get_new_packages(self, link):
        """Download and find new packages in link."""
        r = requests.get(link)
        self.find_links_in_explore_page(r.text)
        return r.status_code

    def find_links_in_explore_page(self, page):
        """Find links in pages crawled with above function."""
        self.parser.links = list()
        self.parser.feed(page)
        for link in self.parser.links:
            package_name = link.strip('/_')
            if package_name not in self.to_be_explored_pages:
                self.cv.acquire()
                new_link = 'http://hub.docker.com' + link
                self.to_be_explored_pages[package_name] = new_link
                self.cv.notify()
                self.cv.release()
