""" Event support for Python. """

import typing

cdef class Event(object):
	""" Event. """

	cdef int eventtype
	cdef str eventtype_str
	cdef object eventtype_other
	def __init__(self, int eventtype, str eventtype_str, object eventtype_other)

cdef type Func = type(lambda: None)

cdef class Subscriber(object):
    """ Subscribes to a kind of event. """
    cdef int eventtype
	cdef typing.List[Event] events_recieved
	cdef Func handler

    def __init__(self, int eventtype, Func handler)

