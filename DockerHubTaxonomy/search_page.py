"""Search page explorer process."""
import multiprocessing
import time

from explore_page import ExplorePageParser, explorePageProcess


class SearchPageProcess(explorePageProcess):
    """Process class."""

    def __init__(
            self,
            to_be_explored_pages,
            explored_pages,
            to_be_explored_images,
            explored_images,
            cv,
            cvt,
            package_name, lq):
        """Init process."""
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.to_be_explored_pages = to_be_explored_pages
        self.explored_pages = explored_pages
        self.to_be_explored_images = to_be_explored_images
        self.explored_images = explored_images
        self.cv = cv
        self.cvt = cvt
        self.package_name = package_name
        self.page_number = 0
        self.lq = lq
        self.parser = ExplorePageParser()

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            try:
                self.search_page_crawler()
            except (KeyboardInterrupt, RuntimeError) as e:
                self.shutdown()
            finally:
                self.shutdown()
        # print("You exited!")

    def search_page_crawler(self):
        """Download new packages from search page."""
        start_time = time.time()
        for self.page_number in range(1, 2):
            base_link = 'https://hub.docker.com/search/'
            params = '?isAutomated=0&isOfficial=0'
            page = '&page=' + str(self.page_number)
            params += '&pullCount=0'
            query = '&q={q_p}&starCount=0'.format(q_p=self.package_name)
            link = base_link + params + page + query
            self.download_and_get_new_packages(link)

        stop_time = time.time()
        duration = stop_time - start_time
        self.lq.put((len(self.to_be_explored_pages),
                     len(self.explored_pages),
                     len(self.to_be_explored_images),
                     len(self.explored_images),
                     duration))
