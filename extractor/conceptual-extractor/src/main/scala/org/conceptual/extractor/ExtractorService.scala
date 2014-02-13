package org.conceptual.extractor

import org.zeromq.ZMQ
import org.zeromq.ZMQQueue


object ExtractorService {
    println("Intializing CoreNLP and OLLIE")
    var extractor = new Extractor

    def main(args:Array[String]) {
        launchServer(8080)
    }

    def launchServer(port:Int) {
        val context = ZMQ.context(1)
        val clients = context.socket(ZMQ.ROUTER)
        clients.bind("tcp://0.0.0.0:" + port)

        val workers = context.socket(ZMQ.DEALER)
        workers.bind("inproc://workers")

        for (thread_nbr <- 1 to 5)  {
            val worker_routine = new Thread(){
                override def run(){
                    val socket = context.socket(ZMQ.REP)
                    socket.connect("inproc://workers")

                    while (true) {
                        val str = new String(socket.recv(0))
                        println(str)
                        var exts = extractor.extract(str)
                        socket.send(exts.toString(), 0)
                    }
                }
            }
            worker_routine.start()
        }
        //  Connect work threads to client threads via a queue
        val zMQQueue = new ZMQQueue(context, clients, workers)
        println("Listening on port " + port)
        zMQQueue run
    }
}
