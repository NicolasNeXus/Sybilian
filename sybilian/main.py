from cards import *
from deck import *
from board import *
from player import *

board = Board()
# player_one has access to the first and second lines of the board
# player_two has access to the third and fourth lines of the board
player_one = Player("draft_bleu.csv", board, [0, 1], 2)
player_two = Player("draft_rouge.csv", board, [2, 3], 1)
player_one.other_player = player_two
player_two.other_player = player_one


player_one.play(2,(1,0))
player_two.play(2,(3,0))
print(board)
player_one.attack_player_with_monster(board.grid[1][0], player_two)
#player_one.attack_player_with_monster(board.grid[1][0], player_two)
player_two.attack_monster(board.grid[3][0], board.grid[1][0])

