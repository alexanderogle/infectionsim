# Class for timing functions
import time
import logging
import typing
import uuid

class Anchor:
    def __init__(self):
        self.start = time.time()
        self.end = None
        self.id = uuid.uuid4()

    def end_anchor(self):
        self.end = time.time()

    def get_start(self) -> float:
        return self.start

    def get_end(self) -> float:
        return self.end

    def timing(self) -> float:
        if(self.end != None):
            return self.end - self.start
        else:
            logging.error("Anchor has no end, cannot return a time.")

class AnchorTracker:

    def __init__(self):
        self.anchors = {}
        self.verbose = False

    def create_anchor(self, anchor_name: str) -> None:
        # Instantiates the anchor
        if anchor_name not in self.anchors:
            self.anchors[anchor_name] = Anchor()
        elif self.verbose:
            logging.warning(f'Anchor \'{anchor_name}\' already exists.')

    def end_anchor(self, anchor_name: str) -> None:
        if anchor_name in self.anchors and self.anchors[anchor_name].get_end() == None:
            # Set the end of the anchor
            self.anchors[anchor_name].end_anchor()
        elif anchor_name in self.anchors and self.anchors[anchor_name].get_end() != None and self.verbose:
            logging.warning(f'Anchor \'{anchor_name}\' already has an end.')
        elif self.verbose:
            logging.warning(f'Anchor \'{anchor_name}\' does not exist.')

    def timing(self, anchor_name: str) -> float:
        if anchor_name in self.anchors and self.anchors[anchor_name].get_end() != None:
            t = self.anchors[anchor_name].get_end() - self.anchors[anchor_name].get_start()
            return t
        elif self.verbose:
            logging.warning(f'Anchor \'{anchor_name}\' does not exist')

    def timing_all(self) -> dict:
        times = {}
        for anchor in self.anchors:
            if self.anchors[anchor].get_end() != None:
                t = self.timing(anchor)
                times[anchor] = t
        return times

    def set_verbose(self, var: bool) -> None:
        self.verbose = var

    def get_anchors(self) -> typing.List[Anchor]:
        return self.anchors.values()

    def __str__(self):
        str = ''
        for anchor in self.anchors:
            str += f'For anchor \'{anchor}\':\n'
            str += f'\tstart_time: {self.anchors[anchor].get_start()}\n'
            if self.anchors[anchor].get_end() != None:
                str += f'\tend_time: {self.anchors[anchor].get_end()}\n'
        return str
