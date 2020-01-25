"""
    This file defines the class Player
    which is the one of the key element of
    our game.
"""

import random
from collections import deque
from cards import Monster, Placeholder, Spell
from deck import Life, Hand, Graveyard
from board import Board
from bdd import csv_to_deck


class Player:
    """
        The Player is the main class of our game.
        It can access the board, play cards and
        attack the other player with his cards
    """

    def __init__(self, deck_name: str, board: Board, lines: list)-> None:
        """ Construct a player

        :param deck_name : name of the player's deck
        :param board : board of the game
        :lines : lines where the player can play cards
        """

        self.deck = self.create_deck(deck_name)
        self.owner = deck_name
        self.life = Life(self.deck)
        self.life_points = self.life.size + 1
        self.hand = Hand(self.deck, self.life)
        self.grave = Graveyard()
        self.board = board
        self.lines = lines
        self.other_player = None

    def draw(self) -> None:
        """ Draw a card from the deck/hp and put it in the player's hand """
        # The deck still have at least one card
        if self.deck.size >= 1:
            # Verify that the player have less than max_len cards in his hand
            if self.hand.size < self.hand.max_len:
                self.hand.draw()
            # Add the card to the graveyard
            else:
                self.grave.add(self.deck.draw())
        else:
            self.draw_hp()

    def draw_hp(self) -> None:
        """ Draw a card from the hp and put it in the player's hand """
        self.life_points -= 1
        # The life deck still have at least one card
        if self.life.size >= 1:
            # Verify that the player have less than max_len cards in his hand
            if self.hand.size < self.hand.max_len:
                self.hand.draw_hp()
            # Add the card to the graveyard
            else:
                self.grave.add(self.life.draw())

    def create_deck(self, deck_name: str):
        """ Create the deck of the player

        :param deck_name : name of the deck
        """

        return csv_to_deck(deck_name)

    def attack_monster(self, card: Monster, other_card: Monster) -> None:
        """
            Attack the other Monster, put cards in the purgatory,
            clean the board and empty the purgatory which
            activates the effects

        :param card : monster which attacks
        :param other_card : monster which is attacked
        """

        card.attack(other_card)
        self.board.clean()
        self.empty_purgatory()
        self.other_player.empty_purgatory()

    def verify_first_line_opponent_empty(self) -> bool:
        """ Return True if the first line of the opponent is empty """
        empty = not isinstance(
            self.board.grid[self.other_player.lines[0]][0], Monster)
        for i in range(1, 3):
            empty = empty and not isinstance(
                self.board.grid[self.other_player.lines[0]][i], Monster
            )
        return empty

    def attack_player_with_monster(self, card: Monster) -> None:
        """ Attack the other player directly

        :param card : monster which attacks
        """

        self.other_player.draw_hp()
        card.life -= 1
        self.board.clean()
        self.empty_purgatory()

    def effect_impact(self, card: Monster, targets: list = [Placeholder()]) -> None:
        """ Trigger impact effect of a card

        :param card : monster which has an impact effect
        :param targets : optional list of targets
        """

        if "Impact" in card.effect.keys():
            if card.effect["Impact"]["Condition"] == "None":
                if "Damage" in card.effect["Impact"]["Event"]["Do"]:
                    if card.effect["Impact"]["Event"]["Do"]["Damage"] == "Target" and all(list(map(lambda card: isinstance(card, Monster), targets))):
                        if card.effect["Impact"]["Event"]["Target"]["Owner"] == "Both":
                            for i in range(min(card.effect["Impact"]["Event"]["Target"]["Amount"], len(targets))):
                                card_targeted = targets[i]
                                if card.effect["Impact"]["Event"]["Target"]["Attribute"] == "Undamaged" and card_targeted.life == 2:
                                    card_targeted.life -= 1  # works because it's a reference
                                  # no need to return a card

    def effect_destruction(self, card: Monster, targets: list = [Placeholder()]) -> None:
        """ Trigger the desctruction

        :param card : monster which has a destruction effect
        :param targets : optional list of targets
        """

        if "Destruction" in card.effect.keys():
            if card.effect["Destruction"]["Condition"] == "None":
                if "Lose_HP" in card.effect["Destruction"]["Event"]["Do"].keys():
                    for _ in range(
                            card.effect["Destruction"]["Event"]["Do"]["Lose_HP"]["Amount"]
                    ):
                        if (
                                card.effect["Destruction"]["Event"]["Do"]["Lose_HP"][
                                    "Owner"
                                ]
                                == "Player"
                        ):
                            self.draw_hp()
                        else:
                            self.other_player.draw_hp()

    def effect_spell(self, card: Spell) -> None:
        """ Trigger the effect of a spell

        :param card : spell
        """

        if "Spell" in card.effect.keys():
            if card.effect["Spell_effect"]["Condition"] == "None":
                print("No condition")
            else:
                if "Heal" in card.effect["Spell_effect"]["Event"]["Do"].keys():
                    target = card.effect["Spell_effect"]["Event"]["Target"]
                    if target["Amount"] == "All" and target["Attribute"] == "Creatures":
                        if target["Owner"] == "Both":
                            for i in range(len(self.board)):
                                for j in range(len(self.board[0])):
                                    card_targeted = self.board[i][j]
                                    if isinstance(card_targeted, Monster):
                                        card_targeted.life = 2

    def empty_purgatory(self) -> None:
        """
            Transfer monsters in the purgatory to the graveyard
            if they are dead and activate the destruction effect
        """

        storage = deque([])
        storage_size = 0
        for _ in range(self.board.purgatory.size):
            card_purgatory = self.board.purgatory.draw()
            # One should apply here the effect on the card
            if card_purgatory.owner == self.owner:
                self.effect_destruction(card_purgatory)
                self.grave.add(card_purgatory)
            else:
                storage_size += 1
                storage.append(card_purgatory)
        for _ in range(storage_size):
            self.board.purgatory.add(storage.pop())

    def my_undamaged_monsters(self) -> list:
        """ Return a list of the undamaged monsters of the player """
        monsters = []
        for line in self.lines:
            for col in [0, 1, 2]:
                if isinstance(self.board.get_monster((line, col)), Monster):
                    if self.board.get_monster((line, col)).life == 2:
                        monsters.append(self.board.get_monster((line, col)))
        return monsters

    def play(self, j: int, coord: tuple = (0, 0)) -> None:
        """ Play a card from the player's hand on the board

        :param j : index of the card
        :param coord : coordinates
        """

        card_played = self.hand.play(j)
        if isinstance(card_played, Monster):
            if "Impact" in card_played.effect.keys():
                target_list = self.other_player.my_undamaged_monsters()
                random.shuffle(target_list)
                if "Target" in card_played.effect["Impact"]["Event"].keys():
                    max_target = card_played.effect["Impact"]["Event"]["Target"]["Amount"]
                    self.effect_impact(card_played, target_list[:min(len(target_list), max_target)])
                else:
                    self.effect_impact(card_played)
                self.board.clean()
                self.empty_purgatory()
                self.other_player.empty_purgatory()
            self.board.play(card_played, coord)
        if isinstance(card_played, Spell):
            self.effect_spell(card_played)
