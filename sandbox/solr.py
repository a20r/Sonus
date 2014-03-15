#!/usr/bin/env python
import solr

# create a connection to a solr server
s = solr.SolrConnection('http://example.org:8083/solr')

# add a document to the index
s.add(
    id=1,
    title='Lucene in Action',
    author=['Erik Hatcher', 'Otis Gospodnetić']
)
s.commit()

# do a search
response = s.query('title:lucene')
for hit in response.results:
        print hit['title']
