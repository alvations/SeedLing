import os

def install_wpdownload():
    os.system("sudo pip install progressbar wp-download")
    os.system("wget -O wpdl.cfg http://pastebin.com/raw.php?i=UbAyiGR9")

def download_wiki(wiki_dir):
    os.system("wp-download -c wpdl.cfg "+wiki_dir)

def extract_dump(wikidump, extracted_dir):
    os.system("python wikiextractor.py "+wikidump+" -b 500K -o "+extracted_dir)
    
def extract_all_wiki(wiki_dir, extracted_dir):
    dumps = [os.path.join(root, name)
                 for root, dirs, files in os.walk(path)
                 for name in files
                 if name.endswith(("articles.xml.bz2"))]
    for dump in dumps:
        extract_dump(dump, extracted_dir)
    
def main(indir):
    wiki_dir = indir+"/raw_wikidumps/"
    extracted_dir = indir+"/extracted_wikis/"
    os.system('mkdir '+wiki_dir)
    os.system('mkdir '+extracted_dir)
    install_wpdownload()
    download_wiki(wiki_dir)
    extract_all_wiki(wiki_dir, extracted_dir)
    ## run cleaner.
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python %s wiki_directory \n' % sys.argv[0])
        sys.exit(1)
    if os.path.exists(sys.argv[1]):
        main(sys.argv[1])