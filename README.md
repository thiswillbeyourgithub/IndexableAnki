# IndexableAnki
Turn each card of an anki collection into txt files that can be searched using a desktop search engine like [Recoll](https://www.lesbonscomptes.com/recoll/) or Docfetcher etc. 

**Note: For a more powerful version, you can use [my sophisticated RAG lib, wdoc,](https://wdoc.readthedocs.io/en/stable) to parse anki notes as text: `wdoc_parse_file --filetype "anki" --anki_profile "Main" --anki_deck "mydeck::subdeck1" --anki_notetype "my_notetype" --anki_template "<header>\n{header}\n</header>\n<body>\n{body}\n</body>\n<personal_notes>\n{more}\n</personal_notes>\n<tags>{tags}</tags>\n{image_ocr_alt}" --anki_tag_filter "a::tag::regex::.*something.*" --only_text`**

## Please read:
* **Why did I make this?** I wanted to make my anki databases searchable though [Recoll](https://www.lesbonscomptes.com/recoll/) or Docfetcher (those are desktop search engines).
* **What do you think of issues and contributions?** They are more than welcome, even just for typos, don't hesitate to open an issue.
* **Will this change my collection?** No, it makes a copy before hand and doesn't change a thing.
* **What version of python should I use?** It has been tested on Python 3.9
* **I'd like to index my rss reader into recoll, is it possible?** I created just that [over there](https://github.com/thiswillbeyourgithub/IndexableNewsboat)
* **How does it work?** It finds your database, copies it inside /tmp (otherwise it might be locked), loads it into pandas, drops useless columns,finds the deck name and add it to each line, saves each card as a .txt file, zips all the txt files together, moves the zip in the desired folder, deletes the txt files and the temporary db.
* **Is it cross platform?** Currently no, only Linux, and OSX could maybe work quite easily. It's on the todo list but don't be afraid to ask if you think you need this.

## TODO:
* use ankipandas
* make it OS agnostic, so far it can only work on linux and possibly OSX

## Usage:
```
python3 ./IndexableAnki.py -a ~/.local/share/Anki2 -p Myprofile -o ~/Documents/
```

```
usage: IndexableAnki.py [-h] [-a ANKI_PATH] [-p ANKI_PROFILE] [-o OUT_PATH] [-f {zip,directory}]

optional arguments:
  -h, --help            show this help message and exit
  -a ANKI_PATH, --anki ANKI_PATH
                        The path to the anki folder (ex: /home/USER/.local/share/Anki2/)
  -p ANKI_PROFILE, --profile ANKI_PROFILE
                        Name of the anki profile you want to make indexable (ex: Main)
  -o OUT_PATH, --output_dir OUT_PATH
                        Path to the directory where the indexable archive will be found
  -f {zip,directory}, --format {zip,directory}
                        Format of the output archive. Default: zip
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
