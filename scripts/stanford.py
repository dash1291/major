import subprocess
import xml.dom.minidom as xmldom


def parse_output(output):
    dom = xmldom.parse(output)
    coref_list = []
    corefs = dom.getElementsByTagName('coreference')[0]
    for coref in corefs.getElementsByTagName('coreference'):
        representative = None
        for mention in coref.getElementsByTagName('mention'):
            if mention.getAttribute('representative') == 'true':
                representative = mention.getElementsByTagName('text')[0].childNodes[0].data
            else:
                name = mention.getElementsByTagName('text')[0].childNodes[0].data
                sent = mention.getElementsByTagName('sentence')[0].childNodes[0].data
                coref_list.append((str(name).lower(), str(representative).lower(), int(sent)))

    return coref_list


def call_stanford(input_file):
    path = '../stanford-corenlp-full-2013-11-12'
    jars = '%s/stanford-corenlp-3.3.0.jar:%s/stanford-corenlp-3.3.0-models.jar' % (path, path)
    jars += ':%s/xom.jar:%s/joda-time.jar:%s/jollyday.jar' % (path, path, path)
    annots = 'tokenize,ssplit,pos,lemma,ner,parse,dcoref'
    cmd = 'java -cp %s -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators %s -file %s' % (
        jars, annots, input_file)
    subprocess.call(cmd.split(' '))


def get_corefs(input_file):
    call_stanford(input_file)
    return parse_output(input_file.split('/')[-1] + '.xml')
