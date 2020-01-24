from cards import *
from deck import *
from board import *
from player import *
from game import *

game = Game()
print(game.players[0].hand)
print(game.players[1].hand)
#game.players[0].play(0, (0, 0))
#print(game.board)
#game.can_play_monster(game.players[game.index].owner, 0, (0, 0))
#game.game_loop()
