# -*- coding: utf-8 -*-

# Access modules from parent dir, see http://goo.gl/dZ5HVk
import os, codecs, tempfile
from utils import read_tarfile, currentdirectory

def enumerate_udhr(intarfile):
  """
  Returns the number of languages in a defaultdict(list). If language(s) has
  dialects/registers in the UDHR, len(enumerate_udhr(intarfile)[lang]) > 1 .
  
  # USAGE:
  >>> ls = enumerate_udhr('../data/udhr/udhr-unicode.tar')
  >>> for i in sorted(ls):
  >>>   print i, ls[i]
  >>> print len(ls) # Number of languages
  """
  from collections import defaultdict
  import tarfile
  TEMP_DIR = tempfile.mkdtemp()
  # Reads the tarfile and extract to temp directory.
  with tarfile.open(intarfile) as tf:
    for member in tf.getmembers():
      tf.extract(member, TEMP_DIR)
  languages = defaultdict(list)
  # Loop through temp directory.
  for infile in os.listdir(TEMP_DIR):
    lang = infile.partition('.')[0].lower()
    try:
      lang, dialect = lang.split('_') # Checks for dialects denoted by "_".
      languages[lang].append(dialect)
    except:
      languages[lang].append(lang)
  return languages

def documents(intarfile=currentdirectory()+'/data/udhr/udhr-unicode.tar', \
              bysentence=False):
  """ Yields UDHR by documents. """
  for infile in read_tarfile(intarfile):
    #language = infile.split('/')[-1][:3]
    language = infile.split('/')[-1].split('-')[1].split('.')[0].split('_')[0]
    with codecs.open(infile,'r','utf8') as fin:
      if bysentence:
        for sentence in fin.readlines():
          if sentence:
            yield language, sentence.strip()
      else:
        yield language, fin.read()
        
def sents(intarfile=currentdirectory()+'/data/udhr/udhr-unicode.tar', \
          bysentence=True):
  return documents(intarfile, bysentence)

def source_sents(intarfile=currentdirectory()+'/data/udhr/udhr-unicode.tar', \
                 bysentence=True):
  return sents(intarfile, bysentence)

def languages():
  """ Returns a list of available languages from original data source. """
  langs = [i.partition('-')[2].partition('.')[0] for i in \
           enumerate_udhr(intarfile=currentdirectory()+ \
                          '/data/udhr/udhr-unicode.tar')]
  return langs

def num_languages():
  """ Returns the number of languages available from original data source. """
  return len(languages())

''''# USAGE:
print languages()
print num_languages()
for lang, sent in source_sents():
  print lang, sent
'''