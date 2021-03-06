package org.conceptual.extractor

import collection.mutable.MutableList

import edu.arizona.sista.processors.Document
import edu.arizona.sista.processors.Processor
import edu.arizona.sista.processors.CorefMention
import edu.arizona.sista.processors.corenlp.CoreNLPProcessor
import edu.knowitall.tool.sentence.OpenNlpSentencer

import edu.knowitall.ollie.Ollie
import edu.knowitall.tool.parse.MaltParser
import scala.io.Source
import edu.knowitall.ollie.confidence.OllieConfidenceFunction



// Coreference structure
class Coreference(repr:String, ref:String, sentence_index:Int) {
    // lowercase all this shit
    var representative:String = repr.toLowerCase
    var coref:String = ref.toLowerCase
    var sentence:Int = sentence_index

    override def toString():String = "(" + representative + ";" + coref + ";" + sentence + ")"
}


// Extraction structure
class Extraction(arg1Text:String, relText:String, arg2Text:String) {
    // lowercase all this shit
    var arg1:String = arg1Text.toLowerCase
    var rel:String = relText.toLowerCase
    var arg2:String = arg2Text.toLowerCase

    override def toString():String = "(" + arg1 + ";" + rel + ";" + arg2 + ")"
}


class ExtractionsList(extractions:Iterable[Extraction]) {
    override def toString:String = {
        var retVal = ""
        for (extraction <- extractions) {
            retVal += extraction.toString() + "\n"
        }
        return retVal
    }
}


class CorefResolver {
    var proc:Processor = new CoreNLPProcessor(internStrings = true)
    proc.annotate("Initialize this processor.")

    var corefs = new MutableList[Coreference]

    private def lessThanForMentions(x:CorefMention, y:CorefMention):Boolean = {
        if (x.sentenceIndex < y.sentenceIndex) return true
        if (x.sentenceIndex > y.sentenceIndex) return false

        if (x.headIndex < y.headIndex) return true
        if (x.headIndex > y.headIndex) return false

        val diffSize = (x.endOffset - x.startOffset) - (y.endOffset - y.startOffset)
        if (diffSize > 0) return true
        if (diffSize < 0) return false

        true
    }

    def resolve(docString: String):Document = {
        var doc = proc.annotate(docString)

        var i:Int = 0
        var text:String = ""
        var repr:String = ""

        doc.coreferenceChains.foreach(chains => {
            for (mentions <- chains.getChains) {
                for (mention <- mentions.toList.sortWith(lessThanForMentions)) {
                    text = doc.sentences(mention.sentenceIndex).words.slice(mention.startOffset, mention.endOffset).mkString("", " ", "")
                    if (i == 0) {
                        repr = text
                    } else {
                        if (repr != text) {
                            corefs += new Coreference(repr, text, mention.sentenceIndex)
                        }

                    }
                    i = i + 1
                }
                repr = ""
                text = ""
                i = 0
            }
        })
        return doc
    }
}


// Main extractor object
class Extractor {
    var corefResolver = new CorefResolver
    var parser = new MaltParser
    var ollie = new Ollie

    def isPronoun(str:String):Boolean = {
        var strL = str.toLowerCase
        if (strL == "it" || strL == "he" || strL == "she" || strL == "they" || strL == "its") {
            return true
        } else {
            return false
        }
    }

    // Method to be used for extraction.
    def extract(str:String):ExtractionsList = {
        // Extract coreferences
        var doc = corefResolver.resolve(str)
        var corefs = corefResolver.corefs

        // segment the text into sentences
        //var sentencer = new OpenNlpSentencer
        var sentences = doc.sentences

        // store sentence index
        // Here ollie triples are extracted and coreference are
        // replaced by there representative phrases.
        var ind = 1
        var extractions = new MutableList[Extraction]
        for (line <- sentences) {
            println(line)
            val parsed = parser.dependencyGraph(line.words.mkString(" "))
            val extractionInstances = ollie.extract(parsed)

            var repr = ""
            var arg1 = ""
            var arg2 = ""
            var rel = ""
            for (inst <- extractionInstances) {
                var skip = false

                arg1 = inst.extraction.arg1.text
                arg2 = inst.extraction.arg2.text
                rel = inst.extraction.rel.text

                for (coref <- corefs) {
                    repr = coref.representative

                    if (coref.sentence == ind) {
                        if (coref.coref == arg1) {
                            arg1 = repr
                        }

                        if (coref.coref == arg2) {
                            arg2 = repr
                        }
                    }
                }

                if (isPronoun(arg1) || isPronoun(arg2)) {
                    skip = true
                }

                if (!skip) {
                    extractions += new Extraction(arg1, rel, arg2)
                }
            }

            ind = ind + 1
        }

        return new ExtractionsList(extractions)
    }
}
