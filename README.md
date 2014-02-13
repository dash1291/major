# Setup


## Python Environment


The instructions assume that Python (with setuptools) has been installed on the system.

* Install virtualenv using following commands:

``pip install virtualenv``

``curl -s https://raw.github.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL``

* Create virtual environment

``mkvirtualenv conceptual``

* Install Python dependencies

``pip install flask py2neo``


## Neo4j Installation


Download version specific to your OS from this website: http://www.neo4j.org/

## Extractor Service


The extractor service responsible for relationship extraction is built in Scala and requires scala and maven to be installed for building it from source.

Use the following command inside `extractor/conceptual-extractor` directory to build the service:

``mvn clean compile exec:java -Dexec.mainClass=org.conceptual.extractor.ExtractorService``

If ``OutOfMemory`` exception is thrown while building set environment variable ``MAVEN_OPTS=-Xmx2g``.


## Web Server


* Starting the web server

``python api/app.py``
