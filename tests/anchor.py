# Class for timing functions
import time
import logging
import typing

class Anchor:
    def __init__(self):
        self.start = time.time()
        self.end = None

    def end_anchor(self):
        self.end = time.time()

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

class AnchorTracker:

    def __init__(self):
        self.anchors = {}
        self.verbose = False

    def create_anchor(self, anchor):
        # Instantiates the anchor
        if anchor not in self.anchors:
            self.anchors[anchor] = Anchor()
        elif self.verbose:
            logging.warning(f'Anchor \'{anchor}\' already exists.')

    def end_anchor(self, anchor):
        if anchor in self.anchors and self.anchors[anchor].get_end() == None:
            # Set the end of the anchor
            self.anchors[anchor].end_anchor()
        elif anchor in self.anchors and self.anchors[anchor].get_end() != None and self.verbose:
            logging.warning(f'Anchor \'{anchor}\' already has an end.')
        elif self.verbose:
            logging.warning(f'Anchor \'{anchor}\' does not exist.')

    def timing(self, anchor):
        if anchor in self.anchors and self.anchors[anchor].get_end() != None:
            t = self.anchors[anchor].get_end() - self.anchors[anchor].get_start()
            return t
        elif self.verbose:
            logging.warning(f'Anchor \'{anchor}\' does not exist')

    def timing_all(self):
        times = {}
        for anchor in self.anchors:
            if self.anchors[anchor].get_end() != None:
                t = self.timing(anchor)
                times[anchor] = t
        return times

    def set_verbose(var: bool) -> None:
        self.verbose = var

    def __str__(self):
        str = ''
        for anchor in self.anchors:
            str += f'For anchor \'{anchor}\':\n'
            str += f'\tstart_time: {self.anchors[anchor].get_start()}\n'
            if self.anchors[anchor].get_end() != None:
                str += f'\tend_time: {self.anchors[anchor].get_end()}\n'
        return str
