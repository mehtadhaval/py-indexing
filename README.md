py-indexing
===================
A simple in-memory indexing engine built in Python.

This piece of code uses [inverse-indexing](https://en.wikipedia.org/wiki/Inverted_index) to index Page objects, which can be searched against query terms.

How to Use
-------------
This code contains an indexing engine `py_indexing.index.InverseIndexEngine` which provides APIs `index` and `search` to index and search data.

How to Run
-------------
This code also contains `main.py` file, which indexes fixed data and and prints the output against provided search queries. To run it, just execute the file. e.g.

    python3.4 main.py

