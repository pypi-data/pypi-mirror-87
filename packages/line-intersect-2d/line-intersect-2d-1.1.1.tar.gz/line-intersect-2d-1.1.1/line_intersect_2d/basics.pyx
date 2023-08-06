cdef enum:
    COLINEAR = 0
    ANTICLOCKWISE = 1
    CLOCKWISE = 2


cdef int direction(double x1, double y1, double x2, double y2, double x3, double y3):
    cdef double val = (y2-y1)*(x3-x2)-(x2-x1)*(y3-y2)
    if val == 0:
        return COLINEAR
    elif val < 0:
        return ANTICLOCKWISE
    return CLOCKWISE


cdef bint on_line(double x1, double y1, double x2, double y2, double x, double y):
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


cdef double maximum(double a, double b):
    if a > b:
        return a
    else:
        return b

cdef double minimum(double a, double b):
    if a < b:
        return a
    else:
        return b


cdef class Point:
    """
    A single point.

    This is immutable, hashable and __eq__able.
    Take care when comparing floats.

    :param x: x coordinate
    :type x: float
    :param y: y coordinate
    :type y: float

    :ivar x: x coordinate (float)
    :ivar y: y coordinate (float)
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y)

    def __str__(self):
        return 'Point(%s, %s)' % (self.x, self.y)


cdef class Segment:
    """
    A segment.

    This is immutable (save for tag), __eq__able and hashable.

    :param start: start point
    :type start: Vector
    :param stop: stop point
    :type stop: Vector

    :ivar start: start point (Point)
    :ivar stop: stop point (Point)
    :ivar tag: tag (int), writable
    :ivar q_nodes: numbers of q-nodes that this segment belongs to (tp.List[int])
    """
    def __init__(self, start: Point, stop: Point,
                 tag: int = 0):
        self.start = start
        self.stop = stop
        self.tag = tag
        self.q_nodes = []

    def __str__(self):
        return 'Segment(%s, %s, %s)' % (self.start, self.stop, self.tag)

    def __eq__(self, other: Segment) -> bool:
        return ((self.start == other.start) and (self.stop == other.stop)) or \
               ((self.start == other.stop) and (self.stop == other.start))

    def __hash__(self) -> int:
        return hash(self.start) ^ hash(self.stop)

    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y)



    cdef Point get_minimum(self):
        return Point(minimum(self.start.x, self.stop.x), minimum(self.start.y, self.stop.y))

    cdef Point get_maximum(self):
        return Point(maximum(self.start.x, self.stop.x), maximum(self.start.y, self.stop.y))

    cdef bint intersects(self, Segment s):
        """
        :param s: segment s 
        :return: do this segment and s intersect
        :rtype: bool 
        """
        return intersects(self.start.x, self.start.y,
                          self.stop.x, self.stop.y,
                          s.start.x, s.start.y,
                          s.stop.x, s.stop.y)

cdef bint intersects(double x1, double y1, double x2, double y2, double x3, double y3,
                            double x4, double y4):
    cdef:
        int dir1 = direction(x1, y1, x2, y2, x3, y3)
        int dir2 = direction(x1, y1, x2, y2, x4, y4)
        int dir3 = direction(x3, y3, x4, y4, x1, y1)
        int dir4 = direction(x3, y3, x4, y4, x2, y2)

    if dir1 != dir2 and dir3 != dir4:
        return True
    if dir1 == COLINEAR and on_line(x1, y1, x2, y2, x3, y3):
        return True
    if dir2 == COLINEAR and on_line(x1, y1, x2, y2, x4, y4):
        return True
    if dir3 == COLINEAR and on_line(x3, y3, x4, y4, x1, y1):
        return True
    if dir4 == COLINEAR and on_line(x3, y3, x4, y4, x2, y2):
        return True
    return False

