from horairyst.time import *


class Event(object):
    def __init__(self, length=Time(30, Time.MINUTE), subject="", person_ids={0, 0}):
        self.length = length
        self.subject = subject
        self.persons = person_ids
