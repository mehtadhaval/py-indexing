class DataWrapper:

    """
    Wraps data and its weight for index
    """
    _data = None
    _weight = 0

    def __init__(self, data, weight):
        self.update(data, weight)

    def update(self, data, weight):
        self._data = data
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    @property
    def data(self):
        return self._data

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __eq__(self, other):
        return self._data.__eq__(other.data)

    def __hash__(self):
        return self._data.__hash__()


class ResultWrapper:
    """
    Wraps data and fdi
    """

    def __init__(self, data, initial_score):
        self._data = data
        self._score = initial_score

    def add(self, score):
        self._score += score

    @property
    def score(self):
        return self._score

    @property
    def data(self):
        return self._data

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return "{0} - score: {1}".format(repr(self._data), self._score)

    def __eq__(self, other):
        return self._data == other.data

    def __gt__(self, other):
        return self._data > other.data if self._score == other.score else self._score > other.score

    def __ge__(self, other):
        return self._data >= other.data if self._score == other.score else self._score >= other.score

    def __lt__(self, other):
        return self._data < other.data if self._score == other.score else self._score < other.score

    def __le__(self, other):
        return self._data <= other.data if self._score == other.score else self._score <= other.score


class Query:

    def __init__(self, query):
        if isinstance(query, str):
            query = query.split()
        self._terms = query

    @property
    def terms(self):
        return self._terms

    @staticmethod
    def calculate_score(term_weight, obj_weight):
        return term_weight*obj_weight


class IndexEngine:

    def index(self, key, weight, obj):
        raise NotImplementedError("Method not implemented")

    def search(self, query, page_size):
        raise NotImplementedError("Method not implemented")

    def normalize(self, index_string):
        raise NotImplementedError("Method not implemented")


class InverseIndexEngine(IndexEngine):

    def __init__(self, max_weight):
        """
        :param max_weight: Max weight for object to be indexed / query term
        """
        self._index = {}
        self._max_weight = max_weight

    def index(self, key, obj, index):
        """
        Index an object
        :param key: Key against which to index the object
        :param obj: Source object
        :param index: Index of the object. To be useful to calculate weight
        :return:
        """
        weight = self._max_weight - index
        _obj_list = self._index.get(key)
        data_obj = DataWrapper(obj, weight)
        if not _obj_list:
            self._index[key] = [DataWrapper(obj, weight)]
            return
        try:
            # find and update the weight if already exists
            obj_index = _obj_list.index(data_obj)
            _obj_list[obj_index] = data_obj
        except ValueError:
            # not found, append data
            _obj_list.append(data_obj)

    def search(self, query, page_size=5):
        """
        Search the index for terms contained in query
        :param query: Query to be searched
        :param page_size: Max no of pages to return
        :return: List of objects matching the query
        """
        query_terms = query.terms
        results_map = {}
        for term_index, query_term in enumerate(query_terms):
            term_weight = self._max_weight - term_index
            try:
                obj_list = self._index[self.normalize(query_term)]
                for obj in obj_list:
                    score = query.calculate_score(term_weight, obj.weight)
                    try:
                        result_obj = results_map[obj]
                        result_obj.add(score)
                    except KeyError:
                        results_map[obj] = ResultWrapper(obj.data, score)
            except KeyError:
                continue
        results = list(results_map.values())
        results.sort(reverse=True)
        results = [obj.data for obj in results[:5]]
        return results

    def normalize(self, index_string):
        """
        Normalization function, describes processing to be done on strings while indexing and searching
        """
        return index_string.lower()
