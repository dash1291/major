from django.conf import settings

import zmq


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
