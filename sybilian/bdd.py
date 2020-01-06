from pymongo import MongoClient
import csv
from pprint import pprint
from re import sub
from yaml import safe_load
from json import loads

from cards import *
from deck import *

CLIENT = MongoClient('mongodb://TDLOG:sybilian@127.0.0.1:27017/sybiliandb')
DB = CLIENT.sybiliandb
COLLECTION = DB.cards
COULEUR = {"A" : "blue", "B" : "red", "C" : "orange", "D" : "yellow", "E" : "gray", "F" : "green", "G" : "purple" }

def reset_bdd() -> None:
    """
        Delete every document in
        the database
    """
    COLLECTION.delete_many({})


def upload_tsv_bdd(csv_file : str) -> None:
    """
        Connect to the BDD and
        append all the new cards
        /!\ we don't check if the
        card already exists
    """
    with open(csv_file, newline = '') as csvfile:
        parse = csv.reader(csvfile, delimiter = "\t", quotechar="|")
        card_list = []
        for j, row in enumerate(parse):
            try:
                if COLLECTION.count_documents({"id":row[0]})==0:
                    json = dict()
                    json["id"]=row[0]
                    json["color"] = COULEUR[row[0][0]]
                    json["game_text"] = row[1]
                    json["type"] = row[2]
                    json["kin"] = row[3]
                    json["name"] = row[4]
                    json["effect"] = loads(row[5])
                    card_list.append(json)
                    x = COLLECTION.insert_one(json)
                else:
                    print("La carte existe déjà dans la BDD")
            except Exception as e:
                print("La carte ",j," n'a pas été enregistré dans la bdd")
                print(e)
                pass

def pull_card(id_card : str) -> Monster:
    """
        Ask the BDD to pull the card
        with the specic id
    """
    cursor = COLLECTION.find({"id":id_card})
    if COLLECTION.count_documents({"id":id_card})==0:
        return Placeholder()
    for cards in cursor:
        return Monster(cards["name"], 1, cards["color"], cards["kin"], cards["effect"], cards["game_text"],cards["id"])


def csv_to_deck(csv_file : str) -> Deck:
    """
        Function that reads a csv
        of ID and return a Deck
    """
    deck = Deck([])
    with open(csv_file, newline = '') as csvfile:
        parse = csv.reader(csvfile, delimiter = ",", quotechar = "|")
        for j,row in enumerate(parse):
            deck.add(pull_card(row[0]))
    return deck


def show_bdd() -> None:
    """
        Show every entry of
        the BDD
    """
    cursor = COLLECTION.find({})
    for cards in cursor:
        pprint(cards)
