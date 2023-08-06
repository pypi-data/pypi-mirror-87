cdef class Point:
    cdef:
        readonly double x
        readonly double y

    cpdef Point add(self, Point p)
    cpdef Point sub(self, Point p)
    cpdef Point mul(self, double p)
    cpdef Point div(self, double p)

cdef class Segment:
    cdef:
        readonly Point start
        readonly Point stop
        public int tag # path membership
        readonly list q_nodes

    cdef Point get_minimum(self)
    cdef Point get_maximum(self)
    cdef bint intersects(self, Segment s)
    cpdef Point intersection_point(self, Segment s_)

cdef int direction(double x1, double y1, double x2, double y2, double x3, double y3)

cdef bint on_line(double x1, double y1, double x2, double y2, double x, double y)
cdef double maximum(double a, double b)

cdef double minimum(double a, double b)

cdef bint intersects(double x1, double y1, double x2, double y2, double x3, double y3,
                            double x4, double y4)
