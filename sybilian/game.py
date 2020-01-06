from PyQt5.QtGui import QColor

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:08:41 2019

@author: clari
"""

from cards import *
from deck import *
from board import *
from player import *

# graphics use
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap, QDrag, QPen, QCursor
import sys

class Game(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.board = Board()
        # player_one has access to the first and second lines of the board
        # player_two has access to the third and fourth lines of the board
        self.players = (Player("deckA005.csv", self.board, [0, 1], 2), Player("deckB001.csv", self.board, [2, 3], 1))
        self.players[0].other_player = self.players[1]
        self.players[1].other_player = self.players[0]
        self.nb_turns = 0
        self.nb_actions = 2 # possible actions during a turn
        self.end = False
        self.ongo_attack = False
        
        self.finish_turn = QPushButton('FINISH YOUR TURN', self) # button to finish your turn
        self.setMouseTracking(True) # mouse tracking on the screen
        self.acceptDrops(True) # drag 'n' drop accepted 
        self.initUi()
        self.position = [[QRect(150*j + 100, 100 + 150 * i, 50, 100) for j in range(3)] for i in range(2)] + [[QRect(150*j + 100, 400 + 150 * i, 50, 100) for j in range(3)] for i in range(2)]
        self.color = [[QColor(255, 0, 0, 200) for j in range(3)] for i in range(2)] + [[QColor(0, 0, 255, 200) for j in range(3)] for i in range(2)]
        
    def iniUi(self) -> None:
        # event for changing turns 
        def change_turn():
            # mettre fin au tour
            self.nb_actions = 2
            self.ongo_attack = False
            self.nb_turns += 1
            self.end = self.condition_endgame()
        
        self.finish_turn.move(700, 300)
        self.finish_turn.clicked.connect(change_turn)
        # main window
        self.setWindowTitle('GAME')
        self.setGeometry(50, 50, 900, 900)
    
    def condition_endgame(self) -> bool:
        """
            return True if a player won,
            False otherwise
        """
        if self.players[0].life_points > 0 and self.players[1].life_points > 0:
            return False
        elif self.players[0].life_points == 0:
            print("Le joueur 2 a gagné!")
            return True
        elif self.players[1].life_points == 0:
            print("Le joueur 1 a gagné!")
            return True

    def dragEnterEvent(self, e):
        e.accept()
              
    # to play cards on the board (drag'n'drop)
    def dropEvent(self, e):
        position = e.pos()
        for i in range(len(self.board.grid)):
            for j in range(len(self.board.grid[0])):
                if self.position[i][j].contains(position):
                    self.players[self.nb_turns%2].play(0, (i, j))
                    self.nb_actions -= self.board.grid[i][j].price
                    self.players[self.nb_turns%2].hand.container[0].move(self.position[i][j].x(), self.position[i][j].y())
                    e.setDropAction(Qt.MoveAction)
                    e.accept()                    
                                    
    
    def game_loop(self):
        while not self.end:
            print('EN COURS')
#            while self.nb_actions > 0:
#                self.turn()
            #self.nb_turns += 1
            
    ### GRAPHICS USE ###
    
    # color the areas where players put their cards
    def paintEvent(self, e):
        painter = QPainter(self)
        # display the board
        for i in range(len(self.board.grid)):
            for j in range(len(self.board.grid[0])):
                painter.eraseRect(self.position[i][j])
                # black borders with a 3-width pen
                pen = QPen(Qt.black)
                pen.setWidth(3)
                painter.setPen(pen)
                painter.drawRect(self.position[i][j])
                painter.fillRect(self.position[i][j], self.color[i][j])
        # display the hand of the current player
        player = self.players[self.nb_turns%2]
        for i in range(len(player.hand.container)):
            Cards 
            player.hand.container[i].setPixmap()
        painter.end()

    
    # attack of a monster
    def mouseReleaseEvent(self, e):
        x = -1
        y = -1
        x_other_player = -1
        y_other_player = -1
        position = e.pos()
        if self.nb_turns > 1:
            for i in range(len(self.board.grid)):
                for j in range(len(self.board.grid[0])):
                    if self.position[i][j].contains(position):
                        if not self.ongo_attack:
                            x = i
                            y = j
                            self.ongo_attack = True
                            self.color[i][j].setAlpha(50)
                            app.setOverrideCursor(Qt.CrossCursor)
                        else:
                            x_other_player = i
                            y_other_player = j
                            self.color[i][j] = QColor(105, 105, 105, 200)
                            self.players[self.nb_turns%2].attack_monster(self.board.grid[x][y], self.board.grid[x_other_player][y_other_player])
                            self.ongo_attack = False
                            if self.board.grid[x_other_player][y_other_player].life > 0:
                                self.color[i][j] = QColor(105, 105, 105, 200)
                            else:
                                if nb_turns%2 == 0:
                                    self.color[i][j] = QColor(0, 0, 255, 200)
                                else:
                                    self.color[i][j] = QColor(255, 0, 0, 200)
                            app.restoreOverrideCursor()
        self.update()          