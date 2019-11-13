from collections import deque
import random

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

    def add(self, cards):
        """
            Add a card to the deck
        """
        self.container.append(cards)

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
            printable_content+=cards.__str__()
        return printable_content

