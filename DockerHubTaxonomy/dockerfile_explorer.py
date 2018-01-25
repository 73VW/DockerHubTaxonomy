"""Dockerfile explorer process."""
import hashlib
import multiprocessing
import re
import time

import requests


class dockerfileProcess(multiprocessing.Process):
    """Process class."""

    def __init__(self, to_be_explored_pages, explored_pages,
                 to_be_explored_images, explored_images, cv, cvi, cvt, gq,
                 page_name, lq):
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
        self.page_name = page_name

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            try:
                self.dockerfile_crawler()
            except (RuntimeError, KeyboardInterrupt) as e:
                self.shutdown()
            finally:
                self.shutdown()

    def shutdown(self):
        """Shut down process."""
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

        re_result = re.match("^FROM\s*(?P<package>[^:\s]+)",
                             dockerfile)
        if re_result is not None:
            sub_package_name = re_result.group('package')
            new_link = 'http://hub.docker.com/_/' + sub_package_name
            hash_object1 = hashlib.md5(self.page_name.encode())
            hash_object2 = hashlib.md5(sub_package_name.encode())
            edge = "\"" + str(hash_object1.hexdigest()) + "\""
            edge += " -> "
            destination = "\"" + str(hash_object2.hexdigest()) + "\""
            edge += destination + "[arrowsize=.4, shape=vee, penwidth=0.1]"
            destination_parameters = " [label=\"" + sub_package_name + "\""

            if "scratch" in sub_package_name:
                destination_parameters += ", color=red, shape=point, root=true"
            else:
                destination_parameters += ", shape=point"
            destination += destination_parameters + "]"
            self.gq.put(destination)
            self.gq.put(edge)

            self.cvi.acquire()
            if (sub_package_name in self.explored_pages or
                    sub_package_name in self.to_be_explored_pages):
                self.cvi.release()
            else:
                self.to_be_explored_pages[sub_package_name] = new_link
                self.cvi.release()
                # print("\n[From: %s\nNew package name]:%s" % (link,
                #                                            sub_package_name))
        self.explored_images.append(link)
        stop_time = time.time()
        duration = stop_time - start_time

        self.lq.put((len(self.to_be_explored_pages),
                     len(self.explored_pages),
                     len(self.to_be_explored_images),
                     len(self.explored_images),
                     duration))
        # print("Crawled page {}, duration : {}s".format(link, duration))
