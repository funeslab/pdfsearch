# Intro

This program finds words and/or phrases in PDF document pages.

It returns the matches highlighting our searches.

It works as the find in a PDF Viewer but, it is online and search among several
files together.

Now it is set up to search in electoral programs but, you can load the PDF files
you want without many problems.

Example: [Buscador de programas](http://programas.funeslab.com)

# Technologies

* Python (tested with version 2.7.9)
* Django (tested with version 1.8.6)
* Elasticsearch (tested with version 2.0.0)
* pdf2htmlEX (tested with version 0.12)
* pdfseparate (tested with version 0.26.5)
* Docker (tested with version 1.9.1)

# Content

This repository contain:

* `web` The django project and app.
* `docker` Docker files or scripts to build the entire system.
* `doc` Some documentation
* `programs` The PDF documents.
* `prepare.py` and `prepare.sh` scripts to prepare programs to Elasticsearch.
* `load.py` and `load.sh` scripts to load documents to Elasticsearch.


# How to use it

This program has two parts: one, a script to **load documents** to
elasticsearch and another a web interface to **query documents**.

## Load documents

You load a document in ElasticSearch in two steps:

1. Prepare documents
2. Load documents to ElasticSearch

### Prepare documents

Use `prepare.sh` scripts to prepare programs to Elasticsearch.

It is a script that call one time for every document to  `prepare.py`.

`prepare.py` divides PDF files in pages and transforms PDF files to HTML.

```
$ python  prepare.py -h

usage: prepare.py [-h] party pdf

Split a PDF in pages and transform the pages and the complete PDF in HTML

positional arguments:
  party       The Party name
  pdf         The PDF file

optional arguments:
  -h, --help  show this help message and exit
```

### Load documents to ElasticSearch

Use `load.sh` to load the data to Elasticsearch. It is a script that call one
time for every document to `load.py`.

`load.py` modifies the elasticsearch database.

```
$ python  load.py -h

usage: load.py [-h] [-a PARTY] [-y YEAR] [-i PROGRAM_ID] [-z ZONE] [-p PATH]
               [-d] [-s]

Load a program to ElasticSearch

optional arguments:
  -h, --help            show this help message and exit
  -a PARTY, --party PARTY
                        The Party name
  -y YEAR, --year YEAR  The Program year
  -i PROGRAM_ID, --program_id PROGRAM_ID
                        The identifier for this program
  -z ZONE, --zone ZONE  The CCAA code. INE.
  -p PATH, --path PATH  The path to the program.
  -d, --delete          Delete de index.
  -s, --schema          Delete de index.
```

## Query documents

You can search in documents with the web application. This web application is a
Django Project in `web` directory.

# More info

* [Requirements](./doc/requirements.md)
* [Architecture or design](./doc/design.md)
