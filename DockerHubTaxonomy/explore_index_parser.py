from html.parser import HTMLParser
import requests
folder = 'pages/'
# create a subclass and override the handler methods
class ExploreIndexParser(HTMLParser):
        links = list()

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "a":
                print("Encountered a link tag:")
                if 'class' in attrs and attrs['class'] == 'RepositoryListItem__flexible___3R0Sg':
                    self.links.append(attrs['href'])
                    #print(attrs)

# instantiate the parser and fed it some HTML
parser = ExploreIndexParser()

f = open('test.html', 'r')
content = f.read()
parser.feed(content)
f.close
print(parser.links)
for link in parser.links:
    filename = link.strip('/_')
    print("dl " + filename)
    r = requests.get('http://hub.docker.com' + link)
    f = open(folder + filename + '.html', 'w', encoding="utf8")
    f.write(r.text)
    f.close
