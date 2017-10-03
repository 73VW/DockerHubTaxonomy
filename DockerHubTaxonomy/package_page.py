import requests
import copy
from html.parser import HTMLParser

from tools import filter

# create a subclass and override the handler methods
class PackagePageParser(HTMLParser):
        links = list()

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "a":
                if 'href' in attrs and 'Dockerfile' in attrs['href']:
                    self.links.append(attrs['href'])

def package_page_crawler(to_be_explored, explored):
    """
    Find subpackages in package dockerfiles
    """
    new_to_be_explored = copy.deepcopy(to_be_explored)
    #next line is a volunteer error!
    #normally: for page in to_be_explored
    #Start back here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    page = to_be_explored[to_be_explored.keys()[0]]
    r = requests.get(new_to_be_explored[page])
    package_page = r.text
    #find package dockerfiles
    dockerfiles = find_dockerfiles_in_package_page(package_page)
    #find subpackages in those dockerfiles
    for dockerfile in dockerfiles:
        line = filter("^FROM.+", dockerfile)
        sub_package_name = line.split()[1]
        if sub_package_name not in (explored and new_to_be_explored):
            new_to_be_explored[sub_package_name] = 'http://hub.docker.com/_/' + sub_package_name
    #set page explored
    explored[page] = to_be_explored[page]
    del new_to_be_explored[page]
    return new_to_be_explored



def find_dockerfiles_in_package_page(page):
    """
    Return links found in pages crawled with above function
    """
    dockerfiles = []
    parser = PackagePageParser()
    parser.feed(page)
    for link in parser.links:
        link = 'https://raw.githubusercontent.com/' + link.replace('https://github.com/', '').replace('blob/', '')
        r = requests.get(link)
        dockerfiles.append(r.text)
    return dockerfiles
