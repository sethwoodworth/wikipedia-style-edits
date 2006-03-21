#!/bin/sh
cd java-based-opennlp-wrapper
export CLASSPATH=.:needed-jars/maxent-2.4.0.jar:needed-jars/opennlp-tools-1.3.0.jar:needed-jars/resolver.jar:needed-jars/xercesImpl.jar:needed-jars/xercesSamples.jar:needed-jars/xml-apis.jar:needed-jars/xml-writer.jar:needed-jars/trove.jar
exec /usr/java/jdk/bin/java -Xmx1g -Dorg.xml.sax.driver=org.apache.xerces.parsers.SAXParser DataProcessor EnglishSD.bin.gz
