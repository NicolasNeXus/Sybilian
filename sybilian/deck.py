from collections import deque
import random
from cards import Card, Monster


class Deck:
    """ A deck contains cards and has an owner """

    def __init__(self, my_container: list, owner: str = None) -> None:
        """ Create a Deck of cards with a LIFO """
        for card in my_container:
            card.owner = owner
        self.container = deque(my_container)
        self.size = len(my_container)

    def draw(self) -> Card:
        """ Draw a card from the deck and return the card """
        self.size -= 1
        return self.container.pop()

    def add_end(self, card: Card) -> None:
        """ Add a card at the end of the deck """
        self.container.appendleft(card)
        self.size += 1

    def add(self, card: Card) -> None:
        """ Add a card to the deck """
        self.container.append(card)
        self.size += 1

    def shuffle(self) -> None:
        """ Shuffle the Deck """
        list_container = list(self.container)
        random.shuffle(list_container)
        self.container = deque(list_container)

    def __str__(self) -> str:
        """ Print a deck """
        printable_content = ""
        for cards in list(self.container):
            printable_content += cards.__str__() + "\n" + "\n"
        return printable_content


class Life(Deck):
    """ Life has 9 cards and represents the first 9 hp """

    def __init__(self, deck: Deck) -> None:
        """ Create the Life by drawing 9 cards of the deck """
        super().__init__([])
        self.deck = deck
        for _ in range(9):
            self.add(deck.draw())


class Hand():
    """ Hand is the cards which the player has access to """

    def __init__(self, deck: Deck, life: Life) -> None:
        """ Keep a copy of the deck and the life it contains max 10 cards """
        self.container = list()
        self.deck = deck
        self.life = life
        self.max_len = 10
        self.size = len(self.container)
        for _ in range(4):
            self.add(deck.draw())

    def add(self, card: Card) -> None:
        """ Add a card to the hand's container """
        if len(self.container) < self.max_len:
            self.container.append(card)
            self.size += 1

    def read_card(self, i: int) -> Monster:
        """ Return a reference to the card in the hand at the position i """
        return self.container[i]

    def draw(self) -> None:
        """ Add the drawn card to the hand. The card comes from the deck """
        if len(self.container) < 10:
            self.add(self.deck.draw())

    def draw_hp(self) -> None:
        """ Add the drawn card to the hand. The card comes from the health """
        if len(self.container) < 10:
            self.add(self.life.draw())

    def play(self, j: int) -> Card:
        """ Return the j-th card of the hand """
        card_j = self.container.pop(j)
        self.size -= 1
        return card_j

    def __str__(self) -> str:
        """ Print a hand """
        printable_content = ""
        for cards in list(self.container):
            printable_content += cards.__str__() + "\n" + "\n"
        return printable_content


class Graveyard(Deck):
    """ Contains the monsters which are dead, the spells which were played """

    def __init__(self) -> None:
        """ Create the graveyard """
        super().__init__([])

    def grab(self, j: int) -> Card:
        """ Grab the jth card form the Graveyard """
        self.size -= 1
        storage = deque([])
        for _ in range(j):
            storage.append(self.container.pop())
        card_j = self.container.pop()
        for _ in range(j):
            self.container.append(storage.pop())
        return card_j
