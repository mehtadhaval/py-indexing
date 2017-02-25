from py_indexing.index import DataIndex


class Page(DataIndex):
    """
    Represents a page object
    """

    def __init__(self, id, tags):
        if isinstance(tags, str):
            tags = tags.split()
        self._tags = tags
        self._id = id

    def terms(self):
        return self._tags

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return "P{0}".format(self._id)

    def __str__(self):
        return "P{0} {1}".format(self._id, " ".join(self._tags))

    def __eq__(self, other):
        return self._id == other.id

    def __gt__(self, other):
        # sort with increasing page index
        return self._id < other.id

    def __ge__(self, other):
        # sort with increasing page index
        return self._id <= other.id

    def __lt__(self, other):
        # sort with increasing page index
        return self._id > other.id

    def __le__(self, other):
        # sort with increasing page index
        return self._id >= other.id

    def __hash__(self):
        return self._id
