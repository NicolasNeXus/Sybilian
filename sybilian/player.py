"""
    This file defines the class Player
    which is the one of the key element of
    our game.
"""

from cards import *
from deck import *
from board import *
from bdd import *


class Player:
    """
        The Player is the main class of our game.
        It can access the board, play cards and
        attack the other player with his cards.
    """
    def __init__(self, deck_name: str, board: Board, lines: list) -> None:
        """
            Each player has a name, which is linked to
            the name of the deck, and has 3 3 keys elements
            which are a Life, a Hand and a Graveyard.
            The player knows the other player as well.
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
            self.draw_hp()

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

    @
    def create_deck(self, deck_name: str):
        """
            Create the deck of the player
            according to the name of the
            deck
        """
        return csv_to_deck(deck_name)

    def attack_monster(self, card: Monster, other_card: Monster) -> None:
        """
            Attack the other Monster
            on the board directly. We put
            the cards into the purgatory
            and we clean the board aswell.
            We then empty the purgatory to
            activate the effects
        """
        card.attack(other_card)
        self.board.clean()
        self.empty_purgatory()
        self.other_player.empty_purgatory()

    def verify_first_line_opponent_empty(self) -> bool:
        """
            Verify that the first line on the board
            of the opponent is empty
            Return True if it's empty
        """
        empty = not isinstance(
            self.board.grid[self.other_player.lines[0]][0], Monster)
        for i in range(1, 3):
            empty = empty and not isinstance(
                self.board.grid[self.other_player.lines[0]][i], Monster
            )
        return empty

    def attack_player_with_monster(self, card: Monster, other_player: Player) -> None:
        """
            Attack the other player
            directly.
        """
        other_player.draw_hp()
        card.life -= 1
        self.board.clean()
        self.empty_purgatory()

    def effect_impact(self, card: Monster, targets: list = [Placeholder()]) -> None:
        """
            Trigger impact effect of a card
            it takes an optionnal target
        """
        if "Impact" in card.effect.keys():
            if cards.effect["Impact"]["Condition"] == "None":
                if "Damage" in card.effect["Impact"]["Condition"]["Event"]["Do"]:
                    if "Target" == card.effect["Impact"]["Condition"]["Event"]["Do"][
                            "Damage"
                    ] and isinstance(Target, Monster):
                        if (
                                card.effect["Impact"]["Condition"]["Event"]["Target"][
                                    "Owner"
                                ]
                                == "Both"
                        ):
                            for i in range(
                                    min(
                                        card.effect["Impact"]["Condition"]["Event"][
                                            "Amount"
                                            ],
                                        len(targets),
                                    )
                            ):
                                card_targeted = targets[i]
                                if (
                                        card.effect["Impact"]["Condition"]["Event"][
                                            "Attribute"
                                        ]
                                        == "Undamaged"
                                        and card_targeted.life == 2
                                ):
                                    card_targeted.life -= (
                                        1
                                    )  # works because it's a reference
                                    # no need to return a card

    def effect_destruction(
            self, card: Monster, targets: list = [Placeholder()]
    ) -> None:
        """
            Trigger the desctruction
            effect or a card.
            it takes an optionnal
            target
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
        """
            Trigger the effect
            of a spell
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
            Put the monsters within the
            purgatory in the graveyard
            if and only if they are
            dead. It also triggers
            the destruction effect
        """
        storage = deque([])
        storage_size = 0
        for _ in range(self.board.purgatory.size):
            card_purgatory = self.board.purgatory.draw()
            print(card_purgatory.owner)
            print(self.owner)
            # One should apply here the effect on the card
            if card_purgatory.owner == self.owner:
                self.effect_destruction(card_purgatory)
                self.grave.add(
                    card_purgatory
                )  # après regarder si ya les effets de destruction...
            # c'est les cartes de l'adversaire on les "réempile" dans le purgatoire
            else:
                storage_size += 1
                storage.append(card_purgatory)
        for _ in range(storage_size):
            self.board.purgatory.add(storage.pop())

    def play(self, index_card: int, coord: tuple = (0, 0)) -> None:
        """
            The player plays a card from
            its hand on the board at the
            position coord
        """
        card_played = self.hand.play(index_card)
        if isinstance(card_played, Monster):
            if "Impact" in card_played.effect.keys():
                impacted = int(
                    input(
                        "Voulez-vous utiliser l'effet d'impact ? 1 pour oui, 0 pour non"
                    )
                )
                if impacted:
                    if (
                            "Target"
                            in card_played.effect["Impact"]["Condition"]["Event"].keys()
                    ):
                        target_list = []
                        for i in range(
                                card_played.effect["Impact"]["Condition"]["Event"]["Amount"]
                        ):
                            x_impact = int(
                                input("Ligne du montre qui est visé par l'impact")
                            )
                            y_impact = int(
                                input(
                                    "Colonne du monstre qui est visé par l'impact")
                            )
                            target_list.append(
                                self.board.grid[x_impact][y_impact])
                effect_impact(card_played, target_list)
            self.board.play(card_played, coord)
        if isinstance(card_played, Spell):
            self.effect_spell(card_played)
