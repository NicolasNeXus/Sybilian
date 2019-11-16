from collections import deque
import random
import csv
from cards import *

class Deck:
    def __init__(self, my_container : list, owner : str = None) -> None:
        """
            Create a Deck of cards
            with a LIFO
        """
        for card in my_container:
            card.owner = owner
        self.container = deque(my_container)
        self.size = len(my_container)

    def draw(self) -> Card:
        """
            Draw a card from the deck
            and return the card
        """
        self.size-=1
        return self.container.pop()

    def add_end(self, card : Card) -> None:
        """
            Add a card at the end of the deck
        """
        self.container.appendleft(card)
        self.size+=1

    def add(self, card : Card) -> None:
        """
            Add a card to the deck
        """
        self.container.append(card)
        self.size+=1

    def shuffle(self) -> None:
        """
            Shuffle the Deck
        """
        list_container = list(self.container)
        random.shuffle(list_container)
        self.container = deque(list_container)

    def __str__(self) -> str:
        """
            Print a deck
        """
        printable_content = ""
        for cards in list(self.container):
            printable_content+=cards.__str__()+"\n"
        return printable_content


class Life(Deck):
    def __init__(self, deck : Deck) -> None:
        """
            Keep a copy of the deck
            within the hand. Linker.
            Maxlen = 10 ?
        """
        super().__init__([])
        self.deck = deck
        for i in range(9):
            self.add(deck.draw())

class Hand(Deck):
    def __init__(self, deck : Deck, life : Life) -> None:
        """
            Keep a copy of the deck
            within the hand. Linker.
            Maxlen = 10 ?
        """
        super().__init__([])
        self.deck = deck
        self.life = life
        for i in range(4):
            self.add(deck.draw())

    def draw(self) -> None:
        """
            add the drawn card to the hand.
            The card comes from the deck
        """
        self.add(self.deck.draw())

    def draw_hp(self) -> None:
        """
            add the drawn card to the hand.
            The card comes from the health
        """
        self.add(self.life.draw())

    def play(self, j : int) -> None:
        """
            play the j-th card of the hand
        """
        self.size-=1
        storage = deque([])
        for i in range(j):
            storage.append(self.container.pop())
        card_j = self.container.pop()
        for i in range(j):
            self.container.append(storage.pop())
        return card_j

class Graveyard(Deck):
    def __init__(self) -> None:
        super().__init__([])

    def grab(self, j : int) -> Card:
        """
            grab the jth card
            form the Graveyard
        """
        self.size-=1
        storage = deque([])
        for i in range(j):
            storage.append(self.container.pop())
        card_j = self.container.pop()
        for i in range(j):
            self.container.append(storage.pop())
        return card_j



def csv_to_deck(csv_file : str) -> Deck:
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
            if 0<j<=45:
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
                    deck.add(Spell(name,0,color, effect, csv_file))
                if type_card == "Créature":
                    deck.add(Monster(name,1,color,"",effect, csv_file))
                if type_card == "Parade":
                    deck.add(Counterspell(name,0,color,effect, csv_file))
    return deck
