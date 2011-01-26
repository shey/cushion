# Cushion: a simple CouchDB Document API wrapper

This is a Python wrapper for the [CouchDB Document API](http://wiki.apache.org/couchdb/HTTP_Document_API). It was created primarily as an exercise to learn CouchDB's document API.  The library attempts to expose a very simple interface that closely resembles REST.

For example,

	from cushion import api
	
    c = api.Cushion("http://localhost:5984/albums",
		username='abc',
		password='xyz'
	)
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