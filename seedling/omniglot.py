# -*- coding: utf-8 -*-

# Access modules from parent dir, see http://goo.gl/dZ5HVk
import codecs, tarfile
from utils import read_tarfile, currentdirectory

def phrases(intarfile=currentdirectory()+'/data/omniglot/omniglotphrases.tar', \
            onlysource=False):
  """ Yield source and tranlsation sentences from the clean Omniglot tarball. """
  for infile in read_tarfile(intarfile):
    language = infile.split('/')[-1].split('-')[1].split('.')[0].split('_')[0]
    with codecs.open(infile,'r','utf8') as fin:
      for line in fin.readlines():
        sentence, translation = line.strip().split('\t')
        if onlysource and sentence:
          yield language, sentence.strip()
        else:
          yield language, sentence, translation

def source_sents(intarfile=currentdirectory()+\
                 '/data/omniglot/omniglotphrases.tar', onlysource=True):
  """ Yield clean sentences from the clean Omniglot tarball. """
  return phrases(intarfile, onlysource)

def languages():
  """ Returns the number of languages available from original data source. """
  return [str(i.name).partition('-')[2].partition('.')[0] 
          for i in tarfile.open(currentdirectory()+ \
                                '/data/omniglot/omniglotphrases.tar') \
          if i.name != ""]

def num_languages():
  """ Returns the number of languages available from original data source. """
  return len(languages())

'''
# USAGE:
for lang, sent, trans in phrases():
  print lang, sent, trans
print languages
print num_languages()
'''