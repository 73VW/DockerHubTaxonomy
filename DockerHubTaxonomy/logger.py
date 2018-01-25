"""Logging process."""
import multiprocessing
import time


class Logger(multiprocessing.Process):
    """Process class."""

    def __init__(self, queue, target_file):
        """Init process."""
        multiprocessing.Process.__init__(self)
        self.start_time = time.time()
        self.exit = multiprocessing.Event()
        self.queue = queue
        self.target_file = target_file

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            try:
                self.log_progression()
            except (KeyboardInterrupt, RuntimeError) as e:
                self.shutdown()
        # print("You exited!")

    def shutdown(self):
        """Shut down process."""
        self.exit.set()

    def log_progression(self):
        """Log progression."""
        (to_be_explored_pages, explored_pages, to_be_explored_images,
         explored_images, duration) = self.queue.get()
        self.log(to_be_explored_pages, explored_pages, to_be_explored_images,
                 explored_images, duration)

    def log(self, to_be_explored_pages, explored_pages, to_be_explored_images,
            explored_images, duration):
        """Log progression."""
        elapsed_time = time.time() - self.start_time

        log = "\n\n[\"" + str(elapsed_time) + "\"]\n\
        Explored_pages = {}".format(explored_pages)
        log += "\n\tTo_be_explored_pages = {}".format(to_be_explored_pages)
        log += "\n\tExplored_images = {}".format(explored_images)
        log += "\n\tImages_to_be_explored = {}".format(
            to_be_explored_images)
        log += "\n\tDuration = {}".format(duration)

        with open(self.target_file, "a") as myfile:
            myfile.write(log)
