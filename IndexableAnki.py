#!/usr/bin/env python
# coding: utf-8

# # Indexable Anki
# The goal is to export all anki databses as txt files (one file per card)
# so that it can be accessible using desktop search
# engines such as Recoll or DocFetcher.


# imports ###################################################
import pandas as pd
import sqlite3
import os
import re
import argparse
from tqdm import tqdm


# arguments ###################################################
parser = argparse.ArgumentParser()
parser.add_argument("-a",
                    "--anki",
                    help="The path to the anki folder(ex: /home/USER/.local/share/Anki2/)",
                    dest="anki_loc",
                    metavar="ANKI_PATH")
parser.add_argument("-p",
                    "--profile",
                    help="Name of the anki profile you want to make indexable (ex: Main)",
                    dest="profile",
                    metavar="ANKI_PROFILE")
parser.add_argument("-o",
                    "--output",
                    help="Path to the directory that will contain the indexable anki",
                    dest="out_loc",
                    metavar="output_PATH")
parser.add_argument("-t",
                    "--temp-path",
                    help="Path where a temporary anki db will be stored (ex /tmp/anki.db)",
                    dest="tmp_loc",
                    metavar="TMP_PATH")
args = parser.parse_args().__dict__


# checks ###################################################
if args['anki_loc'] is None or\
        args['profile'] is None or\
        args['out_loc'] is None:
    print(f"Problem with provided arguments:\n{args}\nExiting.")
    raise SystemExit()
else:
    args['out_loc_full'] = f'{args["out_loc"]}/IndexableAnki/{args["profile"]}'
    args['db_loc'] = f"{args['anki_loc']}/{args['profile']}/collection.anki2"
    if args['tmp_loc'] is None:
        args['tmp_loc'] = "/tmp/anki_db.db"

if not os.path.exists(args["db_loc"]):
    print(f"Anki db not found.\n{args}\nExiting.")
    raise SystemExit()
else:
    print(f"Found db {args['db_loc']}...")

# main code ###################################################

print(f"Creating temporary db at {args['tmp_loc']}...")
if " " in args['db_loc']:  # fixes unescpaed spaces
    args['db_loc'] = args['db_loc'].replace(" ", r"\ ")
os.system(f'rm "{args["tmp_loc"]}"')
os.system(f"cp --remove-destination {args['db_loc']} {args['tmp_loc']}")


def query_sql(table):
    "get anki db as a pandas DataFrame"
    conn = sqlite3.connect(args['tmp_loc'])
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


def deck_namer(card_id, card_id_did, deck_id_name):
    "used to fills the deck_name field of the dataframe for each card"
    did = card_id_did.loc[card_id]['did']
    name = deck_id_name.loc[did]["name"]
    name = re.sub('\u001F', "::", str(name))  # removes \x1F
    return name


print("Retrieving deck name for each card...")
db["deck_name"] = [deck_namer(n, cardid_did, deck_id_name) for n in tqdm(db.index)]
db.sort_index()


def text_processor(content) :
    "to remove clozes and useless html"
    content = str(content).lower()
    content = re.sub('\'', " ", content)  # removes ''
    content = re.sub('\\n|<div>|</div>|<br>', " ", content)  # removes newline
    content = re.sub('\u001F', " ", content)  # removes \x1F
    content = re.sub("\[sound:.*?\]", " ", content)  # extract title of
    # images (usually OCR'd text) before html is removed
    content = re.sub("paste-.*?\....", "", content)
    content = re.sub("title=(\".*?\")", ">OCR:\\1<", content)  # extract
    # title of images (usually OCR'd text) before html is removed
    content = re.sub("<.*?>", " ", content)  # removes all html
    content = re.sub("{{c\d+::|}}", "", content)  # removes clozing
    content = re.sub("::|:", " ", content)  # part of clozing + punc
    content = re.sub("&nbsp;", " ", content)  # html spaces
    content = re.sub("/", " ", content)  # replaces / by a space
    return content


print("Processing text content 1/2...")
db["sfld"] = [text_processor(content) for content in tqdm(db["sfld"])]
print("Processing text content 2/2...")
db["flds"] = [text_processor(content) for content in tqdm(db["flds"])]
db.sort_index()


os.system(f'mkdir -p "{args["out_loc_full"]}"')


def save_card_as_file(card_id):
    with open(f'{args["out_loc_full"]}/{card_id}.txt',
              'w', encoding="utf-8") as f:
        string = "ANKI EXPORT AS TXT\n"
        string += f"card id: {card_id}\n"
        string += f"tags: {str(db.loc[card_id]['tags']).strip()}\n"
        string += f"deck: {str(db.loc[card_id]['deck_name']).strip()}\n"
        string += f"sfld: {db.loc[card_id]['sfld']}\n"
        string += f"flds: {db.loc[card_id]['flds']}\n"
        f.write(string)


print("Saving cards as txt...")
for i in tqdm(db.index):
    save_card_as_file(i)

print("Done!\nExiting...")

