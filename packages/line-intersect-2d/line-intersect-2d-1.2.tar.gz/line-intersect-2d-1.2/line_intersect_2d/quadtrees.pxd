from .basics cimport Point, Segment

cdef enum:
    TOP = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3
    EVERY_EDGE = 4

cdef class QuadtreeNode:
    cdef:
        readonly Point top_left
        readonly Point bottom_right
        readonly list segments
        int tag

    cdef bint includes(self, Segment s)
    cdef bint contains(self, Point x)
    cdef Segment get_edge(self, int edge)
    cdef void append(self, Segment s)

cdef class Path:
    cdef:
        readonly list segments

    cdef void apply_tag(self, int tag)
    cdef Segment area(self)


cdef class Quadtree:
    cdef:
        readonly Point top_left
        readonly Point bottom_right
        readonly list nodes

    cdef tuple get_collision(self)
    cdef void add_path(self, Path path)
    cdef void add_segment(self, Segment segment)


cpdef tuple check_intersection(list paths, float split_factor=*)
