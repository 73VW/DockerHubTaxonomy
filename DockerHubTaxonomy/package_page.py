import requests
import copy
from html.parser import HTMLParser
import time
import multiprocessing

from tools import filter, print_progression, log_progression

# create a subclass and override the handler methods
class PackagePageParser(HTMLParser):
        links = list()

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "a":
                if 'href' in attrs and 'Dockerfile' in attrs['href']:
                    self.links.append(attrs['href'])

class packagePageProcess(multiprocessing.Process):

    def __init__(self, to_be_explored_pages, explored_pages,to_be_explored_images,explored_images, cv):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.to_be_explored_pages = to_be_explored_pages
        self.explored_pages = explored_pages
        self.to_be_explored_images = to_be_explored_images
        self.explored_images = explored_images
        self.cv = cv
        self.parser = PackagePageParser()

    def run(self):
        while not self.exit.is_set():
            try:
                self.package_page_crawler()
            except:
                self.shutdown()
        print( "You exited package process!")

    def shutdown(self):
        print ("Shutdown initiated")
        self.exit.set()

    def package_page_crawler(self):
        """
        Find subpackages in package dockerfiles
        """
        start_time = time.time()
        self.cv.acquire()
        while not self.to_be_explored_pages:
            if self.cv.wait(10) is False: #cleanup
                self.cv.release()
                raise RuntimeError
        page, link = self.to_be_explored_pages.popitem()
        self.cv.release()
        with open("log.txt", "a") as myfile:
            myfile.write("\n[Crawling] " + page)
        r = requests.get(link)
        package_page = r.text
        #find package dockerfiles
        dockerfiles = self.find_dockerfiles_in_package_page(package_page)
        #find subpackages in those dockerfiles
        for dockerfile in dockerfiles:
            line = filter("^FROM.+", dockerfile)
            sub_package_name = line.split()[1].split(':')[0] if line is not None else "scratch"
            if sub_package_name not in self.explored_images and sub_package_name not in self.to_be_explored_images:
                with open("log.txt", "a") as myfile:
                    myfile.write("\n[New package name]: " + sub_package_name)
                self.to_be_explored_images[sub_package_name] = 'http://hub.docker.com/_/' + sub_package_name
        self.explored_pages[page] = link
        stop_time = time.time()
        duration = stop_time - start_time
        self.cv.acquire()
        print_progression(self.to_be_explored_pages,self.explored_pages,self.to_be_explored_images,self.explored_images, duration)
        self.cv.release()

        print("Crawled page {}, duration : {}s".format(page, duration))



    def find_dockerfiles_in_package_page(self, page):
        """
        Return links found in pages crawled with above function
        """
        dockerfiles = []
        self.parser.links = list()
        self.parser.feed(page)
        for link in self.parser.links:
            prefix=""
            if 'http' in link:
                prefix="http"
            elif 'https' in link:
                prefix="https"
            link.replace('prefix', '')
            link = 'https://raw.githubusercontent.com/' + link.replace('://github.com/', '').replace('blob/', '')
            r = requests.get(link)
            dockerfiles.append(r.text)

        return dockerfiles
