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
            printable_content+=cards.__str__()+"\n"+"\n"
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

class Hand():
    def __init__(self, deck : Deck, life : Life) -> None:
        """
            Keep a copy of the deck
            within the hand. Linker.
            The deck contains 10 cards max.
        """
        self.container = list()
        self.deck = deck
        self.life = life
        self.max_len = 10
        self.size = len(self.container)
        for i in range(4):
            self.add(deck.draw())


    def add(self, card : Monster) -> None:
        """
            add a card to the hand
            container
        """
        if len(self.container) < 10:
            self.container.append(card)
            self.size+=1

    def read_card(self, i : int) -> Monster:
        """
            Return a reference to
            the card in the hand
            at the position i
        """
        return self.container[i]

    def draw(self) -> None:
        """
            add the drawn card to the hand.
            The card comes from the deck
        """
        if len(self.container) < 10:
            self.add(self.deck.draw())

    def draw_hp(self) -> None:
        """
            add the drawn card to the hand.
            The card comes from the health
        """
        if len(self.container) < 10:
            self.add(self.life.draw())

    def play(self, j : int) -> Card:
        """
            play the j-th card of the hand
        """
        card_j = self.container.remove(j)
        self.size-=1
        return card_j
        
    def __str__(self) -> str:
        """
            Print a hand
        """
        printable_content = ""
        for cards in list(self.container):
            printable_content+=cards.__str__()+"\n"+"\n"
        return printable_content

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

