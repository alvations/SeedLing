# -*- coding: utf-8 -*-

import codecs, os, subprocess, sys, re, tempfile
import bz2

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), \
             os.path.pardir))
sys.path.append(parentddir)
from utils import make_tarfile
from wikicodes import WIKI2ISO

try:
  from bs4 import BeautifulSoup
except: # TODO: Installation of BeautifulSoup 4 necessary?
  from BeautifulSoup import BeautifulSoup 


def extract_wikipedia(WIKIDUMP_DIR):
  run_wikiextractor(WIKIDUMP_DIR, WIKITEXTS_DIR='../data/wikipedia/texts/')
  print('Wikipedia texts are extracted.')
  clean_wikipedia('../data/wikipedia/texts/')
  print('Wikipedia is cleaned.')


def run_wikiextractor(WIKIDUMP_DIR, WIKITEXTS_DIR, filesize = "5000K"):
  '''
  Extract all documents (articles) from wikipedia dumps (in WIKIDUMP_DIR)
  '''
  WIKIEXTRACTOR_DIR = '../'
  if not os.path.exists('../data/wikipedia/texts/'):
    os.makedirs('../data/wikipedia/texts/')

  for root, dirnames, filenames in os.walk(WIKIDUMP_DIR):
    for filename in filenames:
      print('extracting ' + filename)
      filepath = os.path.join(root, filename)
      # run WikiExtractor
      process = subprocess.Popen('bzcat ' + filepath + ' | python ' 
                        + WIKIEXTRACTOR_DIR + 'WikiExtractor.py -cb ' + filesize + ' -o '
                        + WIKITEXTS_DIR + filename , stdout=subprocess.PIPE, 
                                                                   shell=True)
      outputRaw, error = process.communicate()


def clean(s):
    '''Clean a string taken from Wikipedia texts.'''
    # disallow for wikipedia magic words
    # (http://en.wikipedia.org/wiki/Help:Magic_words)
    s = re.sub('__[A-Z]+__', '', s)
    
    # delete all square backets along wiht their content          
    s = re.sub(' ?\[.*?\]', '', s)

    # delete parentheses that contain no letters           
    s = re.sub(' ?\([\s,;"#\']*?\)', '', s)

    # clean: (, ; 4 ш. до н.э. - 26-36 н.э.) 
    s = re.sub('\([\s,;]+','(', s)

    # delete codice_13, etc.       
    #s = re.sub ('[Cc]odice_\d+', '', s)
    
    # delete formula_1, etc.  
    #s = re.sub ('[Ff]ormula_\d+', '', s)

    # delete newlines     
    s = re.sub('\n+', '\n', s)               
    return s



def get_iso(filepath):
    '''
    Extract language code from filepath and convert it into iso-6393 language code.
    Return the iso code. Return None if the language code can not be mapped into ISO.
    '''
    language = re.search('\/([\w]+)wiki-', filepath).group(1)
    try:
        isolanguage = WIKI2ISO[language]
        #isolanguage = wikicode2iso(language)
    except KeyError:
          isolanguage = None
    if isolanguage == None:
          print('Skip language ' + language + ': could not be converted into ISO.')
    return isolanguage



def clean_wikipedia(wiki_raw_dir, option = "firstfile"):
    '''
    Clean all files in wiki_raw_dir and write clean files into
    data/wikipedia/clean/ .
    Options:
    - firstfile: cleans and stores only one folder (AA) per language. For 
      "normal" WikiExtractor setting, this corresponds to 100 files with
      5000K each. Currently this means, that for the 20 most frequent
      languages (see http://meta.wikimedia.org/wiki/List_of_Wikipedias), part
      of the data is ignored.
    - all: cleans and stores all folders 
    '''
    c = 1
    skippedcount = 1

    if not os.path.exists(wiki_raw_dir):
        print('no such path:' + wiki_raw_dir)

    if not os.path.exists('data/wikipedia/'):
        os.makedirs('data/wikipedia/')

    WIKIPEDIA_CLEAN_DIR = 'data/wikipedia/clean/'
    TEMP_WIKIPEDIA_CLEAN_DIR = tempfile.mkdtemp()

    for root, dirnames, filenames in os.walk(wiki_raw_dir):
        for filename in filenames:
          filepath = os.path.join(root, filename)

          # get number for language file and in case of option=firstfile
          # skip all files that are not in a AA folder
          count = re.search('wiki_([\d]+).bz2', filepath).group(1)
          if option == "firstfile" and not 'AA/wiki' in filepath:
              if count == '00' and 'AB/wiki' in filepath:
                  print('[option=firstfile] More files available ' + str(skippedcount) + ': ' + filepath)
                  skippedcount += 1
              continue
          
          language = get_iso(filepath)
          if language == None:
              continue            
  
          if not os.path.exists('data/wikipedia/clean/' + language):
              os.makedirs('data/wikipedia/clean/' + language)

          print('cleaning file ' + str(c) + ': ' + filepath)
          c += 1
          with bz2.BZ2File(filepath, 'r') as openZip:
              f = openZip.read()
              
              # closing ref tags without a corresponding opening tag are a 
              # problem for BeautifulSoup3
              #uni_f = re.sub('</[^d]+.*?>', '', f)
              #uni_f = re.sub('</br', '', uni_f)
              
              uni_f = re.sub('<!\[', '', f)
              soup = BeautifulSoup('<docs>' + uni_f + '</docs>')
              doclist = soup.findAll('doc')

          with codecs.open(TEMP_WIKIPEDIA_CLEAN_DIR + '/' + language + '_'
                               + str(count), 'a', 'utf-8') as out:

              for doc in doclist:
                  content = doc.getText()
                  cleancontent = clean(content.strip())
                  out.write(cleancontent.strip() + '\n')

              make_tarfile(WIKIPEDIA_CLEAN_DIR + language + '/' + language 
                  + '_' + str(count) + '.tar', TEMP_WIKIPEDIA_CLEAN_DIR + '/'
                  + language + '_' + str(count))



#extract_wikipedia('/media/ec609cb5-510c-467e-9655-5e72e99c4153/wikidumps/')
#clean_wikipedia('../data/wikipedia/texts/')
clean_wikipedia('/media/susanne/ec609cb5-510c-467e-9655-5e72e99c4153/sugali_wikipedia/resttexts/')

def source_sents(cleanedwikidir=parentddir+"/data/wikipedia/clean/"):
  """
  USAGE:
  >>> cleanwiki = '/media/alvas/E418A6B618A686E0/xling/cleanedwiki/'
  >>> for i in source_sent(cleanwiki):
  >>>   print i
  
  NOTE:
  cleanwiki should be a main directory that contains one directory for each
  language. And every language directory should contain at least one tarballs. 
  Regardless of how many files each tarballs contain, it extracts the lines.
  
  P/S: I know the nest directory pathing is ugly, but i can't find a simpler
  way to do this =) 
  """
  from utils import read_tarfile
  for lang in os.listdir(cleanedwikidir):
    for intarfile in os.listdir(cleanedwikidir+lang):
      for infile in read_tarfile(cleanedwikidir+lang+"/"+intarfile):
        with codecs.open(infile,'r','utf8') as fin:
          for line in fin:
            yield lang, line.strip()
'''
for i,j in source_sents():
  print i,j
'''

def languages():
  langs_in_wiki = ['lat', 'gag', 'cor', 'cre', 'lit', 'ven', 'mri', 'nau', 
                   'bos', 'arz', 'tha', 'yor', 'tet', 'yid', 'ssw', 'wln', 
                   'diq', 'krc', 'nrm', 'ndo', 'urd', 'pnt', 'isl', 'ori', 
                   'pan', 'kaz', 'kab', 'fra', 'bis', 'sin', 'msa', 'ces', 
                   'cbk', 'mah', 'nor', 'mlt', 'smo', 'new', 'kik', 'frp', 
                   'kor', 'ell', 'spa', 'vol', 'ibo', 'mya', 'ita', 'tsn', 
                   'sah', 'mzn', 'tuk', 'hun', 'dzo', 'tel', 'sun', 'tah', 
                   'lug', 'ile', 'est', 'bel', 'ido', 'vls', 'nso', 'lao', 
                   'orm', 'vec', 'mlg', 'ltg', 'vie', 'iii', 'cos', 'mus',
                    'oci', 'heb', 'ton', 'deu', 'fur', 'zha', 'chu', 'tat', 
                    'min', 'mkd', 'roh', 'amh', 'fry', 'nld', 'bug', 'gle', 
                    'yue', 'pus', 'ace', 'bod', 'lmo', 'srp', 'chy', 'lbe', 
                    'tyv', 'nep', 'pcd', 'lzh', 'jav', 'run', 'aze', 'grn', 
                    'ben', 'mhr', 'jbo', 'kau', 'sgs', 'lez', 'ltz', 'hye', 
                    'kur', 'slv', 'kas', 'tam', 'nov', 'dsb', 'kon', 'lav', 
                    'koi', 'bul', 'nya', 'bxr', 'ina', 'kal', 'wol', 'wuu', 
                    'sco', 'slk', 'nds', 'sag', 'pol', 'ava', 'nan', 'gsw', 
                    'fin', 'dan', 'xho', 'pfl', 'mar', 'ukr', 'snd', 'nap', 
                    'oss', 'vro', 'her', 'cdo', 'uzb', 'lin', 'ewe', 'nno', 
                    'tgk', 'hat', 'xal', 'scn', 'kua', 'hif', 'hmo', 'kom', 
                    'glv', 'mdf', 'uig', 'por', 'ang', 'lim', 'kbd', 'som', 
                    'cho', 'che', 'sot', 'fas', 'cym', 'mon', 'tpi', 'myv', 
                    'pih', 'xmf', 'srn', 'rus', 'pdc', 'rue', 'hak', 'eng', 
                    'ext', 'hau', 'swa', 'got', 'bam', 'tum', 'kin', 'nav', 
                    'fao', 'hrv', 'asm', 'aar', 'crh', 'fij', 'bpy', 'bar', 
                    'ara', 'udm', 'bak', 'zul', 'pap', 'csb', 'aka', 'haw', 
                    'sme', 'zea', 'gla', 'stq', 'tgl', 'mal', 'swe', 'tir', 
                    'afr', 'ckb', 'ksh', 'vep', 'kir', 'rup', 'ful', 'pnb', 
                    'jpn', 'bjn', 'zho', 'abk', 'frr', 'kaa', 'eus', 'ilo', 
                    'bre', 'que', 'pms', 'cha', 'rmy', 'aym', 'szl', 'pam', 
                    'arg', 'hbs', 'pag', 'iku', 'kat', 'cat', 'ron', 'khm', 
                    'sqi', 'san', 'ipk', 'glk', 'jv', 'tur', 'lad', 'ceb', 
                    'mwl', 'glg', 'twi', 'war', 'mrj', 'ast', 'epo', 'pli', 
                    'div', 'kan', 'sna', 'tso', 'chr', 'hsb', 'srd', 'lij', 
                    'bcl', 'chv', 'hin', 'arc', 'ind', 'guj', 'gan']
  return langs_in_wiki
