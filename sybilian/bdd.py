import csv
from pprint import pprint
from json import loads
from pymongo import MongoClient

from cards import Monster, Card
from deck import Deck


CLIENT = MongoClient('mongodb://TDLOG:sybilian@192.168.99.100/sybiliandb')
DB = CLIENT.sybiliandb
COLLECTION = DB.cards
COULEUR = {"A" : "blue", "B" : "red", "C" : "orange", "D" : "yellow", "E" : "gray", "F" : "green", "G" : "purple"}

def reset_bd() -> None:
    """ Delete every document in the database """
    COLLECTION.delete_many({})


def upload_tsv_bdd(tsv_file: str) -> None:
    """ Connect to the BDD and append all the new cards
        !! we don't check if the card already exists

    :param tsv_file : name of the file
    """

    with open(tsv_file, newline='') as tsvfile:
        parse = tsv.reader(tsvfile, delimiter="\t", quotechar="|")
        card_list = []
        for j, row in enumerate(parse):
            try:
                if COLLECTION.count_documents({"id":row[0]}) == 0:
                    json = dict()
                    json["id"] = row[0]
                    json["color"] = COULEUR[row[0][0]]
                    json["game_text"] = row[1]
                    json["type"] = row[2]
                    json["kin"] = row[3]
                    json["name"] = row[4]
                    json["effect"] = loads(row[5])
                    card_list.append(json)
                    COLLECTION.insert_one(json)
                else:
                    print("La carte existe déjà dans la BDD")
            except Exception as e:
                print("La carte ", j, " n'a pas été enregistré dans la bdd")
                print(e)
                pass


def pull_card(id_card: str) -> Card:
    """ Ask the BDD to pull the card with the specic id

    :param id_card : id of the card
    """

    cursor = COLLECTION.find({"id":id_card})
    if COLLECTION.count_documents({"id":id_card}) == 0:
        return Placeholder()
    for cards in cursor:
        return Monster(cards["name"], 1, cards["color"], cards["kin"], cards["effect"], cards["game_text"], cards["id"])


def csv_to_deck(csv_file: str) -> Deck:
    """ Function that reads a csv of ID and return a Deck

    :param csv_file : name of the file
    """

    deck = Deck([])
    with open(csv_file, newline='') as csvfile:
        parse = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in parse:
            card_pulled = pull_card(row[0])
            card_pulled.owner = csv_file
            deck.add(card_pulled)
    return deck


def show_bdd() -> None:
    """ Show every entry of the BDD """
    cursor = COLLECTION.find({})
    for cards in cursor:
        pprint(cards)
