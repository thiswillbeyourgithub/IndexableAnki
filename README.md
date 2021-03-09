# IndexableAnki
Turn each card of an anki collection into easily searchable txt files. 

## Please read :
* **Why did I make this?** I wanted to make my anki databases searchable though [Recoll](https://www.lesbonscomptes.com/recoll/) or Docfetcher (those are desktop search engines).
* **What do you think of issues and contributions?** They are more than welcome, even just for typos, don't hesitate to open an issue.
* **Will this change my collection?** No, it makes a copy before hand and doesn't change a thing.
* **What version of python should I use?** It has been tested on Python 3.9

## TODO :
* I think the text_processor() function is not currently vectorized and taking a lot of time. There are better ways to use regex matching on a pandas dataFrame that are probably much much faster.

## Usage :
    ` python3 ./IndexableAnki.py -a ~/.local/share/Anki2 -p Myprofile -o ~/Documents/ -t /tmp/anki.db`

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

## How do card look like afterwards?
Here's an example card :

```
ANKI EXPORT AS TXT
card id: 15359932XXXXX
tags: physics::something
deck: Some::TAG::Thingie
sfld: [content of the sort field]
flds: [content of all fields (with a little text processing though]
```
