# -*- coding: utf-8 -*-

from collections import defaultdict
from utils import sync_and_read, currentdirectory


class MiniWALS(dict):
  def __init__(self, toupdate=True):
    WALS_URL = "http://wals.info/languoid.tab?sEcho=1&iSortingCols=1"+\
            "&iSortCol_0=0&sSortDir_0=asc"
    WALS_TXT = currentdirectory()+"/data/wals/wals.txt"
                
    wals_tsv = sync_and_read(WALS_URL, WALS_TXT, toupdate=toupdate)
    headerline, _ , data = wals_tsv.partition('\n')
    
    for line in data.split('\n'):
      lang = line.split()[0]
      for key, value in zip(headerline.split('\t')[1:], line.split('\t')[1:]):
        self.setdefault(lang,{})[key] = value

    self.GENUS = defaultdict(list)
    for lang in self:
      self.GENUS[self[lang]['genus']].append(lang)

    self.LANGUAGEFAMILY = defaultdict(list)
    for lang in self:
      self.LANGUAGEFAMILY[self[lang]['family']].append(lang)
    
    self.RELATED_LANGS = defaultdict(list)
    for lang in self:
      self.RELATED_LANGS[lang] = self.GENUS[self[lang]['genus']] + \
                                self.LANGUAGEFAMILY[self[lang]['family']]

'''# USAGE:
wals = MiniWALS()
print wals['eng']
print sorted(wals.LANGUAGEFAMILY.keys())
print wals.LANGUAGEFAMILY['Indo-European']
print wals.GENUS['Germanic']
print sorted(wals.RELATED_LANGS['eng'])
'''