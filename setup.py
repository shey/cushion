try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='cushion',
    version='0.2',
    author='Sheheryar Sewani',
    author_email='sheheryar.sewani@gmail.com',
    url='http://github.com/sheysrebellion/cushion',
    description='A simple wrapper for CouchDB',
    long_description="""
        Cushion: a simple CouchDB Document API wrapper

        This is a Python wrapper for the CouchDB Document API (http://wiki.apache.org/couchdb/HTTP_Document_API).
        It was created primarily as an exercise to learn CouchDB's document API.
        The library attempts to expose a very simple interface that closely resembles REST.

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

        to create a document with a document id:

            c.put.albums(id='c3ea09f0-9758-480c-aa25-0f71a9caa446', Name='Transatlanticism', Band='Death Cab For Cutie')

        alternatively, to create a document without supplying the document id:

            c.post.albums(Name='In Ghost Colors', Band='Cut Copy')
    """,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    packages=[
        'cushion'
    ],

    setup_requires=[
        'setuptools-git'
    ],
    tests_require=[
        'nose',
        'mock'
    ],
    install_requires=[
        'simplejson == 2.0.9',
        'httplib2 == 0.5.0',
        'functional',
    ],

    test_suite = 'nose.collector'
)
