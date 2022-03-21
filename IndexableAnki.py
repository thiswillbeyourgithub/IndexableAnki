#!/usr/bin/env python
# coding: utf-8

#    Released under the GNU General Public License v3.
#    Copyright (C) - 2021 - user "thiswillbeyourgithub" of "github.com"
#    This file is IndexableAnki. It aims to make your anki database searchable
#
#    IndexableAnki is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    IndexableAnki is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with IndexableAnki.  If not, see <https://www.gnu.org/licenses/>.

#    for more information or to get the latest version go to :
#    https://github.com/thiswillbeyourgithub/IndexableAnki
#    Version : March 2021


# imports ###################################################
import pandas as pd
import sqlite3
import os
import re
import argparse
from tqdm import tqdm
from pathlib import Path
import shutil


# arguments ###################################################
parser = argparse.ArgumentParser()
parser.add_argument("-a",
                    "--anki",
                    help="The path to the anki folder(ex:\
/home/USER/.local/share/Anki2/)",
                    dest="anki_loc",
                    metavar="ANKI_PATH")
parser.add_argument("-p",
                    "--profile",
                    help="Name of the anki profile you want to make\
indexable (ex: Main)",
                    dest="profile",
                    metavar="ANKI_PROFILE")
parser.add_argument("-o",
                    "--output_dir",
                    help="Path to the directory where the indexable\
archive will be found",
                    dest="output_dir",
                    metavar="OUT_PATH")
args = parser.parse_args().__dict__


# checks ###################################################
if args['anki_loc'] is None or\
        args['profile'] is None or\
        args['output_dir'] is None:
    print(f"Problem with provided arguments:\n{args}\nExiting.")
    raise SystemExit()
else:
    args['db_loc'] = f"{args['anki_loc']}/{args['profile']}/collection.anki2"

if " " in args['profile']:  # fixes unescaped spaces
    args['profile_escaped'] = args['profile'].replace(" ", "_")
else :
    args['profile_escaped'] = args['profile']

if not Path.exists(Path(args["db_loc"])):
    print(f"Anki db not found.\n{args}\nExiting.")
    raise SystemExit()
else:
    print(f"Found db {args['db_loc']}...")

# main code ###################################################

print("Creating temporary db at /tmp/anki_temporary.db...")
if " " in args['db_loc']:  # fixes unescaped spaces
    args['db_loc'] = args['db_loc'].replace(" ", r"\ ")
Path.unlink(Path("/tmp/anki_temporary.db"), missing_ok=True)
shutil.copy(args['db_loc'], "/tmp/anki_temporary.db")


def query_sql(table):
    "get anki db as a pandas DataFrame"
    conn = sqlite3.connect("/tmp/anki_temporary.db")
    query = f"SELECT * FROM {table}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


print("Getting anki db as pandas DataFrame...")
db = query_sql("notes").copy().set_index("id")
cardid_did = query_sql("cards").copy().set_index("nid")
deck_id_name = query_sql("decks").copy().set_index("id")


print("Adjusting DataFrame...")
db.drop(columns=['guid', 'mid', 'mod', 'usn', 'csum', 'flags', 'data'],
        inplace=True)
db.sort_index()


def deck_namer(card_id, card_id_did, deck_id_name):
    "used to fill the deck_name field of the dataframe for each card"
    did = card_id_did.loc[card_id]['did']
    name = deck_id_name.loc[did]["name"]
    name = re.sub('\u001F', "::", str(name))  # removes \x1F
    return name


print("Retrieving deck name for each card...")
db["deck_name"] = [deck_namer(n, cardid_did, deck_id_name)
                   for n in tqdm(db.index)]
db.sort_index()


def text_processor(content):
    "to remove clozes and useless html"
    content = str(content).lower()
    content = content.replace("\'", " ")  # removes ''
    content = content.replace("\\n", " ")  # removes newline
    content = content.replace("<div>", " ")
    content = content.replace("</div>", " ")
    content = content.replace("<br>", " ")
    content = content.replace("\u001F", " ")  # removes \x1F
    content = re.sub(r"\[sound:.*?\]", " ", content)  # extract title of
    # images (usually OCRed text) before html is removed
    content = re.sub(r"paste-.*?\....", "", content)
    content = re.sub("title=(\".*?\")", ">OCR:\\1<", content)  # extract
    # title of images (usually OCR'd text) before html is removed
    content = re.sub("<.*?>", " ", content)  # removes all html
    content = re.sub(r"{{c\d+::", "", content)  # removes clozing
    content = content.replace("}}", " ")  # replace clozing with a space
    content = content.replace("::", " ")  # part of clozing + punct
    content = content.replace("&nbsp;", " ")  # html spaces
    content = content.replace("/", " ")  # slash
    return content


print("Processing text content 1/2...")
db["sfld"] = [text_processor(content) for content in tqdm(db["sfld"])]
print("Processing text content 2/2...")
db["flds"] = [text_processor(content) for content in tqdm(db["flds"])]


shutil.rmtree("/tmp/IndexableAnki", ignore_errors=True)
Path.mkdir(Path("/tmp/IndexableAnki"), exist_ok=True)


def save_card_as_file(card_id):
    with open(f"/tmp/IndexableAnki/Anki_{args['profile_escaped']}_{card_id}.txt",
              'w', encoding="utf-8") as f:
        string = "ANKI EXPORT AS TXT\n"
        string += f"anki profile: {args['profile']}\n"
        string += f"card id: {card_id}\n"
        string += f"tags: {str(db.loc[card_id]['tags']).strip()}\n"
        string += f"deck: {str(db.loc[card_id]['deck_name']).strip()}\n"
        string += f"sfld: {db.loc[card_id]['sfld']}\n"
        string += f"flds: {db.loc[card_id]['flds']}\n"
        f.write(string)


print("Saving cards as txt...")
for i in tqdm(db.index):
    save_card_as_file(i)

print("Compressing as a zip archive...")
Path.unlink(Path(f"{args['output_dir']}/IndexableAnki_{args['profile_escaped']}.zip"), missing_ok=True)
os.system(f"cd /tmp/IndexableAnki && zip -9 {args['output_dir']}/IndexableAnki_{args['profile_escaped']}.zip *")


print("Cleaning up...")
shutil.rmtree("/tmp/IndexableAnki")
Path.unlink(Path("/tmp/anki_temporary.db"), missing_ok=True)


print("Done!\nExiting...")
