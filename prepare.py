import argparse
import subprocess
import os
import shutil
import re


def cut_doc_outline(file_):
    aux_file = "%s.tmp" % file_
    aux = open(aux_file, 'w')
    with open(file_, 'r') as f:
        for l in f.readlines():
            if l == "<a name=\"outline\"></a><h1>Document Outline</h1>\n":
                aux.write("</body>\n")
                aux.write("</html>\n")
                break
            else:
                aux.write(l)
    aux.close()
    shutil.move(aux_file, file_)


def process_pdf(party, pdf):
    path = 'build/' + party
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.basename(pdf)
    basename, extension = os.path.splitext(filename)
    shutil.copy(args.pdf, path + '/' + filename)
    subprocess.call(['pdfseparate', path + "/" + filename,
                     path + "/" + basename + "-%d.pdf"])
    one_page = re.compile(r'.*-\d+')
    for f in os.listdir(path):
        b, ext = os.path.splitext(f)
        html = "%s/%s.html" % (path, b)
        if ext == ".pdf":
            if one_page.match(b):
                subprocess.call(['pdf2htmlEX', "--tounicode", "1",
                                 "--decompose-ligature", "1",
                                 "--embed-external-font", "0",
                                 "--printing", "0",
                                 "--process-outline", "0",
                                 "--process-nontext", "0",
                                 "--optimize-text", "1",
                                 "--fit-width", "680",
                                 "%s/%s" % (path, f), html])
            else:
                subprocess.call(['pdftohtml', '-s', '-i', '-noframes',
                                 '-nomerge', '-enc', 'UTF-8',
                                 "%s/%s" % (path, f)])
                cut_doc_outline(html)
            assert os.path.exists(html), "No exists: %s" % html


def parse_args():
    desc = "Split a PDF in pages and transform the pages and the \
    complete PDF in HTML"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('party', type=str, help='The Party name')
    parser.add_argument('pdf', type=str, help='The PDF file')
    args = parser.parse_args()
    print "party: %s pdf: %s" % (args.party, args.pdf)
    return args


args = parse_args()
process_pdf(args.party, args.pdf)
