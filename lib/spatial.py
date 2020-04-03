from weakref import WeakSet as _WeakSet
from functools import lru_cache as _lru_cache


class Space:
    def __init__(self, cell_size=16, bodies=()):
        self.cell_size = cell_size
        self.buckets = {}
        self.clear = self.buckets.clear
        self.insert_bodies(bodies)

    @_lru_cache(maxsize=8192)
    def _hash(self, x, y):
        """Normalize vector to cell size"""
        return int(x / self.cell_size), int(y / self.cell_size)

    def insert_body(self, body):
        """Insert body into approprite bucket"""
        min_vec, max_vec = self._hash(
            *body.aabb[0:2]), self._hash(*body.aabb[2:4])
        for i in range(min_vec[0], max_vec[0]+1):
            for j in range(min_vec[1], max_vec[1]+1):
                self.buckets.setdefault((i, j), _WeakSet()).add(body)

    def insert_bodies(self, bodies):
        """Insert bodies into approprite bucket"""
        for body in bodies:
            min_vec, max_vec = self._hash(
                *body.aabb[0:2]), self._hash(*body.aabb[2:4])
            for i in range(min_vec[0], max_vec[0]+1):
                for j in range(min_vec[1], max_vec[1]+1):
                    self.buckets.setdefault((i, j), _WeakSet()).add(body)

    def remove_body(self, body):
        """Remove body from buckets"""
        min_vec, max_vec = self._hash(
            *body.aabb[0:2]), self._hash(*body.aabb[2:4])
        for i in range(min_vec[0], max_vec[0]+1):
            for j in range(min_vec[1], max_vec[1]+1):
                self.buckets.get((i, j)).remove(body)

    def get_hits(self, aabb):
        aleft, abottom, aright, atop = aabb
        min_vec, max_vec = self._hash(aleft, abottom), self._hash(aright, atop)

        def simple_overlap(body_aabb):
            bleft, bbottom, bright, btop = body_aabb
            # An overlap has occured if ALL of these are True, otherwise return False:
            return bleft < aright and bright > aleft and btop > abottom and bbottom < atop

        hits = set()

        for i in range(min_vec[0], max_vec[0]+1):
            for j in range(min_vec[1], max_vec[1]+1):
                # append to each intersecting cell
                hits |= {body for body in self.buckets.get(
                    (i, j), set()) if simple_overlap(body.aabb)}

        return hits
