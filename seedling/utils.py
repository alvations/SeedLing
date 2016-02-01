# -*- coding: utf-8 -*-

def sync_and_read(url, filename, toupdate=True):
  """ 
  Downloads and update a file from the given url, 
  if internet is available. 
  """
  if toupdate==False:
    return open(filename, 'r').read()
  import urllib2
  try: # Getting an updated version of the file online.
    infile = urllib2.urlopen(url).read().decode('utf8')
    with open(filename,'w') as fout:
      fout.write(infile.encode('utf-8'))
  except urllib2.URLError:
    infile = open(filename, 'r').read()
  return infile

def parentdirectory():
  """ Returns parent directory. """
  import os
  return os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                      os.path.pardir))

def currentdirectory():
  """ Returns current directory. """
  import os
  return os.path.dirname(os.path.realpath(__file__))

def make_tarfile(output_filename, source_dir):
  """ Compress all files into a single tarfile. """
  import os, tarfile
  with tarfile.open(output_filename, "w") as tar:
    tar.add(source_dir, arcname=os.path.basename(source_dir))

def read_tarfile(intarfile):
  """ Extracts a tarfile to a temp directory, then yield one file at a time. """
  import tempfile, tarfile, os
  TEMP_DIR = tempfile.mkdtemp()
  with tarfile.open(intarfile) as tf:
    for member in tf.getmembers():
      tf.extract(member, TEMP_DIR)
  
  for infile in os.listdir(TEMP_DIR):
    yield TEMP_DIR+'/'+infile

def remove_tags(text):
  """ Removes <tags> in angled brackets from text. """
  import re
  tags = {i:" " for i in re.findall("(<[^>\n]*>)",text.strip())}
  no_tag_text = reduce(lambda x, kv:x.replace(*kv), tags.iteritems(), text)
  return " ".join(no_tag_text.split())
