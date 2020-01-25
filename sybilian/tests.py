# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 15:47:08 2020

@author: clari
"""

import unittest
from cards import Monster, Placeholder
from game import Game


class TestCanPlayMonster(unittest.TestCase):
    """ Test about the method can_play_monster """

    def setUp(self):
        """ Game with an empty board """
        self.game = Game()

    def test_play_monster_ok(self):
        """
            Test to verify that the monster is played at the actual coordinates
        """

        player_playing = self.game.players[self.game.index]
        for line in player_playing.lines:
            for col in [0, 1, 2]:
                test = self.game.can_play_monster(0, (line, col))[0]
                self.assertTrue(test)
                self.assertIsInstance(self.game.board.get_monster((line, col)), Monster)
                self.assertEqual(self.game.board.get_monster((line, col)).coord, (line, col))
                self.assertEqual(player_playing.hand.size, 3)
                self.assertEqual(self.game.nb_actions, 1)
                # Re-initialisation
                player_playing.hand.add(self.game.board.get_monster((line, col)))
                self.game.board.grid[line][col] = Placeholder()
                self.game.nb_actions = 2

    def test_play_monster_not_ok(self):
        """
            Test to verify that the monster is not played when the conditions
            are no respected
        """

        player_playing = self.game.players[self.game.index]
        opponent = self.game.players[(self.game.index + 1)% 2]

        # The monster is not played when the coordinates are not valid
        for line in opponent.lines:
            for col in [0, 1, 2]:
                test = self.game.can_play_monster(0, (line, col))[0]
                self.assertFalse(test)
                self.assertIsInstance(self.game.board.get_monster((line, col)), Placeholder)
                self.assertEqual(player_playing.hand.size, 4)
                self.assertEqual(self.game.nb_actions, 2)

        # The monster is not played when the spot is not empty
        for line in player_playing.lines:
            for col in [0, 1, 2]:
                self.game.can_play_monster(0, (line, col))
                test = self.game.can_play_monster(0, (line, col))[0]
                self.assertFalse(test)
                self.assertEqual(player_playing.hand.size, 3)
                self.assertEqual(self.game.nb_actions, 1)
                # Initialisation
                player_playing.hand.add(self.game.board.get_monster((line, col)))
                self.game.board.grid[line][col] = Placeholder()
                self.game.nb_actions = 2

        # The monster is not played when the player don't have any actions left
        self.game.nb_actions = 0
        for line in player_playing.lines:
            for col in [0, 1, 2]:
                test = self.game.can_play_monster(0, (line, col))[0]
                self.assertFalse(test)
                self.assertIsInstance(self.game.board.get_monster((line, col)), Placeholder)
                self.assertEqual(player_playing.hand.size, 4)
                self.assertEqual(self.game.nb_actions, 0)


class TestCanDrawCard(unittest.TestCase):
    """ Test about the method can_draw_card """

    def setUp(self):
        """ Game with an empty board """
        self.game = Game()

    def test_draw_card_from_deck_ok(self):
        """ Test to verify that card is drawn from the deck """
        player_playing = self.game.players[self.game.index]
        nb_cards_deck = player_playing.deck.size

        # The player's hand is not full and the deck is not empty
        test = self.game.can_draw_card()[0]
        self.assertTrue(test)
        self.assertEqual(player_playing.deck.size, nb_cards_deck - 1)
        self.assertEqual(player_playing.life.size, 9)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 5)
        self.assertEqual(self.game.nb_actions, 1)

        # The player's hand is full and the deck is not empty
        for _ in range(5):
            player_playing.hand.add(player_playing.deck.draw())
        nb_cards_deck = player_playing.deck.size

        test = self.game.can_draw_card()[0]
        self.assertTrue(test)
        self.assertEqual(player_playing.deck.size, nb_cards_deck - 1)
        self.assertEqual(player_playing.life.size, 9)
        self.assertEqual(player_playing.grave.size, 1)
        self.assertEqual(player_playing.hand.size, 10)
        self.assertEqual(self.game.nb_actions, 0)

    def test_draw_card_from_hp_ok(self):
        """ Test to verify that card is drawn from the life """
        player_playing = self.game.players[self.game.index]

        # The player's hand is full and the deck is empty
        for _ in range(5):
            player_playing.hand.add(player_playing.deck.draw())

        while player_playing.deck.size > 0:
            player_playing.deck.draw()

        test = self.game.can_draw_card()[0]
        self.assertTrue(test)
        self.assertEqual(player_playing.deck.size, 0)
        self.assertEqual(player_playing.life.size, 8)
        self.assertEqual(player_playing.life_points, 9)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 10)
        self.assertEqual(self.game.nb_actions, 1)

        # The player's hand is not full and the deck is empty
        player_playing.hand.container.pop()

        test = self.game.can_draw_card()[0]
        self.assertTrue(test)
        self.assertEqual(player_playing.deck.size, 0)
        self.assertEqual(player_playing.life.size, 7)
        self.assertEqual(player_playing.life_points, 8)
        self.assertEqual(player_playing.grave.size, 1)
        self.assertEqual(player_playing.hand.size, 10)
        self.assertEqual(self.game.nb_actions, 0)

    def test_draw_card_not_ok(self):
        """ Test to verify that card is not drawn when the conditions are not respected """
        player_playing = self.game.players[self.game.index]
        nb_cards_player_deck = player_playing.deck.size

        # The card is not drawn when the player don't have any actions left
        self.game.nb_actions = 0

        test = self.game.can_draw_card()[0]
        self.assertFalse(test)
        self.assertEqual(player_playing.deck.size, nb_cards_player_deck)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 4)
        self.assertEqual(self.game.nb_actions, 0)


class TestCanAttackMonster(unittest.TestCase):
    """ Test about the method can_attack_monster """

    def setUp(self):
        """ Game with an empty board and cards without any effects """
        self.game = Game()
        for k in range(4):
            self.game.players[0].hand.container[k].effect = {}
            self.game.players[1].hand.container[k].effect = {}

    def test_can_attack_monster_ok(self):
        """ Test to verify that the monster is attacked """
        player_playing = self.game.players[self.game.index]
        opponent = self.game.players[(self.game.index + 1) % 2]
        # Intialisation
        for line1 in player_playing.lines:
            for col1 in [0, 1, 2]:
                for line2 in opponent.lines:
                    for col2 in [0, 1, 2]:
                        player_playing.play(0, (line1, col1))
                        opponent.play(0, (line2, col2))
                        # Test first attack
                        test1 = self.game.can_attack_monster((line1, col1), (line2, col2))[0]
                        self.assertTrue(test1)
                        self.assertEqual(self.game.board.get_monster((line1, col1)).life, 1)
                        self.assertEqual(self.game.board.get_monster((line2, col2)).life, 1)
                        # Test second attack
                        test2 = self.game.can_attack_monster((line1, col1), (line2, col2))[0]
                        self.assertTrue(test2)
                        self.assertIsInstance(self.game.board.get_monster((line1, col1)), Placeholder)
                        self.assertIsInstance(self.game.board.get_monster((line2, col2)), Placeholder)
                        self.assertEqual(player_playing.grave.size, 1)
                        self.assertEqual(opponent.grave.size, 1)
                        # Re-initialisation of the test
                        card1 = player_playing.grave.grab(0)
                        card1.life = 2
                        card2 = opponent.grave.grab(0)
                        card2.life = 2
                        player_playing.hand.add(card1)
                        opponent.hand.add(card2)

    def test_can_attack_monster_not_ok(self):
        """
            Test to verify that the monster on the second line is not attacked
            when the conditions are not respected
        """

        player_playing = self.game.players[self.game.index]
        opponent = self.game.players[(self.game.index + 1) % 2]

        # The first line of the opponent is not empty
        opponent.play(0, (opponent.lines[0], 0))
        opponent.play(0, (opponent.lines[1], 0))

        player_playing.play(0, (player_playing.lines[0], 0))

        test = self.game.can_attack_monster((player_playing.lines[0], 0), (opponent.lines[1], 0))[0]
        self.assertFalse(test)
        self.assertEqual(self.game.board.get_monster((opponent.lines[1], 0)).life, 2)
        self.assertEqual(self.game.board.get_monster((opponent.lines[0], 0)).life, 2)
        self.assertEqual(self.game.board.get_monster((player_playing.lines[0], 0)).life, 2)


class TestCanAttackOpponentWithMonster(unittest.TestCase):
    """ Test about the method can_attack_opponent_with_monster """

    def setUp(self):
        """ Game with just a monster on player's side of the board """
        self.game = Game()
        self.game.players[0].play(0, (0, 0))

    def test_can_attack_opponent_with_monster_ok(self):
        """
            Test to verify that the opponent is actually attacked when the
            conditions are respected
        """
        opponent = self.game.players[(self.game.index + 1) % 2]
        # The first line of the opponent is empty
        test = self.game.can_attack_opponent_with_monster((0, 0))[0]
        self.assertTrue(test)
        self.assertEqual(opponent.life_points, 9)
        self.assertEqual(opponent.life.size, 8)
        self.assertEqual(opponent.hand.size, 5)
        self.assertEqual(self.game.board.get_monster((0, 0)).life, 1)


class TestImpact(unittest.TestCase):
    """ Test of the effect of impact of the Geonaut """

    def setUp(self):
        """
            Game with an undamaged monster which has no special effects on the
            opponent's board
        """

        self.game = Game()
        self.game.players[1].hand.container[0].effect = {}
        self.game.players[1].play(0, (2, 0))

    def test_impact(self):
        """
            When playing a geonaut an undamaged creature of the opponent should
            be automatically attacked (the attack doeesn't cost an action)
        """

        self.game.can_play_monster(0, (0, 0))
        self.assertEqual(self.game.board.get_monster((0, 0)).life, 2)
        self.assertEqual(self.game.board.get_monster((2, 0)).life, 1)
        self.assertEqual(self.game.nb_actions, 1)


class TestDestruction(unittest.TestCase):
    """ Test of the effect of destruction """

    def setUp(self):
        """
            Game where each player have a monster on the board, one has the
            effect Destruction
        """

        self.game = Game()
        self.game.players[0].hand.container[0].effect = {}
        self.game.players[0].play(0, (0, 0))
        self.game.players[1].hand.container[0].effect = {'Destruction': {'Condition': 'None', 'Event': {'Do': {'Lose_HP': {'Owner': 'Player', 'Amount': 1}}}}}
        self.game.players[1].play(0, (2, 0))

    def test_destruction(self):
        """
            When opponent's monster is destroyed the opponent should lose
            one hp
        """

        player_playing = self.game.players[self.game.index]
        opponent = self.game.players[(self.game.index + 1) % 2]

        self.game.can_attack_monster((0, 0), (2, 0))
        self.game.can_attack_monster((0, 0), (2, 0))
        self.assertIsInstance(self.game.board.get_monster((2, 0)), Placeholder)
        self.assertEqual(opponent.grave.size, 1)
        self.assertIsInstance(self.game.board.get_monster((0, 0)), Placeholder)
        self.assertEqual(player_playing.grave.size, 1)
        self.assertEqual(opponent.life_points, 9)


class TestPowerful(unittest.TestCase):
    """ Test of the powerful effect """

    def setUp(self):
        """ Game """
        self.game = Game()

    def test_powerful_1(self):
        """
            Test of the powerful effect, monster which is attacking is
            powerful, the other one is normal
        """

        opponent = self.game.players[(self.game.index + 1) % 2]

        self.game.players[0].hand.container[0].effect = {'Powerful': 'No_condition'}
        self.game.players[0].play(0, (0, 0))
        self.game.players[1].hand.container[0].effect = {}
        self.game.players[1].play(0, (2, 0))

        self.game.can_attack_monster((0, 0), (2, 0))
        self.assertEqual(self.game.board.get_monster((0, 0)).life, 1)
        self.assertIsInstance(self.game.board.get_monster((2, 0)), Placeholder)
        self.assertEqual(opponent.grave.size, 1)

    def test_powerful_2(self):
        """
            Test of the powerful effect monster which is attacking is normal,
            the other one is powerful
        """

        player_playing = self.game.players[self.game.index]

        self.game.players[0].hand.container[0].effect = {}
        self.game.players[0].play(0, (0, 0))
        self.game.players[1].hand.container[0].effect = {'Powerful': 'No_condition'}
        self.game.players[1].play(0, (2, 0))

        self.game.can_attack_monster((0, 0), (2, 0))
        self.assertEqual(self.game.board.get_monster((2, 0)).life, 1)
        self.assertIsInstance(self.game.board.get_monster((0, 0)), Placeholder)
        self.assertEqual(player_playing.grave.size, 1)

    def test_powerful_3(self):
        """ Test of the powerful effect both monsters are powerful """
        self.game.players[0].hand.container[0].effect = {'Powerful': 'No_condition'}
        self.game.players[0].play(0, (0, 0))
        self.game.players[1].hand.container[0].effect = {'Powerful': 'No_condition'}
        self.game.players[1].play(0, (2, 0))

        self.game.can_attack_monster((0, 0), (2, 0))
        self.assertEqual(self.game.board.get_monster((0, 0)).life, 1)
        self.assertEqual(self.game.board.get_monster((2, 0)).life, 1)


class TestSequence(unittest.TestCase):
    """ Test of a sequence of actions with real cards of the game Sybilian """

    def test(self):
        """ Test of the tree effects combined together """
        game = Game()

        game.index = 1
        # Player 1 play a fury which has a powerful effect and a destruction effect
        game.can_play_monster(0, (2, 0))
        game.can_draw_card()
        game.can_end_turn()

        # Player 0 play a geonaut which has an effect of impact
        game.can_play_monster(0, (0, 0))
        # The fury is attacked without using any actions
        self.assertEqual(game.board.get_monster((2, 0)).life, 1)
        # The geonaut attacks the fury
        game.can_attack_monster((0, 0), (2, 0))
        # The geonaut dies because the fury is powerful
        self.assertIsInstance(game.board.get_monster((0, 0)), Placeholder)
        self.assertEqual(game.players[0].grave.size, 1)
        # The fury dies because it was already hurt
        self.assertIsInstance(game.board.get_monster((2, 0)), Placeholder)
        self.assertEqual(game.players[1].grave.size, 1)
        # Because of the effect of destruction player 1 loses one hp
        self.assertEqual(game.players[1].life_points, 9)


if __name__ == "__main__":
    unittest.main()
