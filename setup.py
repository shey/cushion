try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='cushion',
    version='0.1',
    author='Sheheryar Sewani',
    author_email='sheheryar.sewani@gmail.com',
    url='http://github.com/sheysrebellion/cushion',
    description='A simple wrapper for CouchDB',

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
