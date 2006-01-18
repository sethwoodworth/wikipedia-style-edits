from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces

class RevisionCounter(saxutils.DefaultHandler):
    def __init__(self):
        self.articles = [] # (title, count) to appear in input order
        self.clear()

    def clear(self):
        self.current_tag = ''
        self.current_title = ''
        self.current_count = 0

    def characters(self, ch):
        if self.current_tag == 'title':
            self.current_title += ch

    def commit(self):
        if self.current_count > 0:
            pair = (self.current_title.strip().encode('utf-8'), self.current_count)
            self.articles.append(pair)
        # and nullify state
        self.clear()

    def startElement(self, name, attrs):
        self.current_tag = name

        # If it's a <page> element, then try to commit the thing we just finished
        # (screw you, end tags)
        if name == 'page':
            self.commit()

        # If it's a <revision> element, bump the count
        if name == 'revision':
            self.current_count += 1

        # That's all I was looking for.  Bye.
        
if __name__ == '__main__':
    import sys
    file = sys.stdin
    # Create a parser
    parser = make_parser()

    # Tell the parser we are not interested in XML namespaces
    parser.setFeature(feature_namespaces, 0)

    # Create the handler
    dh = RevisionCounter()

    # Tell the parser to use our handler
    parser.setContentHandler(dh)

    # Parse the input
    parser.parse(file)

    # Print the resulting data as a CSV
    import csv
    writer = csv.writer(sys.stdout)
    writer.writerows(dh.articles)

