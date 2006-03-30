#!/bin/sh
export LANG=en_US.UTF-8
export LC_CTYPE="en_US.UTF-8"
export LC_NUMERIC="en_US.UTF-8"
export LC_TIME="en_US.UTF-8"
export LC_COLLATE="en_US.UTF-8"
export LC_MONETARY="en_US.UTF-8"
export LC_MESSAGES="en_US.UTF-8"
export LC_PAPER="en_US.UTF-8"
export LC_NAME="en_US.UTF-8"
export LC_ADDRESS="en_US.UTF-8"
export LC_TELEPHONE="en_US.UTF-8"
export LC_MEASUREMENT="en_US.UTF-8"
export LC_IDENTIFICATION="en_US.UTF-8"
export LC_ALL=
cd java-based-opennlp-wrapper
export CLASSPATH=.:needed-jars/maxent-2.4.0.jar:needed-jars/opennlp-tools-1.3.0.jar:needed-jars/resolver.jar:needed-jars/xercesImpl.jar:needed-jars/xercesSamples.jar:needed-jars/xml-apis.jar:needed-jars/xml-writer.jar:needed-jars/trove.jar
exec ~/bin/java -Xmx1g -Dorg.xml.sax.driver=org.apache.xerces.parsers.SAXParser DataProcessor EnglishSD.bin.gz
