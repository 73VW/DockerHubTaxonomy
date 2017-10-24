import requests
from html.parser import HTMLParser
from tools import log_progression
import time

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

def explore_page_crawler(page_number, to_be_explored_pages, explored_pages,to_be_explored_images,explored_images):
    """
    Return a list containing number_of_pages html pages from docker hub explore pages
    """
    start_time = time.time()
    link = 'http://hub.docker.com/explore?page={p_n}'.format(p_n=page_number)
    download_and_get_new_packages(link, to_be_explored_pages)
    log_progression(to_be_explored_pages,explored_pages,to_be_explored_images,explored_images)
    stop_time = time.time()
    duration = stop_time - start_time

    print("Crawled page {}, duration : {}s".format(page_number, duration))


def search_page_crawler(query_package, to_be_explored_pages):
    for page_number in range(1, 2):
        link = 'https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page={p_n}&pullCount=0&q={q_p}&starCount=0'.format(p_n=page_number, q_p=query_package)
        download_and_get_new_packages(link, to_be_explored_pages)

def download_and_get_new_packages(link, to_be_explored_pages):
    r = requests.get(link)
    find_links_in_explore_page(r.text, to_be_explored_pages)
    return r.status_code


def find_links_in_explore_page(page, to_be_explored_pages):
    """
    Find links in pages crawled with above function
    """
    parser = ExplorePageParser()
    parser.links=list()
    parser.feed(page)
    for link in parser.links:
        package_name = link.strip('/_')
        if package_name not in to_be_explored_pages:
            to_be_explored_pages[package_name] = 'http://hub.docker.com' + link
