from collections import deque
import random
import csv
from cards import *

class Deck:
    def __init__(self, my_container):
        """
            Create a Deck of cards
            with a LIFO
        """
        self.container = deque(my_container)

    def draw(self):
        """
            Draw a card from the deck
            and return the card
        """
        return self.container.pop()

    def add_end(self, card):
        """
            Add a card at the end of the deck
        """
        self.container.appendleft(card)

    def add(self, card):
        """
            Add a card to the deck
        """
        self.container.append(card)

    def shuffle(self):
        """
            Shuffle the Deck
        """
        list_container = list(self.container)
        random.shuffle(list_container)
        self.container = deque(list_container)

    def __str__(self):
        """
            Print a deck
        """
        printable_content = ""
        for cards in list(self.container):
            printable_content+=cards.__str__()+"\n"
        return printable_content

def csv_to_deck(csv_file):
    """
        Basic function to create a deck
        from a csv file. Used for dev only
    """
    deck = Deck([])
    name = None
    color = None
    type_card = None
    effect = None
    with open(csv_file, newline = '') as csvfile:
        parse = csv.reader(csvfile, delimiter = ",", quotechar="|")
        for j,row in enumerate(parse):
            if j==0:
                pass
            for i, cells in enumerate(row):
                if i==0:
                    name = cells
                if i==1:
                    color = cells
                if i==2:
                    type_card = cells
                if i==3:
                    effect = cells
            if type_card == "Sort":
                deck.add(Spell(name,0,color, effect))
            if type_card == "Créature":
                deck.add(Monster(name,1,color,"",effect))
            if type_card == "Parade":
                deck.add(Counterspell(name,0,color,effect))
    return deck



if __name__=="__main__":
    card_1 = Monster("Devorombre", 1, "Violet", "Demon", "Transforme en ombre la créature attaquée")
    card_2 = Counterspell("Armistice", 0, "Gris","Toutes les prochaines attaques sont contrés")
    card_3 = Spell("Boule de feu", 0, "Rouge", "L'adversaire perd un point de vie")
    deck = Deck([card_1, card_2, card_3])
