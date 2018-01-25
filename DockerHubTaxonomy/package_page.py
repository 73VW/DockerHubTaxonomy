"""Package page explorer process."""
import hashlib
import multiprocessing
import time
from html.parser import HTMLParser

import requests

from dockerfile_explorer import dockerfileProcess
from search_page import SearchPageProcess


# create a subclass and override the handler methods
class PackagePageParser(HTMLParser):
    """Parser class."""

    links = list()

    def handle_starttag(self, tag, attrs):
        """Return dockerfiles links."""
        attrs = dict(attrs)
        if tag == "a":
            if (attrs is not None
                and 'href' in attrs
                and attrs['href'] is not None
                    and 'Dockerfile' in attrs['href']):
                self.links.append(attrs['href'])


class packagePageProcess(multiprocessing.Process):
    """Process class."""

    def __init__(self, to_be_explored_pages, explored_pages,
                 to_be_explored_images, explored_images, cv, cvi, cvt, gq, lq):
        """Init process."""
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.to_be_explored_pages = to_be_explored_pages
        self.explored_pages = explored_pages
        self.to_be_explored_images = to_be_explored_images
        self.explored_images = explored_images
        self.cv = cv
        self.cvi = cvi
        self.cvt = cvt
        self.gq = gq
        self.lq = lq
        self.parser = PackagePageParser()

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            try:
                self.package_page_crawler()
            except (RuntimeError, KeyboardInterrupt) as e:
                self.shutdown()

    def shutdown(self):
        """Shut down process."""
        self.exit.set()

    def package_page_crawler(self):
        """Find dockerfiles in package."""
        start_time = time.time()
        self.cv.acquire()
        while not self.to_be_explored_pages:
            if self.cv.wait(10) is False:  # cleanup
                self.cv.release()
                raise RuntimeError
        page, link = self.to_be_explored_pages.popitem()
        self.cv.release()

        hash_object = hashlib.md5(page.encode())
        node = "\"" + str(hash_object.hexdigest()) + "\""
        node += " [label=\"" + page + "\", shape=point]"
        self.gq.put(node)

        p = None
        if len(self.to_be_explored_pages) < 300:
            # start a process to go through search pages
            p = SearchPageProcess(self.to_be_explored_pages,
                                  self.explored_pages,
                                  self.to_be_explored_images,
                                  self.explored_images,
                                  self.cv, self.cvt, page, self.lq)
            p.start()

        r = requests.get(link)
        package_page = r.text

        # find package dockerfiles
        # don't need to join because process exits itself
        self.find_dockerfiles_in_package_page(package_page, page)

        self.explored_pages[page] = link
        stop_time = time.time()
        duration = stop_time - start_time

        self.lq.put((len(self.to_be_explored_pages),
                     len(self.explored_pages),
                     len(self.to_be_explored_images),
                     len(self.explored_images),
                     duration))

        # print("Crawled page {}, duration : {}s".format(page, duration))

    def find_dockerfiles_in_package_page(self, page, page_name):
        """Return links found in page."""
        self.parser.links = list()
        self.parser.feed(page)
        for link in self.parser.links:
            prefix = ""
            if 'https' in link:
                prefix = "https"
            else:
                prefix = "http"
            link = link.replace(prefix + '://github.com/', '')
            link = link.replace('blob/', '')
            link = 'https://raw.githubusercontent.com/' + link
            if (link not in self.to_be_explored_images and
                    link not in self.explored_images):
                self.cvi.acquire()
                self.to_be_explored_images.append(link)
                self.cvi.release()
                p = dockerfileProcess(
                    self.to_be_explored_pages,
                    self.explored_pages,
                    self.to_be_explored_images,
                    self.explored_images,
                    self.cv,
                    self.cvi,
                    self.cvt,
                    self.gq,
                    page_name, self.lq)
                p.start()
                return p
