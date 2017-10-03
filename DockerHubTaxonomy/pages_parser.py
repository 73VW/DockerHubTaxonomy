from html.parser import HTMLParser
import os

import requests
pages_folder = 'pages/'
root_dockerfile_folder = "dockerfile/"
# create a subclass and override the handler methods
class ExploreIndexParser(HTMLParser):
        links = list()

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "a":
                if 'href' in attrs and 'Dockerfile' in attrs['href']:
                    self.links.append(attrs['href'])

# instantiate the parser and fed it some HTML
parser = ExploreIndexParser()
if not os.path.exists(root_dockerfile_folder):
    os.makedirs(root_dockerfile_folder)
    print("created : " + root_dockerfile_folder)
for fname in os.listdir(pages_folder):
    print("parsing " + fname)
    f = open(pages_folder+fname, 'r', encoding="utf8")
    content = f.read()
    parser.feed(content)
    f.close

    dockerfile_folder = root_dockerfile_folder + fname.strip('.html')+"/"
    print("future folder : " + dockerfile_folder)
    if not os.path.exists(dockerfile_folder):
        os.makedirs(dockerfile_folder)
        print("created : " + dockerfile_folder)

    for link in parser.links:
        print("1 : " + link)
        link = link.replace('https://github.com/', '')
        print("2 : " + link)
        link = link.replace('blob/', '')
        print("3 : " + link)
        filename = link.replace('/', '-')
        link = 'https://raw.githubusercontent.com/' + link
        print("4 : " + link)
        print("new file : " + dockerfile_folder + filename)
        r = requests.get(link)
        f = open(dockerfile_folder + filename, 'w+', encoding="utf8")
        f.write(r.text)
        f.close
    exit(0)
