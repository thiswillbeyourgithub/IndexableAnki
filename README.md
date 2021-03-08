# IndexableAnki
Turn each card of an anki collection into easily searchable txt files. 

## Why ? 
I wanted to make my anki databases searchable though Recoll or Docfetcher (those are desktop search engines).

## Usage :
```
usage: IndexableAnki.py [-h] [-a ANKI_PATH] [-p ANKI_PROFILE] [-o output_PATH]
                        [-t TMP_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -a ANKI_PATH, --anki ANKI_PATH
                        The path to the anki folder(ex:
                        /home/USER/.local/share/Anki2/)
  -p ANKI_PROFILE, --profile ANKI_PROFILE
                        Name of the anki profile you want to make indexable
                        (ex: Main)
  -o output_PATH, --output output_PATH
                        Path to the directory that will contain the indexable
                        anki
  -t TMP_PATH, --temp-path TMP_PATH
                        Path where a temporary anki db will be stored (ex
                        /tmp/anki.db)
```

## Result :
example card :
```
ANKI EXPORT AS TXT
card id: 15359932XXXXX
tags: physics::something
deck: Some::TAG::Thingie
sfld: [content of the sort field]
flds: [content of all fields (with a little text processing though]
```
