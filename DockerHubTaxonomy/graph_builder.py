"""Search page explorer process."""
import multiprocessing


class GraphBuilder(multiprocessing.Process):
    """Process class."""

    def __init__(self, queue, target_file):
        """Init process."""
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.queue = queue
        self.target_file = target_file

    def run(self):
        """Run process."""
        self.init_graph()
        while not self.exit.is_set():
            try:
                self.write_graph()
            except (KeyboardInterrupt, RuntimeError) as e:
                self.shutdown()
        self.finish_graph()
        # print("You exited!")

    def shutdown(self):
        """Shut down process."""
        self.exit.set()

    def init_graph(self):
        """Init graph file."""
        self.write_to_file(self.target_file, "w",
                           "strict digraph DOCKERHUBTAXONOMY {\n")

    def write_graph(self):
        """Write nodes and edges to file."""
        new_element = self.queue.get()
        self.write_to_file(self.target_file, "a", new_element + "\n")

    def finish_graph(self):
        """Finish graph file."""
        self.write_to_file(self.target_file, "a", "}")

    def write_to_file(self, target, mode, text):
        """Write text to file with mode."""
        with open(target, mode) as f:
            f.write(text)
