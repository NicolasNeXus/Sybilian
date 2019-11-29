from cards import *
from deck import *
from board import *

class Player:
    def __init__(self, deck_name : str, board : Board, lines : list, first_line_other_player : int) -> None:
        self.deck = self.create_deck(deck_name)
        self.owner = deck_name
        self.life = Life(self.deck)
        self.life_points = self.life.size + 1
        self.hand = Hand(self.deck, self.life)
        self.grave = Graveyard()
        self.board = board
        self.lines = lines
        self.first_line_other_player = first_line_other_player
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
        # The deck still have at least one card
        if self.deck.size >= 1:
            # Verify that the player have less than max_len cards in his hand
            if self.hand.size < self.hand.max_len:
                self.hand.draw()
            # Add the card to the graveyard 
            else:
                self.grave.add(self.deck.draw())
        else:
            print("Il n'y a plus de cartes dans la pioche")
 
    def draw_hp(self) -> None:
        """
            Draw a card from the
            HP and put it
            into the hand of
            the player
        """
        self.life_points -= 1
        # The life deck still have at least one card
        if self.life.size >= 1:
            # Verify that the player have less than max_len cards in his hand
            if self.hand.size < self.hand.max_len:
                self.hand.draw_hp()
            # Add the card to the graveyard 
            else:
                self.grave.add(self.life.draw())


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
        assert isinstance(card, Monster) and isinstance(other_card, Monster)
        #self.card.attack(other_card) quand on aura implémenter l'effet puissant
        card.life-=1
        other_card.life-=1
        self.board.clean()
        self.empty_purgatory()
        self.other_player.empty_purgatory()
    
    def verify_first_line_opponent_empty(self) -> bool:
        """ 
            Verify that the first line
            of the opponent is empty
            Return True if it's empty
        """
        empty = not isinstance(self.board.grid[self.first_line_other_player][0], Monster)
        for i in range(1, 3):
            empty = empty and not isinstance(self.board.grid[self.first_line_other_player][i], Monster)
        return empty

    def attack_player_with_monster(self, card : Monster, other_player) -> None:
        """
            Attack the other player
            directly. 
            /!\ must verify that
            attack can't be countered
        """
        # Verify that the first line of the opponent is empty
        if self.verify_first_line_opponent_empty():
            other_player.draw_hp()
            print("the hp is drawn")
            card.life-=1
            self.board.clean()
            self.empty_purgatory()
        else:
            print("Impossible d'attaquer directement l'adversaire")

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
                self.grave.add(card_purgatory) #après regarder si ya les effets de destruction...
            # c'est les cartes de l'adversaire on les "réempile" dans le purgatoire
            else:
                storage_size+=1 
                storage.append(card_purgatory)
        for i in range(storage_size):
            self.board.purgatory.add(storage.pop())
        
    def verify_coord(self, coord : tuple) -> bool:
        """
           Verify that the co-ordinates are valid 
           Return True if they are valid
        """
        i, j = coord
        # The co-ordinates correspond to the lines of the player
        if i in self.lines and j in [0, 1, 2]:
            # The emplacement is empty
            if not isinstance(self.board.grid[i][j], Monster):
                return True
            else:
                print("Il n'y a pas de monstre sur cette case")
                return False
        print("Cette case ne correspond pas à une case de votre adversaire")
        return False
        
    def play(self, j : int, coord : tuple = (0,0)) -> None:
        """
            The player plays a card from
            its hand on the board at the
            position coord
        """
        card_played = self.hand.play(j)
        card_played.coord = coord
        if self.verify_coord(coord):
            self.board.play(card_played, coord)
