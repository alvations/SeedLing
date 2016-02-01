# -*- coding: utf-8 -*-

import cPickle as pickle
from collections import defaultdict

import udhr, omniglot, odin, wikipedia
from counting import count_living_languages, pseudo_ethnologue, sil


def retrieve_endangerment_level(livinglanguages):
  endangerment_languages = defaultdict(list)
  for i in livinglanguages:
    if i in ["nob","nno"]: i = "nor"
    endangerment_level = pseudo_ethnologue[i][0][-1].split()[0]
    endangerment_languages[endangerment_level].append(i)
  return endangerment_languages

livinglanguages_in_seedling = set()

for resource in ['udhr', 'omniglot', 'odin', 'wikipedia']:
  _, livinglanguages = count_living_languages(resource)
  livinglanguages_in_seedling.update(livinglanguages)
  endangerment_languages = retrieve_endangerment_level(livinglanguages)
  print resource
  for endangerment, languages in sorted(endangerment_languages.iteritems()):
    print endangerment+"\t"+str(len(languages))
  print

print "Combined"
endangerment_languages = retrieve_endangerment_level(livinglanguages_in_seedling)
for endangerment, languages in sorted(endangerment_languages.iteritems()):
  print endangerment+"\t"+str(len(languages))
print
