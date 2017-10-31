import requests
from html.parser import HTMLParser
from tools import log_progression, print_progression
import time
import multiprocessing

# create a subclass and override the handler methods
class ExplorePageParser(HTMLParser):
    links = list()

    def handle_starttag(self, tag, attrs):
        """
        Return link matching a class name

        Fucked up but only way found for the moment.
        """
        attrs = dict(attrs)
        if tag == "a":
            if 'class' in attrs and attrs['class'] == 'RepositoryListItem__flexible___3R0Sg':
                self.links.append(attrs['href'])
                #print(attrs)

class explorePageProcess(multiprocessing.Process):

    def __init__(self, page_number, to_be_explored_pages, explored_pages,to_be_explored_images,explored_images, cv):
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
        while not self.exit.is_set():
            self.explore_page_crawler()
            self.shutdown()
        print( "You exited!")

    def shutdown(self):
        print ("Shutdown initiated")
        self.exit.set()


    def explore_page_crawler(self):
        """
        Return a list containing number_of_pages html pages from docker hub explore pages
        """
        start_time = time.time()
        link = 'http://hub.docker.com/explore?page={p_n}'.format(p_n=self.page_number)
        self.download_and_get_new_packages(link)
        stop_time = time.time()
        duration = stop_time - start_time

        print_progression(self.to_be_explored_pages,self.explored_pages,self.to_be_explored_images,self.explored_images, duration)

        print("Crawled page {}, duration : {}s".format(self.page_number, duration))


    def search_page_crawler(self):
        for self.page_number in range(1, 2):
            link = 'https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page={p_n}&pullCount=0&q={q_p}&starCount=0'.format(p_n=self.page_number, q_p=query_package)
            self.download_and_get_new_packages(link)

    def download_and_get_new_packages(self, link):
        r = requests.get(link)
        self.find_links_in_explore_page(r.text)
        return r.status_code


    def find_links_in_explore_page(self, page):
        """
        Find links in pages crawled with above function
        """
        self.parser.links=list()
        self.parser.feed(page)
        for link in self.parser.links:
            package_name = link.strip('/_')
            if package_name not in self.to_be_explored_pages:
                self.cv.acquire()
                self.to_be_explored_pages[package_name] = 'http://hub.docker.com' + link
                self.cv.notify()
                self.cv.release()
