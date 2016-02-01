# -*- coding: utf-8 -*-

import cPickle as pickle
import codecs
from collections import defaultdict, Counter

import udhr, omniglot, odin, wikipedia
import miniwals, miniethnologue
from miniethnologue import check_lang

sil = miniethnologue.MiniSIL(toupdate=False)
pkfile = 'data/ethnologue/livinglanguages_with_info.pk'
pseudo_ethnologue = pickle.load(codecs.open(pkfile, 'rb'))

def count_iso_languages(resource):
  languages = globals()[resource].languages()
  languages_iso6393 = [i for i in languages if i in sil.ISO6393]
  return languages_iso6393

def languages_wo_constructed_but_in_ISO6393(resource):
  languages_in_resource = [i for i in globals()[resource].languages() \
                     if i in sil.ISO6393]
  
  # Substitute retired codes with the updated ones.
  languages_in_resource = [sil.ISO6393[i]['changeto'] if \
                    sil.ISO6393[i].get('retired') and 
                    sil.ISO6393[i]['changeto'] != ""\
                    else i \
                    for i in languages_in_resource]
  return list(set(languages_in_resource))

def count_num_tokens(resource):
  languages_in_resource = languages_wo_constructed_but_in_ISO6393(resource)
  num_tokens = 0
  for lang, sent in  globals()[resource].source_sents():
    if sil.ISO6393.get(lang):
      lang = sil.ISO6393.get(lang).get('changeto') if sil.ISO6393.get(lang).get('retired') and \
      sil.ISO6393.get(lang).get('changeto') != "" else lang
    if lang in languages_in_resource:
      print sent
      num_tokens+= sent.count(" ")+1
  return num_tokens

def count_living_languages(resource, shutup=False):
  languages = globals()[resource].languages()
  languages_iso6393 = [i for i in languages if i in sil.ISO6393]
  
  # Substitute retired codes with the updated ones.
  language_iso6393 = [sil.ISO6393[i]['changeto'] if \
                      sil.ISO6393[i].get('retired') and 
                      sil.ISO6393[i]['changeto'] != ""\
                      else i \
                      for i in languages_iso6393]
  
  num_in_ISO = len(languages_iso6393)
  
  num_constructed = [i for i in language_iso6393 if \
                     sil.ISO6393[i.split("_")[0]].get('type') == "Constructed"]
  
  for con in num_constructed:
    languages_iso6393.remove(con)
    
  num_in_iso_without_con = len(set(languages_iso6393))
  

  # Check why are languages not in ISO.
  not_in_ISO = {i:check_lang(i, option="Status") for i in \
                set(languages).difference(languages_iso6393)}
  
  livinglanguages = [i for i in languages_iso6393 if i in \
                     pseudo_ethnologue.keys()+['nno', 'nob']]
  
  # Check why are languages not living.
  not_living = {}
  for i in set(languages_iso6393).difference(livinglanguages):
    if i in sil.MACROLANGS:
      not_living[i] = "macro"
    else:
      langtype = check_lang(i, option="Type")
      if check_lang(i, option="Type") == '' and \
      check_lang(i, option="Status") == "retired":
        langtype = "retired"  
      not_living[i] = langtype
  
  
  languagefamilies = defaultdict(list)
  for i in livinglanguages:
    i = "nor" if i in ["nob","nno"] else i
    languagefamilies[pseudo_ethnologue[i][0][0]].append(i)
  
  if not shutup:
    print resource
    print "Original #Languages :", len(set(languages))
    print "#Languages in ISO:", num_in_ISO
    print "#Languages in ISO (w/o constructed)", num_in_iso_without_con
    if resource != "wikipedia":
      print "#Tokens for languages in ISO (w/o constructed)", count_num_tokens(resource)
    print "#LivingLanguages:", len(set(livinglanguages))
    print "#Families:", len(set(languagefamilies))
    print "Languages not in ISO because:", not_in_ISO
    print "Languages not living because:", not_living
    print
  return list(set(languages_iso6393)), list(set(livinglanguages))

def count_freqs(d):
  '''Counts freqs in a dictionary.'''
  countdic = dict()
  for key in d.keys():
    try:
      countdic[d[key]] += 1
    except KeyError:
      countdic[d[key]] = 1
  return countdic

def count_source_per_language(l):
    d = defaultdict(int)
    for lang in l:
        d[lang] += 1
    ##print(d)
    countdic = count_freqs(d)
    for key in countdic.keys():
      print('# of languages that appear in exactly ' + str(key) 
                            + ' datasource(s): ' + str(countdic[key]))

"""
def count_source_perlanguage2(ll):
  ll_numsources = Counter()
  for resource in ['udhr', 'omniglot', 'odin', 'wikipedia']:
    languages_in_resource = languages_wo_constructed_but_in_ISO6393(resource)
    for lang in set(languages_in_resource):
      if lang in ll:
        ll_numsources[lang] +=1
  
  numsources_ll = defaultdict(list)
  for ll, numsources in ll_numsources.iteritems():
    numsources_ll[numsources].append(ll)
  
  ##print numsources_ll
  
  for key in numsources_ll.keys():
    print('# of languages that appear in exactly ' + str(key) 
          + ' datasource(s): ' + str(len(numsources_ll[key])))
"""

######################################################################  

# USAGE:
livinglanguages_in_seedling = set()
languages_with_iso6393_in_seedling_without_constructed = set()
source_per_language = set()
source_per_living_language = set()

for resource in ['udhr', 'omniglot', 'odin', 'wikipedia']:
  languages_in_iso6393_without_constructed, \
  livivinglanguages_in_ethnologue = count_living_languages(resource)
  
  livinglanguages_in_seedling.update(livivinglanguages_in_ethnologue)
  languages_with_iso6393_in_seedling_without_constructed.update(languages_in_iso6393_without_constructed)
  
  source_per_language.update(languages_in_iso6393_without_constructed)
  source_per_living_language.update(livivinglanguages_in_ethnologue)

print "Combined #Languages:", len(languages_with_iso6393_in_seedling_without_constructed)
print("\nAll languages in ISO:")
#count_source_perlanguage2(languages_with_iso6393_in_seedling_without_constructed)
count_source_per_language(list(source_per_language))
print("\nLiving Languages:")
#count_source_perlanguage2(livinglanguages_in_seedling)
count_source_per_language(list(source_per_living_language))


