"""Main program.

"""
from explore_page import explore_page_crawler
from package_page import package_page_crawler

def main():
    """Run main program."""
    to_be_explored = {}
    explored = {}

    #download 10 pages from http://hub.docker.com/explore
    to_be_explored = explore_page_crawler(1)
    print_progression(to_be_explored, explored)
    to_be_explored = package_page_crawler(to_be_explored, explored)
    print_progression(to_be_explored, explored)


def print_progression(to_be_explored, explored):
    print("Explored pages : ")
    for page in explored:
        print(page)
    print("To be Explored pages : ")
    for page in to_be_explored:
        print(page)



if __name__ == "__main__":
    """Catch main function."""
    main()
