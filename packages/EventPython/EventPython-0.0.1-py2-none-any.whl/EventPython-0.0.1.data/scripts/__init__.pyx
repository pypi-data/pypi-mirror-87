""" Event support for Python. """

from typing cimport List
from multiprocessing cimport Process
import typing

cdef class Event(object):
    """ Event. """
    def __init__(self, int eventtype, str eventtype_str, object eventtype_other):
        self.eventtype = evventtype
        self.eventtype_str = eventtype_str
        if eventtype:
            self.eventtype_other = eventtype_other
        else:
            self.eventtype_other = self

cdef type Func = type(lambda: None)

cdef class Subscriber(object):
    """ Subscribes to a kind of event. """
    
    def __init__(self, int eventtype, Func handler):
        self.eventtype = eventtype
        self.events_recieved = List[Event]()
        self.handler = handler
    
    cdef void recieve(self, Event event):
        """ Recieve an event. """
        self.events_recieved.append(event)
        self.handler()

cdef class Clock(object):
    """ A clock that sends events to subscribers depending on the event type. """
    
    def __init__(self, List[Subscriber] subscribers):
        self.subscribers = subscribers
        self.time = time.time()
        self.events_given_to_all_subscribers = List[Event]()
        self.last_event_time = time.time()
        self.last_event = Event(0, "EV_NULL", None)
        self.proc = None
        self.running = False
    
    cdef void tick(self):
        """ Ticks the clock. """
        if self.last_event_time == time.time() or self.last_event_time == time.time() - 1:
            for subscriber in self.subscribers:
                if subscriber.eventtype == self.last_event.eventtype:
                     subscriber.recieve(self.last_event)
        self.time = time()
    
    cdef void clock(self):
        while self.running:
            self.tick()
            if self.last_event != Event(0, "EV_NULL", None):
                time.sleep(0.5)
    
    cdef void send(self, int subscriber_type, Event ev):
        for i in self.subscribers:
            if i.eventtype == subscriber_type:
                i.recieve(event)
                self.last_event = ev
                self.last_event_time = time.time()
    
    cdef void startclock(self):
        """ Starts the clock. """
        self.running = True
        self.proc = Process(target=self.clock, args={})
    
    cdef void end(self):
        """ Ends the clock. """
        self.running = False
        self.proc.kill()
        self.proc = None
        
