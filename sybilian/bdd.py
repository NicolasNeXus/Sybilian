from pymongo import MongoClient
import csv
from pprint import pprint
from re import sub
from yaml import safe_load

from cards import *

CLIENT = MongoClient('mongodb://TDLOG:sybilian@127.0.0.1:27017/sybiliandb')
DB = CLIENT.sybiliandb
COLLECTION = DB.cards
COULEUR = {"A" : "blue", "B" : "red", "C" : "orange", "D" : "yellow", "E" : "gray", "F" : "green", "G" : "purple" }


def reset_bdd():
    return True

def upload_csv_bdd(csv_file : str) -> None:
    """
        Connect to the BDD and
        append all the new cards
        /!\ we don't check if the
        card already exists
    """
    with open(csv_file, newline = '') as csvfile:
        parse = csv.reader(csvfile, delimiter = ",", quotechar="|")
        for j, row in enumerate(parse):
            try:
                json = dict()
                json["id"]=row[0]
                json["color"] = COULEUR[row[0][0]]
                json["game_text"] = row[1]
                json["type"] = row[2]
                json["kin"] = row[3]
                json["name"] = row[4]
                effect = sub('""','"', row[5][1:-1].rstrip())
                effect = sub(";",",", effect.rstrip())
                json["effect"] = safe_load(effect)
                card_list.append(json)
                x = COLLECTION.insert_one(json)
            except:
                pprint(row)
                pass

def pull_card(id_card : str) -> Monster:
    """
        Ask the BDD to pull the card
        with the specic id
    """
    cursor = COLLECTION.find({"id":id_card})
    for cards in cursor:
        return Monster(cards["name"], 1, cards["color"], cards["kin"], cards["effect"], cards["id"])


def show_bdd() -> None:
    """
        Show every entry of
        the BDD
    """
    cursor = COLLECTION.find({})
    for cards in cursor:
        pprint(cards)
