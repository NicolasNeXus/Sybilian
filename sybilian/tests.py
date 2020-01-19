# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 15:47:08 2020

@author: clari
"""

import unittest
from cards import *
from deck import *
from board import *
from player import *
from game import *

class TestCanPlayMonster(unittest.TestCase):
    """ Test about the method can_play_monster """
    
    def setUp(self):
        """ Game with an empty board """
        self.game = Game()

    def test_play_monster_OK(self):
        """ Test to verify that the monster is played at the actual coordinates """
        player_playing = self.game.players[self.game.index]
        for line in player_playing.lines:
            for col in [0, 1, 2]:
                test = self.game.can_play_monster(player_playing.owner, 0, (line, col))
                self.assertTrue(test)
                self.assertIsInstance(self.game.board.get_monster((line, col)), Monster)
                self.assertEqual(self.game.board.get_monster((line, col)).coord, (line, col))
                self.assertEqual(player_playing.hand.size, 3)
                self.assertEqual(self.game.nb_actions, 1)
                # Initialisation
                player_playing.hand.add(self.game.board.get_monster((line, col)))
                self.game.board.grid[line][col] = Placeholder()
                self.game.nb_actions = 2
    
    def test_play_monster_notOK(self):
        """ Test to verify that the monster is not played when the conditions are no respected """
        player_playing = self.game.players[self.game.index]
        opponent = self.game.players[(self.game.index + 1)% 2]

        # The monster is not played when the owner is not the player playing
        for line in player_playing.lines:
            for col in [0, 1, 2]:
               test = self.game.can_play_monster(opponent.owner, 0, (line, col))
               self.assertFalse(test)
               self.assertIsInstance(self.game.board.get_monster((line, col)), Placeholder)
               self.assertEqual(player_playing.hand.size, 4)
               self.assertEqual(self.game.nb_actions, 2)

        # The monster is not played when the coordinates are not valid
        for line in opponent.lines:
            for col in [0, 1, 2]:
               test = self.game.can_play_monster(player_playing.owner, 0, (line, col))
               self.assertFalse(test)
               self.assertIsInstance(self.game.board.get_monster((line, col)), Placeholder)
               self.assertEqual(player_playing.hand.size, 4)
               self.assertEqual(self.game.nb_actions, 2)
   
        # The monster is not played when the spot is not empty
        for line in player_playing.lines:
            for col in [0, 1, 2]:
                self.game.can_play_monster(player_playing.owner, 0, (line, col))
                test = self.game.can_play_monster(player_playing.owner, 0, (line, col))
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
                test = self.game.can_play_monster(player_playing.owner, 0, (line, col))
                self.assertFalse(test)
                self.assertIsInstance(self.game.board.get_monster((line, col)), Placeholder)
                self.assertEqual(player_playing.hand.size, 4)
                self.assertEqual(self.game.nb_actions, 0)
                
class TestCanDrawCard(unittest.TestCase):
    """ Test about the method can_draw_card """
    
    def setUp(self):
        """ Game with an empty board """
        self.game = Game()
    
    def test_draw_card_OK(self):
        """ Test to verify that card is drawn from the deck """
        player_playing = self.game.players[self.game.index]
        nb_cards_deck = player_playing.deck.size
        
        # The player's hand is not full
        test = self.game.can_draw_card(player_playing.owner)
        self.assertTrue(test[0])
        self.assertEqual(player_playing.deck.size, nb_cards_deck - 1)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 5)
        self.assertEqual(self.game.nb_actions, 1)

        # The player's hand is full
        for k in range(5):
            player_playing.hand.add(player_playing.deck.draw())
        nb_cards_deck = player_playing.deck.size

        test = self.game.can_draw_card(player_playing.owner)
        self.assertTrue(test[0])
        self.assertEqual(player_playing.deck.size, nb_cards_deck - 1)
        self.assertEqual(player_playing.grave.size, 1)
        self.assertEqual(player_playing.hand.size, 10)
        self.assertEqual(self.game.nb_actions, 0)
    
    def test_draw_card_notOK(self):
        """ Test to verify that card is not drawn when the conditions are not respected """
        player_playing = self.game.players[self.game.index]
        nb_cards_player_deck = player_playing.deck.size
        opponent = self.game.players[(self.game.index + 1) % 2]
        nb_cards_opponent_deck = opponent.deck.size
        
        # The card is not drawn when it's from the opponent deck
        test = self.game.can_draw_card(opponent.owner)
        self.assertFalse(test[0])
        self.assertEqual(opponent.deck.size, nb_cards_opponent_deck)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 4)
        self.assertEqual(self.game.nb_actions, 2)
        
        # The card is not drawn when the player don't have any actions left
        self.game.nb_actions = 0

        test = self.game.can_draw_card(player_playing.owner)
        self.assertFalse(test[0])
        self.assertEqual(player_playing.deck.size, nb_cards_player_deck)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 4)
        self.assertEqual(self.game.nb_actions, 0)

        # The card is not drawn when the deck is empty
        while player_playing.deck.size > 0:
            player_playing.deck.draw()
        self.game.nb_actions = 2

        test = self.game.can_draw_card(player_playing.owner)
        self.assertFalse(test[0])
        self.assertEqual(player_playing.deck.size, 0)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 4)
        self.assertEqual(self.game.nb_actions, 2)

class TestCanDrawHp(unittest.TestCase):
    """ Test about the method can_draw_card """
    
    def setUp(self):
        """ Game with an empty board """
        self.game = Game()
    
    def test_draw_hp_OK(self):
        """ Test to verify that card is drawn from the life """
        player_playing = self.game.players[self.game.index]

        # The player's hand is not full
        test = self.game.can_draw_hp(player_playing.owner)
        self.assertTrue(test[0])
        self.assertEqual(player_playing.life.size, 8)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 5)
        self.assertEqual(self.game.nb_actions, 1)
        self.assertEqual(player_playing.life_points, 9)

        # The player's hand is full
        for k in range(5):
            player_playing.hand.add(player_playing.deck.draw())

        test = self.game.can_draw_hp(player_playing.owner)
        self.assertTrue(test[0])
        self.assertEqual(player_playing.life.size, 7)
        self.assertEqual(player_playing.grave.size, 1)
        self.assertEqual(player_playing.hand.size, 10)
        self.assertEqual(self.game.nb_actions, 0)
        self.assertEqual(player_playing.life_points, 8)
    
    def test_draw_hp_notOK(self):
        """ Test to verify that card is not drawn when the conditions are not respected """
        player_playing = self.game.players[self.game.index]
        opponent = self.game.players[(self.game.index + 1) % 2]
        
        # The card is not drawn when it's from the opponent deck
        test = self.game.can_draw_hp(opponent.owner)
        self.assertFalse(test[0])
        self.assertEqual(opponent.life.size, 9)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 4)
        self.assertEqual(self.game.nb_actions, 2)
        self.assertEqual(player_playing.life_points, 10)
        
        # The card is not drawn when the player don't have any actions left
        self.game.nb_actions = 0

        test = self.game.can_draw_hp(player_playing.owner)
        self.assertFalse(test[0])
        self.assertEqual(player_playing.life.size, 9)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 4)
        self.assertEqual(self.game.nb_actions, 0)
        self.assertEqual(player_playing.life_points, 10)

        # The card is not drawn when the life is empty
        while player_playing.life.size > 0:
            player_playing.life.draw()
        self.game.nb_actions = 2

        test = self.game.can_draw_hp(player_playing.owner)
        self.assertFalse(test[0])
        self.assertEqual(player_playing.life.size, 0)
        self.assertEqual(player_playing.grave.size, 0)
        self.assertEqual(player_playing.hand.size, 4)
        self.assertEqual(self.game.nb_actions, 2)       


class TestCanAttackMonster(unittest.TestCase):
    """ Test about the method can_attack_monster """
    
    def setUp(self):
        """ Game with an empty board and cards without any effects """
        self.game = Game()
        for k in range(4):
            self.game.players[0].hand.container[k].effect = {}
            self.game.players[1].hand.container[k].effect = {}

    def test_can_attack_monster_OK(self):
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
                        test1 = self.game.can_attack_monster(player_playing.owner, (line1, col1), opponent.owner, (line2, col2))
                        self.assertTrue(test1)
                        self.assertEqual(self.game.board.get_monster((line1, col1)).life, 1)
                        self.assertEqual(self.game.board.get_monster((line2, col2)).life, 1)
                        # Test second attack
                        test2 = self.game.can_attack_monster(player_playing.owner, (line1, col1), opponent.owner, (line2, col2))
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
    
#    def test_can_attack_monster_notOK(self):
#        """ Test to verify that the monster is not attacked when the conditions
#        are not respected 
#        """ 
#        player_playing = self.game.players[self.game.index]
#        opponent = self.game.players[(self.game.index + 1) % 2]

class TestImpact(unittest.TestCase):
    """ Test of the effect of impact of the Geonaut """  
    
    def setUp(self):
        """ Game with an undamaged monster which has no special effects on the
        opponent's board 
        """
        self.game = Game()
        self.game.players[1].hand.container[0].effect = {}
        self.game.players[1].play(0, (2, 0))
    
    def test_impact(self):
        player_playing = self.game.players[self.game.index]
        self.game.can_play_monster(player_playing.owner, 0, (0, 0))
        self.assertEqual(self.game.board.get_monster((0, 0)).life, 2)
        self.assertEqual(self.game.board.get_monster((2, 0)).life, 1)

class TestDestruction(unittest.TestCase):
    """ Test of the effect of destruction """
    
    
        
        
         
        
             
        
        


                
        

        
if __name__ == "__main__":
    unittest.main()