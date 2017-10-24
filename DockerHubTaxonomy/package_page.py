import requests
import copy
from html.parser import HTMLParser

from tools import filter, print_progression

# create a subclass and override the handler methods
class PackagePageParser(HTMLParser):
        links = list()

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "a":
                if 'href' in attrs and 'Dockerfile' in attrs['href']:
                    self.links.append(attrs['href'])

def package_page_crawler(page, link, to_be_explored, explored):
    """
    Find subpackages in package dockerfiles
    """
    r = requests.get(link)
    package_page = r.text
    #find package dockerfiles
    dockerfiles = find_dockerfiles_in_package_page(package_page)
    #find subpackages in those dockerfiles
    for dockerfile in dockerfiles:
        line = filter("^FROM.+", dockerfile)
        sub_package_name = line.split()[1].split(':')[0] if line is not None else "scratch"
        if sub_package_name not in explored and sub_package_name not in to_be_explored:
            with open("log.txt", "a") as myfile:
                myfile.write("\nNew package name: " + sub_package_name)
            to_be_explored[sub_package_name] = 'http://hub.docker.com/_/' + sub_package_name



def find_dockerfiles_in_package_page(page):
    """
    Return links found in pages crawled with above function
    """
    dockerfiles = []
    parser = PackagePageParser()
    parser.links = list()
    parser.feed(page)
    for link in parser.links:
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
