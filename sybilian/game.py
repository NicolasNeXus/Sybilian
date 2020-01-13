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
    def __init__(self, app : QApplication) -> None:
        super().__init__()
        self.board = Board()
        # player_one has access to the first and second lines of the board
        # player_two has access to the third and fourth lines of the board
        self.players = (Player("deckA005.csv", self.board, [0, 1], 2, self), Player("deckB001.csv", self.board, [2, 3], 1, self))
        self.players[0].other_player = self.players[1]
        self.players[1].other_player = self.players[0]
        self.nb_turns = 0
        self.nb_actions = 2 # possible actions during a turn
        self.end = False
        self.ongo_attack = False
        
        
        self.finish_turn = QPushButton('FINISH YOUR TURN', self) # button to finish your turn
        self.setMouseTracking(True) # mouse tracking on the screen
        self.setAcceptDrops(True)
        self.initUi()
        self.position = [[QRect(150*j + 100, 100 + 150 * i, 50, 100) for j in range(3)] for i in range(2)] + [[QRect(150*j + 100, 400 + 150 * i, 50, 100) for j in range(3)] for i in range(2)]
        self.color = [[QColor(255, 0, 0, 200) for j in range(3)] for i in range(2)] + [[QColor(0, 0, 255, 200) for j in range(3)] for i in range(2)]
        self.grid = [[Placeholder for j in range(3)] for i in range(2)] + [[Placeholder for j in range(3)] for i in range(2)]
        self.name_player = [["Joueur1" for j in range(3)]for i in range(2)] + [["Joueur2" for j in range(3)]for i in range(2)]
        self.initHand()
        self.initLife()
        self.index_current_card = -1
        self.qapp = app
        self.player_medal = [QRect(0, 0, 100, 50), QRect(0, 850, 100, 50)]
        self.color_players = [QColor(255, 0, 0, 200), QColor(0, 0, 255, 200)]
    
    def initLife(self) -> None:
        # display life points for the 2 players
        for i in range(2):
            player = self.players[i]
            for j in range(player.life.size):
                card = player.life.container[j]  
                card.setPixmap(QPixmap("hidden_card.png"))
                card.move(550, 300*i + 100 + 25*j)
                card.show()
    
    def initHand(self) -> None:
        # display the hand of the current player
        player = self.players[self.nb_turns%2] # current player
        for i in range(len(player.hand.container)):
            card = player.hand.container[i]  
            card.setPixmap(QPixmap("monster.png"))
            card.move(20 + 70*i, 700)
            card.show()
    
    def clearHand(self) -> None:
        # erase (graphically) the hand of the current player
        player = self.players[self.nb_turns%2] # current player
        print("Main", len(player.hand.container))
        for i in range(len(player.hand.container)):
            card = player.hand.container[i]  
            card.hide()
            
    def clearLife(self) -> None:
        # erase (graphically) the life of the current player
        for i in range(2):
            player = self.players[i]
            for j in range(player.life.size):
                card = player.life.container[j]  
                card.hide()
    
    def initUi(self) -> None:
        # event for changing turns 
        def change_turn():
            # mettre fin au tour
            self.nb_actions = 2
            self.ongo_attack = False
            self.clearHand()
            self.clearLife()
            self.end = self.condition_endgame() # mise a jour de la condition end
            self.players[self.nb_turns%2].draw_hp()
            self.nb_turns += 1
            self.initHand()
            self.initLife()
            
        
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

    # est-ce qu'on a le droit de prendre cette carte dans la main ?
    def back_take_card_from_hand(self, player : str, index_card : int) -> bool:
        return(True)

    def dragEnterEvent(self, e):
        for i in range(len(self.players[self.nb_turns%2].hand.container)):
            card = self.players[self.nb_turns%2].hand.container[i]
            if QRect(card.x(), card.y(), card.width, card.height).contains(e.pos()):
                self.index_current_card = i
        if self.back_take_card_from_hand(self.hand[], self.index_current_card):
            e.accept()
              
    def move_card_from_hand_to_board(self, index_current_card : int, position : tuple) -> None:
        self.players[self.nb_turns%2].hand.container[self.index_current_card].move(self.position[position[0]][position[1]].x(), self.position[position[0]][position[1]].y())
        self.index_current_card = -1

    # est-ce que j'ai le droit de jouer cette carte de ma main ?
    def back_play_card_from_hand(self, player : str, index_card : int, card : Card, pos : tuple) -> bool:
        return(True)

    # to play cards on the board (drag'n'drop) --> Jouer des cartes sur le plateau
    def dropEvent(self, e):
        position = e.pos()
        for i in range(len(self.board.grid)):
            for j in range(len(self.board.grid[0])):
                if self.position[i][j].contains(position):
                    pos = (i, j)
                    if self.back_play_card_from_hand(self.name_player[self.index_current_card], self.index_current_card) :
                        self.move_card_from_hand_to_board(self.players[self.nb_turns%2], self.index_current_card, pos)
                        e.setDropAction(Qt.MoveAction)
                        e.accept() 
        self.update()
            
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
        
        # dessiner les joueurs
        for i in range(len(self.player_medal)):
            painter.fillRect(self.player_medal[i], self.color_players[i])
        painter.end()

    # possibilité d'attaquer via la position sur la grille
    def back_card_that_attack(self, pos : tuple) -> bool: 
        return(True)
    
    def back_monster_could_be_attacked(self, pos_board : tuple, pos : tuple) -> bool:
        return(True)
        
    def back_player_could_be_attacked(self, pos_board : tuple, player : str) -> bool:
        return(True)

    # attack of a monster --> Attaquer monstres ou joueurs
    def mouseReleaseEvent(self, e):
        x, y = -1, -1
        x_att, y_att = -1, -1
        position = e.pos()
        attack_instance = None
        attacked_instance = None
        if self.nb_turns > 1: # pas le premier tour pour qu'on puisse attaquer
            # Y-a-til un clic sur le Board ?
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    if self.position[i][j].contains(position):
                        if not self.ongo_attack: # pas encore d'attaque
                            x, y = i, j
                            if self.back_card_that_attack((x, y)):
                                self.ongo_attack = True
                                self.color[i][j].setAlpha(50)
                                self.qapp.setOverrideCursor(Qt.CrossCursor) # curseur cible
                        else: # attaque en cours
                            x_att, y_att = i, j # coord de la carte attaquée
                            if self.back_monster_could_be_attacked((x, y), (x_att, y_att)): # monstre peut être attaqué ?                       
                                self.color[i][j] = QColor(105, 105, 105, 200)
                            self.players[self.nb_turns%2].attack_monster(self.grid[x][y], self.grid[x_other_player][y_other_player])
                            self.ongo_attack = False
                            
                            if self.grid[x_other_player][y_other_player].life > 0:
                                self.color[i][j] = QColor(105, 105, 105, 200)
                            else:
                                if self.nb_turns%2 == 0:
                                    self.color[i][j] = QColor(0, 0, 255, 200)
                                else:
                                    self.color[i][j] = QColor(255, 0, 0, 200)
                            self.qapp.restoreOverrideCursor()
        
            # Y-a-t-il un clic sur un Player ?
            for i in range(len(self.player_medal)):
                if self.player_medal[i].contains(position):
                    if self.ongo_attack: # attaque en cours
                        if self.back_player_could_be_attacked(self.player_medal[i]): # joueur peut être attaqué ?
                            attack_player()
        self.update()          