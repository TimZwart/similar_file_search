#!/bin/python
import subprocess
import sys
import os
import pdb
from sklearn.feature_extraction.text import TfidfVectorizer
from binaryornot.check import is_binary
import time
import difflib
import argparse
import Levenshtein

start = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("directory", help="the directory to search")
parser.add_argument("file", help="the file to compare against")
parser.add_argument("--difflib", help="experimental: use difflib libarary instead", action="store_true")
parser.add_argument("--levenstein", help="experimental: use levenstein distance instead", action="store_true")
parser.add_argument("--runtime", help="show runtime", action="store_true")
arguments = parser.parse_args()
file_to_compare = arguments.file
opened_file_to_compare = open(file_to_compare)
str_to_compare = opened_file_to_compare.read()

scorelist = []
the_folder = arguments.directory

def walk_folder(folder):
  print "scanning folder", folder
  for (dirpath, dirnames, filenames) in os.walk(folder):
#    print "scanning folder", dirpath
#    print "files to scan", filenames
    for f in filenames:
      filename = "/".join([dirpath, f])
      if is_binary(filename):
        break
      try:
        opened = open(filename)
        str_f = opened.read()
        if arguments.difflib:
          matcher = difflib.SequenceMatcher(str_to_compare, str_f)
          scorelist.append([filename, matcher.ratio()])
        if arguments.levenstein:
          distance = Levenshtein.distance(str_to_compare, str_f)
          scorelist.append([filename, distance])
        else:
          opened = [str_to_compare, str_f]
          tfidvec = TfidfVectorizer().fit_transform(opened)
          similarity = tfidvec * tfidvec.T
          scorelist.append([filename, similarity[0,1]])
      except UnicodeDecodeError:
        print "nonstandard binary file found", filename

walk_folder(the_folder)

def getKey(pair1):
  return 0 - pair1[1]
def levenKey(pair1):
  return pair1[1]

def formatted_scorelist(scorelist):
  text = ""
  for entry in scorelist:
    line = entry[0] +": " + str(entry[1]) +"\n"
    text = text + line
  return text

if arguments.levenstein:
  keyfunc = levenKey
else:
  keyfunc = getKey

sorted_scorelist = sorted(scorelist, key=keyfunc)

print formatted_scorelist(sorted_scorelist)

end = time.time()
running_time = end - start

if arguments.runtime:
  print "time elapased", running_time
