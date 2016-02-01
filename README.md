SeedLing
========

Building and using a seed corpus for the *Human Language Project* (Steven and Abney, 2010).

The SeedLing corpus on this repository includes the data from:
*  **ODIN**: Online Database of Interlinear Text 
*  **Omniglot**: Useful foreign phrases from www.omniglot.com
*  **UDHR**: Universal Declaration of Human Rights

The SeedLing API includes scripts to access data/information from:
* **SeedLing**: different data sources that forms the SeedLing corpus (`odin.py`, `omniglot.py`, `udhr.py`, `wikipedia.py`)
* **WALS**: Language information from World Atlas of Language Structures (`miniwals.py`)

**FAQs**:

- To use the SeedLing corpus through the python API, please follow the instructions on the **Usage** section.
- To download the plaintext version of the SeedLing corpus (excluding wikipedia data), click here: https://db.tt/N7hV3gwW.
- To download the wikipedia data, please follow the **Getting Wikipedia** section.


***
Usage
=====

To access the SeedLing from various data sources:

```
from seedling import udhr, omniglot, odin

# Accessing ODIN IGTs:
>>> for lang, igts in odin.igts():
>>>   for igt in igts:
>>>     print lang, igt

# Accesing Omniglot phrases
>>> for lang, sent, trans in omniglot.phrases():
>>>   print lang, sent, trans

# Accessing UDHR sentences.
>>> for lang, sent in udhr.sents():
>>>   print lang, sent
```

To access the SIL and WALS information:

```
from seedling import miniwals

# Accessing WALS information
>>> wals = miniwals.MiniWALS()
>>> print wals['eng']
{u'glottocode': u'stan1293', u'name': u'English', u'family': u'Indo-European', u'longitude': u'0.0', u'sample 200': u'True', u'latitude': u'52.0', u'genus': u'Germanic', u'macroarea': u'Eurasia', u'sample 100': u'True'}
```

Detailed usage of the API can also be found in `demo.py`.


***
Getting Wikipedia
====

There are two ways to access the Wikipedia data:
 1. Plant your own Wiki
 2. Access it from our cloud storage


Plant your own Wiki
----

We encourage SeedLing users to take part in building the Wikipedia data from the SeedLing corpus. A fruitful experience, you will find.

Please **ENSURE** that you have sufficient space on your harddisk (~50-70GB) and also this process of download and cleaning might take up to a week for **ALL** languages available in Wikipedia. 

**For the lazy**: run the script `plant_wiki.py` and it would produce the desired cleaned plaintext Wikipedia data as presented in the SeedLing publication:

```
$ python plant_wiki.py &
```


For more detailed, step-by-step instructions:

 - First, you have to download the Wikipedia dumps. We have used the `wp-download` (https://github.com/babilen/wp-download) tool when building the SeedLing corpus. 
 - Then, you have to extract the text from the Wikipedia dumps. We used the `Wikipedia Extractor` (http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) to convert wikipedia dumps into textfiles.
 - Finally, you can use the cleaning function in `wikipedia.py` to clean the Wikipedia data and assigns the ISO 639-3 language code to textfiles. The cleaning function can be called as such:

```
import codecs
from seedling.wikipedia import clean

extracted_wiki_dir = "/home/yourusername/path/to/extracted/wiki/"
cleaned_wiki_dir = "/home/yourusername/path/to/cleaned/wiki/"

for i in os.listdir(extracted_wiki_dir):
  dirpath, filename = os.path.split(i)
  with codecs.open(i, 'r', 'utf8') as fin, codecs.open(clean_wiki_dir+"/"+filename, 'w', 'utf8') as fout:
    fout.write(clean(fin.read()))
```

Please feel free to contact the colloborators in the SeedLing project if you encounter problems with getting the Wikipedia data.

Access it from our cloud storage
----

To be updated.

***
Cite
=====

To cite the SeedLing corpus:

Guy Emerson, Liling Tan, Susanne Fertmann, Alexis Palmer and Michaela Regneri . 2014. SeedLing: Building and using a seed corpus for the Human Language Project. In Proceedings of
*The use of Computational methods in the study of Endangered Languages (ComputEL) Workshop*. Baltimore, USA.

in `bibtex`:

```
@InProceedings{seedling2014,
  author    = {Guy Emerson, Liling Tan, Susanne Fertmann, Alexis Palmer and Michaela Regneri},
  title     = {SeedLing: Building and using a seed corpus for the Human Language Project},
  booktitle = {Proceedings of The use of Computational methods in the study of Endangered Languages (ComputEL) Workshop},
  month     = {June},
  year      = {2014},
  address   = {Baltimore, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {},
  url       = {}
}
```

***
References
====

 - Steven Abney and Steven Bird. 2010. The Human Language Project: Building a universal corpus of the world’s languages. In Proceedings of the 48th Annual Meeting of the Association for Computational Linguistics, pages 88–97. Association for Computational Linguistics.

 - Sime Ager. Omniglot - writing systems and languages of the world. Retrieved from www.omniglot.com.

 - William D Lewis and Fei Xia. 2010. Developing ODIN: A multilingual repository of annotated language data for hundreds of the world’s languages. Literary and Linguistic Computing, 25(3):303–319.

 - UN General Assembly, Universal Declaration of Human Rights, 10 December 1948, 217 A (III), available at: http://www.refworld.org/docid/3ae6b3712c.html [accessed 26 April 2014]

