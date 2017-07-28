#!/bin/python
import subprocess
import sys
import os
import pdb
from sklearn.feature_extraction.text import TfidfVectorizer
from binaryornot.check import is_binary

file_to_compare = sys.argv[2]
opened_file_to_compare = open(file_to_compare)
str_to_compare = opened_file_to_compare.read()

scorelist = []
the_folder = sys.argv[1]

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
        opened = [str_to_compare, str_f]
        tfidvec = TfidfVectorizer().fit_transform(opened)
        similarity = tfidvec * tfidvec.T
        scorelist.append([filename, similarity[0,1]])
      except UnicodeDecodeError:
        print "nonstandard binary file found", filename

walk_folder(the_folder)

def getKey(pair1):
  return 0 - pair1[1]

sorted_scorelist = sorted(scorelist, key=getKey)

print sorted_scorelist
