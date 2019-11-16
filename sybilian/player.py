from cards import *
from deck import *
from board import *

class Player:
    def __init__(self, deck_name : str, board = Board) -> None:
        self.deck = self.create_deck(deck_name)
        self.owner = deck_name
        self.life = Life(self.deck)
        self.hand = Hand(self.deck, self.life)
        self.grave = Graveyard()
        self.board = board
        self.other_player = None

    def __str__(self):
        """
            create a string from
            a player
        """
    
    def draw(self) -> None:
        """
            Draw a card from the
            deck and put it
            into the hand of
            the player
        """
        self.hand.draw()
 
    def draw_hp(self) -> None:
        """
            Draw a card from the
            HP and put it
            into the hand of
            the player
        """
        self.hand.draw_hp()


    def create_deck(self, deck_name : str):
        """
            Create the deck of the player
            according to the name of the
            deck
        """
        return csv_to_deck(deck_name)

    def attack_monster(self, card : Monster, other_card : Monster) -> None:
        """
            Attack the other Monster
            on the board directly
        """
        card.life-=1
        other_card.life-=1
        self.board.clean()
        self.empty_purgatory()
        self.other_player.empty_purgatory()

    def attack_player_with_monster(self, card : Monster, other_player) -> None:
        """
            Attack the other player
            directly. 
            /!\ must verify that
            there is nothing on the
            first line
            /!\ must verify that
            attack can't be countered
        """
        other_player.draw_hp()
        print("the hp is drawn")
        card.life-=1
        self.board.clean()
        self.empty_purgatory()

    def empty_purgatory(self) -> None:
        """
            Put the monster within the
            purgatory in the graveyard
            if and only if they are
            dead
        """
        storage = deque([])
        storage_size = 0
        for i in range(self.board.purgatory.size):
            card_purgatory = self.board.purgatory.draw()
            print(card_purgatory.owner)
            print(self.owner)
            # One should apply here the effect on the card
            if (card_purgatory.owner == self.owner):
                self.grave.add(card_purgatory)
            else:
                storage_size+=1
                storage.append(card_purgatory)
        for i in range(storage_size):
            self.board.purgatory.add(storage.pop())
        

    def play(self, j : int, coord : tuple = (0,0)) -> None:
        """
            The player plays a card from
            its hand on the board at the
            position coord
            /!\ must test the coord because
            we can't play on the ennemy's board
        """
        card_played = self.hand.play(j)
        if isinstance(card_played, Monster):
            card_played.coord = coord
            self.board.play(card_played, coord)
