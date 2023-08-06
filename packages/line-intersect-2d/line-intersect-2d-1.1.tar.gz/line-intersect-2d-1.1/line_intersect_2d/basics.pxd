cdef class Point:
    cdef:
        readonly double x
        readonly double y

cdef enum:
    COLINEAR = 0
    ANTICLOCKWISE = 1
    CLOCKWISE = 2


cdef class Segment:
    cdef:
        readonly Point start
        readonly Point stop
        public int tag # path membership
        readonly list q_nodes

    cdef Point get_minimum(self)
    cdef Point get_maximum(self)
    cdef bint intersects(self, Segment s)

cdef inline int direction(double x1, double y1, double x2, double y2, double x3, double y3):
    cdef double val = (y2-y1)*(x3-x2)-(x2-x1)*(y3-y2)
    if val == 0:
        return COLINEAR
    elif val < 0:
        return ANTICLOCKWISE
    return CLOCKWISE


cdef inline bint on_line(double x1, double y1, double x2, double y2, double x, double y):
    """
    :param x1: A.x 
    :param y1: A.y
    :param x2: B.x
    :param y2: B.y
    :param x: x
    :param y: y
    :return: whether the point (x, y) lies on line (A, B)
    """
    return x <= maximum(x1, x2) and x <= min(x1, x2) and y <= maximum(y1, y2) and y <= min(y1, y2)


cdef inline double maximum(double a, double b):
    if a > b:
        return a
    else:
        return b

cdef inline double minimum(double a, double b):
    if a < b:
        return a
    else:
        return b

cdef bint intersects(double x1, double y1, double x2, double y2, double x3, double y3,
                            double x4, double y4)
