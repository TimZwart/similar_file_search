# Similarity search tool

## purpose

given a file, find files similar to this file

## Setup

make sure /bin/python links to your python and install the dependencies.

##usage

```
/path/to/SimilarFiles.py <directory> <file>
```

directory is the directory you want to look for similar files
file is the file used for comparison

redirect the output to less for best results if you are scanning a lot of files

##output

an array consisting of entries like ["filename", similarity\_score] sorted by similarity score and the time it took to run

## issues

- only tested on windows subsystem for linux (ubuntu)
- could not get it to run on cygwin
- unknown whether it will work on other systems
- not fully tested yet

## dependencies

- python 2.x
- scipy
- numpy
- scikit-learn

## optional arguments

adding a third argument 'difflib' makes it use the difflib library instead. this is not recommended because this does not produce a reasonable similarity. 

```
/path/to/SimilarFiles.py <directory> <file> difflib

```
