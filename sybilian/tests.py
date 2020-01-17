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

    def test_play_monster_empty_board(self):
        """ Test to verify that we play a monster """
        print(self.game.board)
        print(self.game.players[0].hand)
        test = self.game.can_play_monster(self.game.players[self.game.index].owner, 0, (0, 0))
        self.assertTrue(test)
#        player_playing = self.game.players[self.game.index]
#        for line in player_playing.lines:
#            for col in [0, 1, 2]:
#                print((line, col))
#                test = self.game.can_play_monster(player_playing.owner, 0, (line, col))
#                self.assertTrue(test)
#                self.assertIsInstance(self.game.board.get_monster((line, col)), Monster)
#                self.assertEqual(self.game.board.get_monster((line, col)).coord, (line, col))
#                player_playing.hand.add(self.game.board.get_monster((line, col)))
#                self.game.board[line][col] = Placeholder()
        
if __name__ == "__main__":
    unittest.main()