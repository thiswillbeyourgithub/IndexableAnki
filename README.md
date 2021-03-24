# IndexableAnki
Turn each card of an anki collection into txt files that can be searched using a desktop search engine like [Recoll](https://www.lesbonscomptes.com/recoll/) or Docfetcher etc. 

## Please read:
* **Why did I make this?** I wanted to make my anki databases searchable though [Recoll](https://www.lesbonscomptes.com/recoll/) or Docfetcher (those are desktop search engines).
* **What do you think of issues and contributions?** They are more than welcome, even just for typos, don't hesitate to open an issue.
* **Will this change my collection?** No, it makes a copy before hand and doesn't change a thing.
* **What version of python should I use?** It has been tested on Python 3.9
* **I'd like to index my rss reader into recoll, is it possible?** I created just that [over there](https://github.com/thiswillbeyourgithub/IndexableNewsboat)
* **How does it work?** It finds your database, copies it inside /tmp (otherwise it might be locked), loads it into pandas, drops useless columns,finds the deck name and add it to each line, saves each card as a .txt file, zips all the txt files together, moves the zip in the desired folder, deletes the txt files and the temporary db.
* **Is it cross platform?** Currently no, only Linux, and OSX could maybe work quite easily. It's on the todo list but don't be afraid to ask if you think you need this.

## TODO:
* switch to ankipandas instead of doing it on your own, it seems way easier
* make it OS agnostic, so far it can only work on linux and possibly OSX

## Usage:
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

## How do cards look like afterwards?
Here's an example card :

```
ANKI EXPORT AS TXT
card id: 15359932XXXXX
tags: physics::something
deck: Some::TAG::Thingie
sfld: [content of the sort field]
flds: [content of all fields (with a little text processing though]
```
