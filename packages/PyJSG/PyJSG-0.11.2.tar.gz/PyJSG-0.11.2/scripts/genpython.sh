#!/usr/bin/env bash
# Note: need antlr4.8 or later to run this!
# see: http://www.antlr.org/download.html for details
# Note: The output path follows the input path, so we need
#       to make a local copy if we want the output in the
#       parser directory
cp ../grammar/jsg*.g4 .
antlr4 -Dlanguage=Python3 -package parser -o ../pyjsg/parser -no-listener -visitor  jsgParser.g4 jsgLexer.g4
rm jsg*.g4
