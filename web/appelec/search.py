import requests
import argparse

INDEX_URL = 'http://elasticsearch:9200/election'
PRETTY = "?pretty=true"

requests.encoding = 'utf-8'

# Characters that are part of Lucene query syntax must be stripped
# from user input: + - && || ! ( ) { } [ ] ^ " ~ * ? : \
# See: http://lucene.apache.org/java/3_0_2/queryparsersyntax.html#Escaping
SPECIAL_CHARS = [33, 34, 38, 40, 41, 42, 45, 58, 63, 91, 92, 93, 94, 123, 124,
                 125, 126]
UNI_SPECIAL_CHARS = dict((c, None) for c in SPECIAL_CHARS)


def pretty(url):
    return url + PRETTY


def _clean_string(text):
    """
    Remove Lucene reserved characters from query string
    """
    return text.translate(UNI_SPECIAL_CHARS).strip()


def parse_args():
    desc = "Search texts in ElasticSearch."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('phrases', metavar='P', nargs='+',
                        help='Phrases to search')
    parser.add_argument('-p', '--program', type=str, help='The program id')
    parser.add_argument('-n', '--page', type=int, help='The page number')
    parser.add_argument('-v', '--view_html', action='store_true',
                        default=False, help='Print the HTML to stdout.')
    args = parser.parse_args()
    return args


def search(text):
    data = {
        "query": {
            "match_phrase": {
                "content": text
            }
        },
        "highlight": {
            "fields": {
                "content": {
                    "number_of_fragments": 0
                }
            },
            "pre_tags": ["<em class='match'>"],
            "post_tags": ["</em>"]
        }
    }
    result = requests.get(pretty(INDEX_URL + "/_search/"), json=data)
    data = result.json()
    hits = data['hits']['total']
    content = data['hits']['hits'][0]['highlight']['content'][0]
    return (hits, content)


def _or_query_string(phrases):
    return " OR ".join(['\"' + _clean_string(p) + '\"' for p in phrases])


def programs(phrases, ids):
    """
    Return:
    {
      "total": 2,
      "max_score": 0.071510606,
      "hits": [
         {
            "_index": "election",
            "_type": "program",
            "_id": "podemos",
            "_score": 0.071510606
         },
         {
            "_index": "election",
            "_type": "program",
            "_id": "pp",
            "_score": 0.02175878
         }
      ]
    }
    """
    data = {
        "fields": ["party", "pages"],
        "size": 1000,
        "query": {
            "filtered": {
                "query": {
                    "query_string": {
                        "default_field": "content",
                        "query": _or_query_string(phrases)
                    }
                },
                "filter": {
                    "ids": {
                        "values": ids
                    }
                }
            }
        }
    }
    print "AAAAAAAAAAAAAAAA--------------------"
    print data
    print "--------------------"
    result = _search(data, document='program')
    return result[u'hits']


def pages(phrases, program):
    """
    Return:
    Like programs, but "max_score" and "_score" is none.
    Results: Ordered by page number.
    """
    data = {
        "_source": False,
        "size": 1000,
        "sort": [{"page": {"order": "asc"}}],
        "query": {
            "filtered": {
                "query": {
                    "query_string": {
                        "default_field": "content",
                        "query": _or_query_string(phrases)
                    }
                },
                "filter": {
                    "term": {"program": program}
                }
            }
        }
    }
    result = _search(data, document='page')
    return result[u'hits']


def page(page_id):
    data = {
        "fields": ["content"],
        "query": {
            "ids": {
                "values": [page_id]
            }
        }
    }
    result = _search(data, document='page')
    assert result[u'hits']['total'] == 1
    assert len(result[u'hits']['hits']) == 1
    return result[u'hits']['hits'][0]["fields"]["content"][0]


def page_highlight(phrases, page_id):
    query = _or_query_string(phrases)
    data = {
        "_source": False,
        "query": {
            "ids": {
                "values": [page_id]
            }
        },
        "highlight": {
            "fields": {
                "content": {
                    "highlight_query": {
                        "query_string": {
                            "default_field": "content",
                            "query": query
                        }
                    },
                    "number_of_fragments": 0
                },
            },
            "pre_tags": ["<em class='match' style='background-color:yellow;'>"],
            "post_tags": ["</em>"]
        }
    }
    result = _search(data, document='page')
    assert result[u'hits']['total'] == 1
    assert len(result[u'hits']['hits']) == 1
    return result[u'hits']['hits'][0]


def _search(data, document=None, identifier=None):
    url = INDEX_URL
    if document:
        url += '/' + document
    if identifier:
        url += '/' + identifier
    url += '/_search'
    result = requests.get(pretty(url), json=data)
    return result.json()


if __name__ == "__main__":
    args = parse_args()
    phrases = [unicode(u, 'utf-8') for u in args.phrases]
    program = args.program
    page = args.page
    is_view = args.view_html

    if args.page:
        if args.program:
            result = text(phrases, program, page)
            if is_view:
                result = result['highlight']["content"][0]
            else:
                aux = result['highlight']["content"][0]
                result['highlight']["content"][0] = aux[0:14] + " (...)"
        else:
            raise ValueError("Arg -n/--page without arg -p/--program.")
    else:
        if args.program:
            result = pages(phrases, program)
        else:
            result = programs(phrases)
    if is_view:
        print result.encode('utf-8')
    else:
        pprint.pprint(result)
