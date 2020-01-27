"""
Created on Fri Nov 29 11:08:41 2019

@author: clari
and @Nicolas
"""

from cards import Monster, Placeholder, Spell
from board import Board
from player import Player

class Game:
    """ Game (model) with the different methods to communicate with the graphic
        interface
    """

    def __init__(self) -> None:
        """ Game with two players, a board, the index of the current player
            and the number of actions he still have
        """

        self.board = Board()
        # player_one has access to the first and second lines of the board
        # player_two has access to the third and fourth lines of the board
        self.players = (Player("deckC001.csv", self.board, [1, 0]), Player("deckB001.csv", self.board, [2, 3]))
        self.players[0].other_player = self.players[1]
        self.players[1].other_player = self.players[0]
        self.index = 0
        self.nb_actions = 2
        self.end = False

    def get_current_hand(self):
        """ Return the 'hand' of the player actually playing """
        return self.players[self.index].hand.container

    def condition_endgame(self) -> bool:
        """ Return True if a player won, False otherwise """
        if self.players[0].life_points > 0 and self.players[1].life_points > 0:
            return False
        if self.players[0].life_points == 0:
            print("Le joueur " + str(self.players[0].owner) + " a gagné!")
            return True
        print("Le joueur " + str(self.players[1].owner) + " a gagné!")
        return True

    def can_play_monster(self, index_card: int, coord: tuple) -> bool:
        """ Return [True, elements to refresh] if the player can play the
            monster

        :param index_card : index of the card
        :param coord : position where we want to put the card
        """

        player_playing = self.players[self.index]
        opponent = self.players[(self.index + 1) % 2]
        # The owner's card that wants to play is the player who is playing and
        # the card is a monster
        if isinstance(player_playing.hand.read_card(index_card), Monster):
            # The player still have actions left
            if self.nb_actions > 0:
                # The coordinates are valid
                if coord[0] in player_playing.lines and coord[1] in [0, 1, 2]:
                    # The spot is empty
                    if isinstance(self.board.get_monster(coord), Placeholder):
                        # Impact
                        if "Impact" in player_playing.hand.read_card(index_card).effect.keys():
                            player_playing.play(index_card, coord)
                            self.nb_actions -= 1
                            return [True, player_playing.hand.container, player_playing.deck.size, player_playing.life.size, player_playing.grave.size, opponent.hand.size, opponent.deck.size, opponent.life.size, opponent.grave.size, self.board]
                        player_playing.play(index_card, coord)
                        self.nb_actions -= 1
                        return [True, player_playing.hand.container, player_playing.deck.size, None, None, None, None, None, None, self.board]
        return [False]

    def can_play_spell(self, index_card: int) -> bool:
        """ Return [True, elements to refresh] if the player can play the spell

        :param index_card : index of the card
        """

        player_playing = self.players[self.index]
        opponent = self.players[(self.index + 1) % 2]
        # The owner's card that wants to play is the player who is playing and
        # the card is a spell
        if isinstance(player_playing.hand.read_card(index_card), Spell):
            player_playing.play(index_card)
            return [True, player_playing.hand.container, player_playing.deck.size, player_playing.life.size, player_playing.grave.size, opponent.hand.size, opponent.deck.size, opponent.life.size, opponent.grave.size, self.board]
        return [False]

    def can_draw_card(self):
        """ Return [True, elements to refresh] if the player can draw a card
            from his deck/hp
        """
        player_playing = self.players[self.index]
        # The player still have actions left
        if self.nb_actions > 0:
            # The player's deck is not empty:
            if player_playing.deck.size > 0:
                # Verify that the player have less than max_len cards in his hand
                if player_playing.hand.size < player_playing.hand.max_len:
                    player_playing.draw()
                    self.nb_actions -= 1
                    return [True, player_playing.hand.container, player_playing.deck.size, None, None, None, None, None, None, None]
                # The card is added to the graveyard
                player_playing.draw()
                self.nb_actions -= 1
                return [True, None, player_playing.deck.size, None, player_playing.grave.size, None, None, None, None, None]
            # We draw in the hp
            if player_playing.deck.size == 0 and player_playing.life.size > 0:
                # Verify that the player have less than max_len cards in his hand
                if player_playing.hand.size < player_playing.hand.max_len:
                    player_playing.draw()
                    self.nb_actions -= 1
                    return [True, player_playing.hand.container, None, player_playing.life.size, None, None, None, None, None, None]
                # The card is added to the graveyard
                player_playing.draw()
                self.nb_actions -= 1
                return [True, None, None, player_playing.life.size, player_playing.grave.size, None, None, None, None, None]
            # The player kills himself
            player_playing.draw()
            self.nb_actions -= 1
        return [False]

    def can_card_attack(self, coord: tuple) -> bool:
        """ Return True if the card with the coordinates coord can attack """
        player_playing = self.players[self.index]
        # The coordinates are valid
        if coord[0] in player_playing.lines and coord[1] in [0, 1, 2]:
            return True
        return False

    def can_attack_monster(self, coord1: tuple, coord2: tuple) -> list:
        """ Return True if the player can attack an opponent's monster with his
            own monster

        :param coord1 : coordinates of the monster which is supposed to attack
        :param coord2 : coordinates of the monster which is supposed to be attacked
        """

        player_playing = self.players[self.index]
        opponent = player_playing.other_player
        # The player who wants to attack is the player who is playing
        if  coord1[0] in player_playing.lines and coord1[1] in [0, 1, 2]:
            # The player is attacking his oponent
            if coord2[0] in opponent.lines and coord2[1] in [0, 1, 2]:
                # We have two monsters
                if isinstance(self.board.get_monster(coord1), Monster) and isinstance(self.board.get_monster(coord2), Monster):
                    # The player wants to attack the first line of his opponent
                    if coord2[0] == opponent.lines[0]:
                        player_playing.attack_monster(self.board.get_monster(coord1), self.board.get_monster(coord2))
                        return [True, player_playing.hand.container, player_playing.deck.size, player_playing.life.size, player_playing.grave.size, opponent.hand.size, opponent.deck.size, opponent.life.size, opponent.grave.size, self.board]
                    # The player wants to attack the second line of his opponent
                    if coord2[0] == opponent.lines[1] and player_playing.verify_first_line_opponent_empty():
                        player_playing.attack_monster(self.board.get_monster(coord1), self.board.get_monster(coord2))
                        return [True, player_playing.hand.container, player_playing.deck.size, player_playing.life.size, player_playing.grave.size, opponent.hand.size, opponent.deck.size, opponent.life.size, opponent.grave.size, self.board]
        return [False]

    def can_attack_opponent_with_monster(self, coord: tuple):
        """ Return [True, elements to refresh] if the player can attack his
            opponent with his monster

        :param coord : coordinates of the monster which is supposed to attack
        """

        player_playing = self.players[self.index]
        opponent = player_playing.other_player
        # The player who wants to attack is the player who is playing
        if coord[0] in player_playing.lines and coord[1] in [0, 1, 2]:
            # We have a monster
            if isinstance(self.board.get_monster(coord), Monster):
                # The first line of the opponent is empty
                if player_playing.verify_first_line_opponent_empty():
                    player_playing.attack_player_with_monster(self.board.get_monster(coord))
                    return [True, player_playing.hand.container, player_playing.deck.size, player_playing.life.size, player_playing.grave.size, opponent.hand.size, opponent.deck.size, opponent.life.size, opponent.grave.size, self.board]
        return [False]

    def can_end_turn(self) -> bool:
        """ Return [True, elements to refresh] if the player can end his
            turn
        """

        # The player has no actions left
        if self.nb_actions == 0:
            self.index = (self.index + 1) % 2
            self.nb_actions = 2
            self.players[self.index].draw()
            player_playing = self.players[self.index]
            opponent = player_playing.other_player
            return [True, player_playing.hand.container, player_playing.deck.size, player_playing.life.size, player_playing.grave.size, opponent.hand.size, opponent.deck.size, opponent.life.size, opponent.grave.size, self.board]
        return [False]
          