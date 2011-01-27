# Cushion: a simple CouchDB wrapper

Cushion is a very thin python wrapper around [CouchDB's Document API](http://wiki.apache.org/couchdb/HTTP_Document_API). It's interface closely mimics REST.  It was created primarily as an exercise to learn CouchDB's API, Cushion is not an object mapper, it doesn’t enforce ‘OOP’, and if you found it difficult to get started with CouchDB using other libraries then you maybe interested in Cushion.

To connect to CouchDB:

	from cushion import api

    c = api.Cushion("http://localhost:5984/albums",
		username='abc',
		password='xyz'
	)

Issuing:

	c.get(id='1b0c7bb19b1bbacf7f567bf379000d9c')

returns the following JSON object:

    {
		'Band': 'The Postal Service',
		'_rev':'1-f319aeef4dbb8c232f0257cf2a9ae64b',
		'_id': '1b0c7bb19b1bbacf7f567bf379000d9c',
		'Name': 'Give Up'
	}

alternatively, the database can be specified at runtime,

	c = api.Cushion("http://localhost:5984",
		username='abc',
		password='xyz',
		timeout=5
	)
	c.get.albums(id='1b0c7bb19b1bbacf7f567bf379000d9c')

which also returns:

	{
		'Band': 'The Postal Service',
		'_rev':'1-f319aeef4dbb8c232f0257cf2a9ae64b',
		'_id': '1b0c7bb19b1bbacf7f567bf379000d9c',
		'Name': 'Give Up'
	}

## Examples

To retrieve a document including previous version numbers:

	c.get.albums(id='1b0c7bb19b1bbacf7f567bf379000d9c', revs='true')

to get a listing of all documents in a database:

	c.get.albums._all_docs(startkey="1", limit=100)

to create a document with a document id:

	c.put.albums(id='c3ea09f0-9758-480c-aa25-0f71a9caa446', Name='Transatlanticism', Band='Death Cab For Cutie')

alternatively, to create a document without supplying the document id:

	c.post.albums(Name='In Ghost Colors', Band='Cut Copy')


## Installation

    easy_install cushion

## Links

* [CouchDB Document API Documentation](http://wiki.apache.org/couchdb/HTTP_Document_API)
* [Source Code](https://github.com/sheysrebellion/cushion)

## TODO

* more examples
* more documentation

## Copyright

Copyright (c) 2011 Sheheryar Sewani. See LICENSE for details.