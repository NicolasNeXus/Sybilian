from cards import *
from deck import *

class Board:
    """
        A Board is a 4*3 matrix
        where player can play cards
    """
    def __init__(self) -> None:
        """
            We create an empty grid
            with the purgatory zone
        """
        self.grid = [[Card("void","-1","","") for i in range(3)] for j in range(4)]
        self.purgatory = Deck([])

    def __str__(self) -> None:
        """
            print a existing board
        """
        printable_content = ""
        for i,row in enumerate(self.grid):
            for card in row:
                printable_content += card.name + " | "
            printable_content+="\n"
            if i==1:
                printable_content += "------------------------\n"
        return printable_content

    def get_monster(self, coord : tuple) -> Monster:
        i,j = coord
        return self.grid[i][j]

    def clean(self) -> None:
        """
            Put every dead monster
            in the purgatory
        """
        for i,row in enumerate(self.grid):
            for j,monster in enumerate(row):
                if isinstance(monster, Monster) and monster.life<=0:
                    self.purgatory.add(monster)
                    self.grid[i][j] = Card("void", "-1","","") 


    def play(self, card : Card, coord : tuple) -> None:
        """
            put a card on the board
        """
        i,j = coord
        self.grid[i][j] = card
        card.coord = coord

