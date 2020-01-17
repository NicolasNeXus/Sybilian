from cards import *
from deck import *
from board import *
from player import *
from game import *

game = Game()
game.can_play_monster(game.players[game.index].owner, 0, (0, 0))
#game.game_loop()
