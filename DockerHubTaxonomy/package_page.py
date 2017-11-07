"""Package page explorer process."""
import multiprocessing
import time
from html.parser import HTMLParser

import requests

from dockerfile_explorer import dockerfileProcess
from tools import log_progression


# create a subclass and override the handler methods
class PackagePageParser(HTMLParser):
    """Parser class."""

    links = list()

    def handle_starttag(self, tag, attrs):
        """Return dockerfiles links."""
        attrs = dict(attrs)
        if tag == "a":
            if 'href' in attrs and 'Dockerfile' in attrs['href']:
                self.links.append(attrs['href'])


class packagePageProcess(multiprocessing.Process):
    """Process class."""

    def __init__(self, to_be_explored_pages, explored_pages,
                 to_be_explored_images, explored_images, cv, cvi, cvd,
                 dockerfile_jobs):
        """Init process."""
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.to_be_explored_pages = to_be_explored_pages
        self.explored_pages = explored_pages
        self.to_be_explored_images = to_be_explored_images
        self.explored_images = explored_images
        self.cv = cv
        self.cvi = cvi
        self.cvd = cvd
        self.dockerfile_jobs = dockerfile_jobs
        self.parser = PackagePageParser()

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            try:
                self.package_page_crawler()
            except (RuntimeError, KeyboardInterrupt) as e:
                self.shutdown()
        print("You exited package process!")

    def shutdown(self):
        """Shut down process."""
        print("Shutdown initiated")
        self.exit.set()

    def package_page_crawler(self):
        """Find dockerfiles in package."""
        start_time = time.time()
        self.cv.acquire()
        while not self.to_be_explored_pages:
            if self.cv.wait(5) is False:  # cleanup
                self.cv.release()
                raise RuntimeError
        page, link = self.to_be_explored_pages.popitem()
        self.cv.release()

        r = requests.get(link)
        package_page = r.text

        # find package dockerfiles
        self.find_dockerfiles_in_package_page(package_page)

        self.explored_pages[page] = link
        stop_time = time.time()
        duration = stop_time - start_time

        log_progression(self.to_be_explored_pages, self.explored_pages,
                        self.to_be_explored_images, self.explored_images,
                        duration)

        print("Crawled page {}, duration : {}s".format(page, duration))

    def find_dockerfiles_in_package_page(self, page):
        """Return links found in page."""
        self.parser.links = list()
        self.parser.feed(page)
        for link in self.parser.links:
            prefix = ""
            if 'https' in link:
                prefix = "https"
            else:
                prefix = "http"
            link = link.replace(prefix+'://github.com/', '')
            link = link.replace('blob/', '')
            link = 'https://raw.githubusercontent.com/' + link
            if (link not in self.to_be_explored_images and
                    link not in self.explored_images):
                self.cvi.acquire()
                self.to_be_explored_images.append(link)
                self.cvi.release()
                p = dockerfileProcess(self.to_be_explored_pages,
                                      self.explored_pages,
                                      self.to_be_explored_images,
                                      self.explored_images,
                                      self.cv, self.cvi)
                self.cvd.acquire()
                self.dockerfile_jobs.append(p)
                self.cvd.release()
                p.start()
