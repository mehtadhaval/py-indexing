from py_indexing.data import Page
from py_indexing.index import InverseIndexEngine, Query


def search_data(data_str):
    queries = []
    index_engine = InverseIndexEngine(8)
    page_count = 0
    for line in data_str.split("\n"):
        data_type, data = line.split(maxsplit=1)
        if data_type == "P":
            page_count += 1
            page = Page(id=page_count, tags=data)
            page.index(index_engine)
        elif data_type == "Q":
            queries.append(Query(data))
        else:
            continue

    for query_index, query in enumerate(queries):
        results = index_engine.search(query)
        print("{query}: {results}".format(query="Q{0}".format(query_index+1), results=" ".join([repr(result) for result in results])))


def main():
    data = "P Ford Car Review\n" \
           "P Review Car\n" \
           "P Review Ford\n" \
           "P Toyota Car\n" \
           "P Honda Car\n" \
           "P Car\n" \
           "Q Ford\n" \
           "Q Car\n" \
           "Q Review\n" \
           "Q Ford Review\n" \
           "Q Ford Car\n" \
           "Q cooking French "
    search_data(data)


if __name__ == "__main__":
    main()
