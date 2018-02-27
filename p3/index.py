#!/usr/bin/env python

#-*- coding: utf-8 -*-

"""index.py: Indexer script using lucene."""

__author__      = "Ernesto Serrano"
__license__     = "GPL"
__version__     = "1.0.1"
__email__       = "erseco@correo.ugr.es"


import sys
import glob

from xml.etree import ElementTree as ET


import lucene

from java.io import File
from org.apache.lucene.analysis.es import SpanishAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from org.apache.lucene.analysis.util import CharArraySet

if __name__ == "__main__":

    if len(sys.argv) != 4:

        print sys.argv[0]+' <documentsDirectory> <stopWords> <indexDirectory>'
        exit()

    documentsDirectory=sys.argv[1]
    stopWords=sys.argv[2]
    indexDirectory=sys.argv[3]

    lucene.initVM()

    exclusionSet = CharArraySet(0, True)
    f = open(stopWords,'r')
    while 1:
        line = f.readline()
        if not line:break
        exclusionSet.add(line.strip())
    f.close()




    indexDir = SimpleFSDirectory(File(indexDirectory))


    writerConfig = IndexWriterConfig(SpanishAnalyzer(exclusionSet))

    writer = IndexWriter(indexDir, writerConfig)

    totalDocs = len(glob.glob(documentsDirectory+'/*.xml'))

    print "%d docs in index" % writer.numDocs()
    print "Reading %i from %s ..." % (totalDocs, documentsDirectory)

    i = 1

    for filename in glob.iglob(documentsDirectory+'/*.xml'):

        # print "Indexing %i of %i" % (i, totalDocs)

        sys.stdout.write("Indexing %i of %i\r" % (i, totalDocs))
        sys.stdout.flush()

        i += 1

        tree = ET.parse(filename)
        elements = tree.findall('.//parrafo')
        result = u" "
        for text in elements:
            # print(text.text)
            result += unicode(text.text) + " "
            # result.append(text.text + " ")


        doc = Document()

        doc.add(Field("filename", filename, Field.Store.YES, Field.Index.ANALYZED));
        doc.add(Field("text", result, Field.Store.YES, Field.Index.ANALYZED));

        # doc.add(Field("text", l, Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)
    print "Indexed %d lines from stdin (%d docs in index)" % (totalDocs, writer.numDocs())
    print "Closing index of %d docs..." % writer.numDocs()
    writer.close()
