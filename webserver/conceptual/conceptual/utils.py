from hashlib import md5
import json
import os

from django.conf import settings

from bs4 import BeautifulSoup
import requests
import zmq


"""ExtractorClient to interact with the extractor service."""
class ExtractorClient():
    def __init__(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(settings.EXTRACTOR_SERVICE)

        self.socket = socket
        print 'Connected to the extractor service at %s' % (
            settings.EXTRACTOR_SERVICE)

    def parse_output(self, out):
        extractions = out.strip().split("\n")
        pairs = []

        for extraction in extractions:
            pairs.append(extraction[1:-1].split(";"))

        return pairs

    def send_extractor_request(self, text):
        self.socket.send(text)
        return self.socket.recv()


    def extract(self, text):
        res = self.send_extractor_request(text)
        return self.parse_output(res)


def store_extractions(url, extractions):
    # store extractions in DB or JSON
    file_hash = md5(url).hexdigest()
    dump_file_path = os.path.join(settings.EXTRACTIONS_PATH, file_hash)
    open(dump_file_path, 'w').write(json.dumps((extractions)))
    return dump_file_path


def strip_blacklist(doc):
    # Doc is a BeautifulSoup object
    blacklist = ['script', 'pre', 'code', 'title', 'style']

    for tag in blacklist:
        elements = doc.find_all(tag)
        map(lambda x: x.decompose(), elements)

    return doc


def process_html(doc):
    # Take HTML input and output pre-processed text content
    soup = BeautifulSoup(doc)
    soup = strip_blacklist(soup)
    return soup.text


def process_url(url):
    req = requests.get('http://' + url)
    a = process_html(req.text)
    extracted = ExtractorClient().extract(str(a.encode('utf-8')))
    return store_extractions(url, extracted)
