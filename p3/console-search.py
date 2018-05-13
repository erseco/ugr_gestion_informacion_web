#!/usr/bin/env python

"""console-search.py: Test script for lucene index."""

__author__      = "Ernesto Serrano"
__license__     = "GPL"
__version__     = "1.0.1"
__email__       = "erseco@correo.ugr.es"

import sys
import lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.es import SpanishAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

if __name__ == "__main__":

    if len(sys.argv) != 3:

        print sys.argv[0]+' <stopWords> <searchString>'
        exit()

    indexDirectory=sys.argv[1]
    searchString=sys.argv[2]


    lucene.initVM()
    analyzer = SpanishAnalyzer()
    reader = IndexReader.open(SimpleFSDirectory(File(indexDirectory)))
    searcher = IndexSearcher(reader)

    query = QueryParser("text", analyzer).parse(searchString)
    MAX = 1000
    hits = searcher.search(query, MAX)

    print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
    for hit in hits.scoreDocs:
        print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        # print doc.get("text").encode("utf-8")
        print doc.get("filename")
