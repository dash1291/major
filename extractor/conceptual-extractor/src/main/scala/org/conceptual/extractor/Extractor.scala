package org.conceptual.extractor

import collection.mutable.MutableList

import edu.arizona.sista.processors.Processor
import edu.arizona.sista.processors.CorefMention
import edu.arizona.sista.processors.corenlp.CoreNLPProcessor

import edu.knowitall.ollie.Ollie
import edu.knowitall.tool.parse.MaltParser
import scala.io.Source
import edu.knowitall.ollie.confidence.OllieConfidenceFunction


class Coreference(repr:String, ref:String, sentence_index:Int) {
    var representative:String = repr
    var coref:String = ref
    var sentence:Int = sentence_index

    override def toString():String = "(" + representative + ", " + coref + ")"
}

object CorefResolver {
    var proc:Processor = new CoreNLPProcessor(internStrings = false)

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

    def resolve(docString: String):MutableList[Coreference] = {
        var doc = proc.annotate(docString)
        var corefs = new MutableList[Coreference]

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
                        corefs += new Coreference(repr, text, mention.sentenceIndex)
                    }
                    i = i + 1
                }
                repr = ""
                text = ""
                i = 0
            }
        })

        return corefs
    }

}

object Extractor extends App {
    // Get corefs into an iterable
    // Extract OLLIE tripples, and replace with references
    // return the replaced triples
    println(CorefResolver.resolve("Joe Doe is a passionate nerd. He also likes football."))
    //var parser = new MaltParser
    //var ol = new Ollie
}
