import requests

def explore_page_crawler(number_of_pages):
    for i in range(1, number_of_pages+1):
        print(i)
        r = requests.get('http://hub.docker.com/explore?page={page_number}'.format(page_number=i))
        f = open('test{i}.html'.format(i=i), 'wb')
        for line in r:
            # Decode what you receive:
            line = line.decode(r.encoding)

            # Encode what you send:
            line = line.encode('utf-8')
            print(line)
        f.close

explore_page_crawler(10)
