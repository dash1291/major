from hashlib import md5
import json
import os
import re

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
    text = soup.text

    # Turn newlines into full-stops(.) to force sentence split
    text = re.sub('\n+', '.', text)
    text = re.sub('\'m', ' am', text)

    return text


def process_url(url):
    req = requests.get('http://' + url)
    a = process_html(req.text)
    extracted = ExtractorClient().extract(str(a.encode('utf-8')))
    break_edges(extracted)
    return store_extractions(url, extracted)


def break_edges(extractions):
    i1 = 0
    for extraction in extractions:
        obj1 = extraction[0]
        rel = extraction[1]
        obj2 = extraction[2]
        comb = rel + ' ' + obj2

        i2 = 0
        for extraction2 in extractions:
            if i1 == i2:
                i2 += 1
                continue

            if extraction2[0] == obj1 and comb in extraction2[1]:
                # Make the subject2 as subject1 of this extraction
                extraction2[0] = obj2

                # Strip the redundant part of the relation
                extraction2[1] = extraction2[1].replace(comb, '')
            i2 += 1

        i1 += 1
