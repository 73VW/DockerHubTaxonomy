import requests
from html.parser import HTMLParser

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

def explore_page_crawler(number_of_pages):
    """
    Return a list containing number_of_pages html pages from docker hub explore pages
    """
    liste = []
    for i in range(1, number_of_pages+1):
        link = 'http://hub.docker.com/explore?page={page_number}'.format(page_number=i)
        r = requests.get(link)
        page = ""
        for line in r:
            # Decode what you receive:
            page += line.decode(r.encoding)

        liste.append(page)
    return find_links_in_explore_page(liste)

def find_links_in_explore_page(pages_list):
    """
    Return links found in pages crawled with above function
    """
    links = {}
    parser = ExplorePageParser()
    for page in pages_list:
        parser.feed(page)
        for link in parser.links:
            package_name = link.strip('/_')
            if package_name not in links:
                links[package_name] = 'http://hub.docker.com' + link
    return links
