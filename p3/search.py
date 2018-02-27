#!/usr/bin/env python

"""search.py: Search script for lucene index."""

__author__      = "Ernesto Serrano"
__license__     = "GPL"
__version__     = "1.0.1"
__email__       = "erseco@correo.ugr.es"

from flask import Flask, flash, render_template, request, redirect


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

from flask_table import Table, Col, LinkCol

from wtforms import Form, StringField, SelectField, validators


if len(sys.argv) != 2:

    print sys.argv[0]+' <indexDirectory>'
    exit()

indexDirectory=sys.argv[1]



app = Flask(__name__)
app.secret_key = "flask rocks!"


class SearchForm(Form):
    # choices = [('Artist', 'Artist'),
    #            ('Album', 'Album'),
    #            ('Publisher', 'Publisher')]
    # select = SelectField('Search for music:', choices=choices)
    search = StringField('')

class Results(Table):
    filename = Col('Filename')
    text = Col('Text')
    # link = LinkCol('Link', 'edit', url_kwargs=dict(id='filename'))

# Get some objects
class Row(object):
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text

@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    print "buscando:"+search_string

#     if search.data['search'] == '':
#         qry = db_session.query(Album)
#         results = qry.all()
    lucene.initVM()
    # analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    analyzer = SpanishAnalyzer()
    reader = IndexReader.open(SimpleFSDirectory(File(indexDirectory)))
    searcher = IndexSearcher(reader)

    query = QueryParser("text", analyzer).parse(search_string)
    MAX = 1000
    hits = searcher.search(query, MAX)

    if not hits.totalHits:
        flash('No results found!')
        return redirect('/')
    else:

        # print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
        flash("Found %d document(s) that matched query '%s':" % (hits.totalHits, query))
        # render_template('index.html', form=search)
        items = []
        for hit in hits.scoreDocs:
            # print hit.score, hit.doc, hit.toString()
            doc = searcher.doc(hit.doc)
            items.append(Row(doc.get("filename"), doc.get("text")))
        #     print hit.score, hit.doc, hit.toString()
        #     doc = searcher.doc(hit.doc)
        #     # print doc.get("text").encode("utf-8")
        #     print


        # display results
        table = Results(items)
        table.border = True
        return render_template('index.html', form=search, table=table)

if __name__ == '__main__':
    import os
    # if 'WINGDB_ACTIVE' in os.environ:
    app.debug = True
    app.run(host= '0.0.0.0', port=8080, debug=True)