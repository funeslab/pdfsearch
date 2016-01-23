import requests
import os
import argparse
import subprocess
import re


INDEX_URL = 'http://localhost:9200/election'
PRETTY = "?pretty=true"

requests.encoding = 'utf-8'


def pretty(url):
    return url + PRETTY


def parse_args():
    # http://www.ine.es/daco/daco42/codmun/cod_ccaa.htm
    # party, year, program_id, zone, path
    desc = "Load a program to ElasticSearch"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-a', '--party', type=str, help='The Party name')
    parser.add_argument('-y', '--year', type=int, help='The Program year')
    parser.add_argument('-i', '--program_id', type=str,
                        help='The identifier for this program')
    parser.add_argument('-z', '--zone', type=int, help='The CCAA code. INE.')
    parser.add_argument('-p', '--path', type=str,
                        help='The path to the program.')
    parser.add_argument('-d', '--delete', action='store_true', default=False,
                        help='Delete de index.')
    parser.add_argument('-s', '--schema', action='store_true', default=False,
                        help='Delete de index.')
    return parser.parse_args()


def _htmlanalyzer():
    htmlanalyzer = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "htmlanalyzer": {
                        "type": "custom",
                        "char_filter": ["html_strip"],
                        "tokenizer": "standard",
                        "filter": ["standard", "lowercase"]
                    }
                }
            }
        }
    }
    result = requests.put(pretty(INDEX_URL), json=htmlanalyzer)
    print "Analyzer:"
    print result.text


def _program_schema():
    properties = {
        "properties": {
            "content": {
                "index": "analyzed",
                "type": "string",
                "analyzer": "htmlanalyzer",
                "term_vector": "with_positions_offsets",
                "store": True
            }
        }
    }
    url_map = "/".join((INDEX_URL, 'program', '_mapping'))
    result = requests.put(pretty(url_map), json=properties)
    print "Mapping program:"
    print result.text
    url_map = "/".join((INDEX_URL, 'page', '_mapping'))
    result = requests.put(pretty(url_map), json=properties)
    print "Mapping page:"
    print result.text


def schema():
    _htmlanalyzer()
    _program_schema()


def _party_id(party):
    return party.lowercase()


def _insert(id_, type_, data):
    result = requests.put(INDEX_URL + "/" + type_ + "/" + id_ + PRETTY,
                          json=data)
    print "Add %s: %s" % (type_, id_)
    print result.text


def _get_pages(file_name):
    file_name = file_name[:-4] + "pdf"
    stdout = subprocess.check_output(['pdfinfo', file_name])
    pages = 0
    # Pages:          74
    pagesre = re.compile(r'Pages:\s+(\d+)')
    for line in stdout.split('\n'):
        res = pagesre.match(line)
        if res:
            pages = res.group(1)
            break
    assert pages > 0
    return pages


def _insert_program(program_id, party, year, file_name, zone):
    text = open(file_name).read()
    pages = _get_pages(file_name)
    data = {
        "party": party,
        "year": year,
        "content": text,
        "pages": pages,
        "zone": zone
    }
    _insert(program_id, "program", data)


def _insert_page(program_id, page, file_name):
    text = open(file_name).read()
    data = {
        "program": program_id,
        "page": page,
        "content": text
    }
    page_id = "%s-%s" % (program_id, page)
    _insert(page_id, "page", data)


# http://www.ine.es/daco/daco42/codmun/cod_ccaa.htm
def program(party, year, program_id, zone, path):
    for f in os.listdir(path):
        b, ext = os.path.splitext(f)
        if ext == '.html':
            file_ = path + '/' + f
            if '-' in f:
                page = int(b.split('-')[1])
                _insert_page(program_id, page, file_)
            else:
                _insert_program(program_id, party, year, file_, zone)


def delete_index():
    result = requests.delete(pretty(INDEX_URL))
    print "Delete:"
    print result.text

# http://www.ine.es/daco/daco42/codmun/cod_ccaa.htm

if __name__ == "__main__":
    args = parse_args()
    if args.schema:
        schema()
    elif args.delete:
        delete_index()
    else:
        program(args.party, args.year, args.program_id, args.zone, args.path)
