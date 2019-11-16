from cards import *
from deck import *
from board import *
from player import *

board = Board()
player_one = Player("draft_bleu.csv", board)
player_two = Player("draft_rouge.csv", board)
player_one.other_player = player_two
player_two.other_player = player_one

player_one.play(2,(1,0))
player_two.play(2,(3,0))
print(board)
player_one.attack_player_with_monster(board.grid[1][0], player_two)
#player_one.attack_player_with_monster(board.grid[1][0], player_two)
player_two.attack_monster(board.grid[3][0], board.grid[1][0])

