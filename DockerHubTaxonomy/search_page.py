"""Search page explorer process."""
from explore_page import explorePageProcess


class explorePageProcess(explorePageProcess):
    """Process class."""

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            self.explore_page_crawler()
            self.shutdown()
        print("You exited!")

    def search_page_crawler(self):
        """Download new packages from search page."""
        """
        for self.page_number in range(1, 2):
            link = 'https://hub.docker.com/search/?isAutomated=0\
            &isOfficial=0&page={p_n}&pullCount=0&q={q_p}\
            &starCount=0'.format(p_n=self.page_number, q_p=query_package)
            self.download_and_get_new_packages(link)
        """
