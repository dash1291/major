package org.conceptual.extractor

import edu.arizona.sista.processors.Processor
import edu.arizona.sista.processors.corenlp.CoreNLPProcessor


class CorefResolver() {
    var proc:Processor = new CoreNLPProcessor(internStrings = false)

    def resolve(docString: String) = {
        var doc = proc.annotate(docString)

        doc.coreferenceChains.foreach(chains => {
            for (chain <- chains.getChains) {
                println("Found one coreference chain containing the following mentions:")
                for (mention <- chain) {
                    // note that all these offsets start at 0 too
                    println("\tsentenceIndex:" + mention.sentenceIndex +
                    " headIndex:" + mention.headIndex +
                    " startTokenOffset:" + mention.startOffset +
                    " endTokenOffset:" + mention.endOffset +
                    " text: " + doc.sentences(mention.sentenceIndex).words.slice(mention.startOffset, mention.endOffset).mkString("[", " ", "]"))
                }
            }
        })
    }

}

object Extractor {
    def main(args:Array[String]) {
        var coref = new CorefResolver
        coref.resolve("He is crazy.")
    }
}
