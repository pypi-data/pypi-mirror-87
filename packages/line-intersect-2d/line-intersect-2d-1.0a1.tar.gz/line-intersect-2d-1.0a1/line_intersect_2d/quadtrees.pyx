import math
from satella.coding.sequences import f_range, add_next, half_cartesian, group_quantity

from .basics cimport maximum, minimum, Point, Segment


cdef class QuadtreeNode:
    """
    :ivar top_left: top left (Point)
    :ivar bottom_right: bottom right (Point)
    :ivar segments: segments (tp.List[Segment])
    """
    def __init__(self, x1, y1, x2, y2, tag):
        self.top_left = Point(minimum(x1, x2),
                               minimum(y1, y2))
        self.bottom_right = Point(maximum(x1, x2),
                                   maximum(y1, y2))
        self.segments = []
        self.tag = tag

    cdef void append(self, Segment s):
        self.segments.append(s)
        s.q_nodes.append(self.tag)

    cdef Segment get_edge(self, int edge):
        if edge == TOP:
            return Segment(Point(self.top_left.x, self.top_left.y),
                           Point(self.bottom_right.x, self.top_left.y))
        elif edge == RIGHT:
            return Segment(Point(self.bottom_right.x, self.bottom_right.y),
                           Point(self.bottom_right.x, self.top_left.y))
        elif edge == BOTTOM:
            return Segment(Point(self.bottom_right.x, self.bottom_right.y),
                           Point(self.top_left.x, self.bottom_right.y))
        elif edge == LEFT:
            return Segment(Point(self.top_left.x, self.top_left.y),
                           Point(self.top_left.x, self.bottom_right.y))
        else:
            raise ValueError(f'Invalid edge number {edge}')

    cdef bint contains(self, Point x):
        return self.start.x <= x.x <= self.stop.x and \
               self.start.y <= x.y <= self.stop.y

    cdef bint includes(self, Segment s):
        """
        :param s: segment s 
        :return: does segment s belong to this node?
        :rtype: bool
        """
        cdef:
            bint result = True
            int i
        if self.contains(s.start) or self.contains(s.stop):
            result = True
        else:
            for i in range(EVERY_EDGE):
                if self.get_edge(i).intersects(s):
                    result = True
                    break
        print(f'Decided if {self} collides with {s}, result is {result}')
        return result


cdef class Path:
    """
    A path made from connected segments.

    This is immutable.

    Constructor works as:

    >>> p = Path([Segment(...), Segment(...)])

    or

    >>> p = Path((x1, y1), (x2, y2), ...)

    :ivar segments: list of segments (tp.List[Segment])
    """
    def __init__(self, *args):
        cdef Segment s
        if isinstance(args[0], list):
            self.segments = args[0]
        else:
            self.segments = []
            for p1, p2 in add_next(args, skip_last=True):
                s = Segment(Point(*p1), Point(*p2))
                self.segments.append(s)

    def __str__(self):
        return f'<Path(%s)>' % (self.segments, )

    cdef void apply_tag(self, int tag):
        """
        Set all segments to have a particular tag
        
        :param tag: tag to set
        :type tag: int 
        """
        cdef Segment s
        for s in self.segments:
            s.tag = tag

    cdef Segment area(self):
        cdef:
            double min_x = math.inf, min_y = math.inf
            double max_x = -math.inf, max_y = -math.inf
            Segment s
            Point top_left, bottom_right
        for s in self.segments:
            top_left = s.get_minimum()
            bottom_right = s.get_maximum()
            if top_left.x < min_x:
                min_x = top_left.x
            if bottom_right.x > max_x:
                max_x = bottom_right.x
            if top_left.y < min_y:
                min_y = top_left.y
            if bottom_right.y > max_y:
                max_y = bottom_right.y

        return Segment(Point(min_x, min_y), Point(max_x, max_y))


cdef class Quadtree:
    def __init__(self, v1: Point, v2: Point, edge_x: float, edge_y: float):
        cdef:
            double x1 = minimum(v1.x, v2.x)
            double y1 = minimum(v1.y, v2.y)
            double x2 = maximum(v1.x, v2.x)
            double y2 = maximum(v1.y, v2.y)

            double x_start, x_stop, y_start, y_stop
            int tag = 0
        self.nodes = []

        for x_start, x_stop in add_next(f_range(x1, x2, edge_x), skip_last=True):
            for y_start, y_stop in add_next(f_range(y1, y2, edge_y), skip_last=True):
                self.nodes.append(QuadtreeNode(x_start, y_start, x_stop, y_stop, tag))
                tag += 1

    cdef void add_segment(self, Segment segment):
        cdef QuadtreeNode q_node
        for q_node in self.nodes:
            if q_node.includes(segment):
                q_node.append(segment)
                print(f'Appended {segment} to node {q_node.tag}')

    cdef void add_path(self, Path path):
        cdef Segment s
        for s in path.segments:
            self.add_segment(s)

    cdef tuple get_collision(self):
        cdef:
            QuadtreeNode q_node
            Segment s1, s2
            int i = 0
        for q_node in self.nodes:
            if q_node.segments:
                print(f'Examining {i}-th node')
                for s1, s2 in half_cartesian(q_node.segments, include_same_pairs=False):
                    if s1.intersects(s2):
                        if s1.tag != s2.tag:
                            return s1, s2
            i += 1
        return None


cpdef tuple check_intersection(list paths, float split_factor=0.1):
    cdef:
        int tag
        Path p
        Quadtree tree
        double min_x = math.inf, max_x = -math.inf
        double min_y = math.inf, max_y = -math.inf
        Segment area

    for tag in range(len(paths)):
        p = paths[tag]
        p.apply_tag(tag)

    for p in paths:
        area = p.area()
        if area.start.x < min_x:
            min_x = area.start.x
        if area.start.y < min_y:
            min_y = area.start.y
        if area.stop.x > max_x:
            max_x = area.stop.x
        if area.stop.y > max_y:
            max_y = area.stop.y

    tree = Quadtree(Point(min_x, min_y), Point(max_x, max_y),
                    (max_x-min_x)*split_factor,
                    (max_y-min_y)*split_factor)

    for p in paths:
        tree.add_path(p)

    return tree.get_collision()


