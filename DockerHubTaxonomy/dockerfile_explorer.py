"""Dockerfile explorer process."""
import multiprocessing
import re
import time

import requests

from tools import log_progression


class dockerfileProcess(multiprocessing.Process):
    """Process class."""

    def __init__(self, to_be_explored_pages, explored_pages,
                 to_be_explored_images, explored_images, cv, cvi):
        """Init process."""
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.to_be_explored_pages = to_be_explored_pages
        self.explored_pages = explored_pages
        self.to_be_explored_images = to_be_explored_images
        self.explored_images = explored_images
        self.cv = cv
        self.cvi = cvi

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            try:
                self.dockerfile_crawler()
            except (RuntimeError, KeyboardInterrupt) as e:
                self.shutdown()
        print("You exited dockerfile process!")

    def shutdown(self):
        """Shut down process."""
        print("Shutdown initiated")
        self.exit.set()

    def dockerfile_crawler(self):
        """Find subpackages in package dockerfiles."""
        start_time = time.time()
        self.cvi.acquire()
        while not self.to_be_explored_images:
            if self.cvi.wait(5) is False:  # cleanup
                self.cvi.release()
                raise RuntimeError
        link = self.to_be_explored_images.pop()
        self.cvi.release()

        r = requests.get(link)
        dockerfile = r.text

        re_result = re.match("^FROM\s*(?P<package>[^:]+)",
                             dockerfile)
        if re_result is not None:
            sub_package_name = re_result.group('package')

            if (sub_package_name not in self.explored_pages and
                    sub_package_name not in self.to_be_explored_pages):
                with open("log.txt", "a") as myfile:
                    myfile.write("\n[New package name]: " + sub_package_name)
                self.cvi.acquire()
                new_link = 'http://hub.docker.com/_/' + sub_package_name
                self.to_be_explored_pages[sub_package_name] = new_link
                self.cvi.release()
                print(sub_package_name)
                exit(0)

        self.explored_images.append(link)
        stop_time = time.time()
        duration = stop_time - start_time

        log_progression(self.to_be_explored_pages, self.explored_pages,
                        self.to_be_explored_images, self.explored_images,
                        duration)

        print("Crawled page {}, duration : {}s".format(link, duration))
