#!/bin/sh
cd opennlp/opennlp-tools-1.3.0
export CLASSPATH=output/opennlp-tools-1.3.0.jar:lib/maxent-2.4.0.jar:lib/trove.jar:lib/jwnl-1.3.3.jar
exec java opennlp.tools.lang.english.SentenceDetector EnglishSD.bin.gz
