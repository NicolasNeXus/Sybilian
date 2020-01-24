from PyQt5.QtGui import QColor

from cards import *
from cards_graphic import *
from deck import *
from board import *
from player import *

# graphics use
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap, QDrag, QPen, QCursor, QFont
import sys

from game import *
from cards_graphic import *
from cards import *

class Game_Graphic(QWidget):
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.end = False
        self.ongo_attack = False
        self.current_hand = []
        self.other_hand = []
        self.current_life = []
        self.other_life = []
        self.game = Game()
        self.tour = 0
        self.text_tour = QLabel('Tour : ' + str(self.tour), self)
        self.current_deck = Card_Graphic(Placeholder(), self) 
        self.other_deck = Card_Graphic(Placeholder(), self)
        self.i_card_attacking, self.j_card_attacking = -1, -1
        self.could_be_drag = False

        self.finish_turn = QPushButton('FINISH YOUR TURN', self) # button to finish your turn
        self.setMouseTracking(True) # mouse tracking on the screen
        self.setAcceptDrops(True)
        self.index_current_card = -1
        self.qapp = app
        self.player_medal = [QRect(0, 0, 100, 50), QRect(0, 850, 100, 50)]
        self.color_players = [QColor(255, 0, 0, 200), QColor(0, 0, 255, 200)]
        self.position = [[QRect(150*j + 100, 100 + 150 * i, 50, 100) for j in range(3)] for i in range(2)] + [[QRect(150*j + 100, 400 + 150 * i, 50, 100) for j in range(3)] for i in range(2)]
        self.color = [[QColor(255, 0, 0, 200) for j in range(3)] for i in range(2)] + [[QColor(0, 0, 255, 200) for j in range(3)] for i in range(2)]
        self.grid = [[Placeholder() for j in range(3)] for i in range(2)] + [[Placeholder() for j in range(3)] for i in range(2)]
        self.players = ("Player1", "Player2")
        
        self.initUi() # main window
        self.initHand(self.game.get_current_hand(), self.players[0])
        self.initHand([Placeholder() for i in range(4)], self.players[1])

        self.initLife(9, self.players[0])
        self.initLife(9, self.players[1])
        
        self.initBoard(self.grid)

    # Display player life
    def initLife(self, number_card: int, player_name: str) -> None:
        # display life points for the 2 players
        i = self.players.index(player_name)
        for j in range(number_card):
            card = Card_Graphic(Placeholder(), self)
            card.setPixmap(QPixmap("hidden_card.png"))
            card.move(550, 300*i + 100 + 25*j)
            if player_name == self.players[self.tour%2]:
                self.current_life.append(card)
            else:
                self.other_life.append(card)
            card.show()
    
    # display the board
    def initBoard(self, board: list) -> None:
        for i in range(len(board)):
            for j in range(len(board[0])):
                self.grid[i][j] = Card_Graphic(board[i][j], self)
                if not isinstance(self.grid[i][j].card, Placeholder):
                    self.grid[i][j].setPixmap(QPixmap("monster.png"))
                self.grid[i][j].move(self.position[i][j].x(), self.position[i][j].y())
                self.grid[i][j].show()

    def initHand(self, hand: list, player_name: str) -> None:
        # display the hand of a player
        i = self.players.index(player_name)
        for j in range(len(hand)):
            card = Card_Graphic(hand[j], self)
            if player_name == self.players[self.tour%2]:
                self.current_hand.append(card) 
                card.setPixmap(QPixmap("monster.png"))
            else:
                self.other_hand.append(card)
                card.setPixmap(QPixmap("hidden_card.png"))
            card.move(130 + 70*j, 10 + 700*i)
            card.show()
        print([self.current_hand[i].card for i in range(len(self.current_hand))])
            
    def initDeck(self, player_name: str) -> None:
        i = self.players.index(player_name)
        if player_name == self.players[self.tour%2]:
            card = self.current_deck
        else:
            card = self.other_deck
        card.setPixmap(QPixmap("deck_card.png"))
        card.move(750, 150 + 325*i)
        card.show()

    def clearHand(self, hand: list) -> None:
        # erase (graphically) the hand of the current player
        for i in range(len(hand)):
            card = hand[i]
            card.hide()
            card.setParent(None)
        if self.current_hand == hand:
            self.current_hand = []
        elif self.other_hand == hand:
            self.other_hand = []
    
    # clear board
    def clearBoard(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j].hide()     
                self.grid[i][j].setParent(None)
                
    def clearLife(self, player_name: str) -> None:
        # erase (graphically) the life of a player
        card = None
        if player_name == self.players[self.tour%2]:
            for j in range(len(self.current_life)):
                card = self.current_life[j]
                card.hide()
                card.setParent(None)
        else:
            for j in range(len(self.other_life)):
                card = self.other_life[j]
                card.hide()
                #card.deleteLater()
                card.setParent(None)

    def clearDeck(self, player_name: str) -> None:
        if player_name == self.players[self.tour%2]:
            card = self.current_deck
        else:
            card = self.other_deck
        card.hide()

    def initUi(self) -> None:
        # event for changing turns 
        def change_turn():
            flag_change_turn = self.game.can_end_turn()
            print('flag_turn', flag_change_turn)
            if flag_change_turn[0]:
                self.current_hand, self.other_hand = self.other_hand, self.current_hand
                self.refresh(flag_change_turn)
                self.ongo_attack = False                
                self.tour += 1
                # text to indicate the current tour
                self.text_tour.setText("Tour : " + str(self.tour))
                if self.tour%2 == 0:
                    self.text_tour.setStyleSheet("color: red;")
                else:
                    self.text_tour.setStyleSheet("color: blue;")
                self.end = self.game.condition_endgame()
                if self.end:
                    self.qapp.exec_()

        # button to change turns
        self.finish_turn.move(700, 350)
        self.finish_turn.clicked.connect(change_turn)
        
        # Qlabel that displays the number of the current tour
        self.text_tour.setFont(QFont('SimHei', 20))
        self.text_tour.setStyleSheet("color: red;")
        self.text_tour.move(700, 20)
        
        self.initDeck(self.players[0])
        self.initDeck(self.players[1])

        # main window with its properties
        self.setWindowTitle('Sybilian')
        self.setGeometry(50, 50, 1000, 900)


    def refresh(self, list_area: list) -> None:
        if list_area[1] is not None:
            self.clearHand(self.current_hand)
            self.initHand(list_area[1], self.players[self.tour%2])
        if list_area[2] == 0:
            self.clearDeck(self.current_deck)
        if list_area[3] is not None:
            self.clearLife(self.players[self.tour%2])
            self.initLife(list_area[3], self.players[self.tour%2])
        if list_area[5] is not None:
            self.clearHand(self.other_hand)
            self.initHand([Placeholder() for i in range(list_area[5])], self.players[(self.tour+1)%2])
        if list_area[6] == 0:
            self.clearDeck(self.other_deck)
        if list_area[7] is not None:
            self.clearLife(self.players[(self.tour+1)%2])
            self.initLife(list_area[7], self.players[(self.tour+1)%2])
        if list_area[9] is not None:
            self.clearBoard()
            self.initBoard(list_area[9].grid)

    def dragEnterEvent(self, e):
        e.accept()
        for i in range(len(self.current_hand)):
            card = self.current_hand[i] # chosen card
            print('Etat de la boucle :', i)
            if QRect(card.x(), card.y(), card.width, card.height).contains(e.pos()):
                self.index_current_card = i
                print(i)

    def move_card_from_hand_to_board(self, index_current_card: int, position: tuple) -> None:
        self.current_hand[self.index_current_card].move(self.position[position[0]][position[1]].x(), self.position[position[0]][position[1]].y())
        self.index_current_card = -1

    # to play cards on the board (drag'n'drop) --> Jouer des cartes sur le plateau
    def dropEvent(self, e):
        position = e.pos()
        flag_spell = self.game.can_play_spell(self.index_current_card)
        if flag_spell[0]: # spell
            e.accept()
            self.refresh(flag_spell)
        else: # monster
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    if self.position[i][j].contains(position):
                        pos = (i, j)
                        flag_drag = self.game.can_play_monster(self.index_current_card, pos)

                        if flag_drag[0]:
                            self.move_card_from_hand_to_board(self.index_current_card, pos)
                            e.setDropAction(Qt.MoveAction)
                            e.accept()
                            self.refresh(flag_drag)
        print(self.game.board)
        self.update()

    ### GRAPHICS USE ###

    # color the areas where players put their cards
    def paintEvent(self, e):
        painter = QPainter(self)
        # display the board
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                painter.eraseRect(self.position[i][j])
                # black borders with a 3-width pen
                pen = QPen(Qt.black)
                pen.setWidth(3)
                painter.setPen(pen)
                painter.drawRect(self.position[i][j])
                # restore the initial Alpha mode for card that attack
                if(self.color[i][j].alpha() == 50):
                    self.color[i][j].setAlpha(200)
                painter.fillRect(self.position[i][j], self.color[i][j])
        
        # dessiner les joueurs
        for i in range(len(self.player_medal)):
            painter.fillRect(self.player_medal[i], self.color_players[i])
        painter.end()


    # attack of a monster --> Attaquer monstres ou joueurs
    def mouseReleaseEvent(self, e):
        position = e.pos()
        # draw a card from the deck
        if QRect(self.current_deck.x(), self.current_deck.y(), self.current_deck.width, self.current_deck.height).contains(e.pos()):
            flag_draw = self.game.can_draw_card()
            if flag_draw[0]:
                self.refresh(flag_draw)
        
        # attack mode
        if self.tour >= 1: # pas le premier tour pour qu'on puisse attaquer
            # Y-a-til un clic sur le Board ?
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    if self.position[i][j].contains(position):
                        if not self.ongo_attack: # pas encore d'attaque
                            self.i_card_attacking = i
                            self.j_card_attacking = j
                            self.color[i][j].setAlpha(50)
                            if self.game.card_can_attack((i, j)):
                                self.ongo_attack = True # ongoing attack

                                self.qapp.setOverrideCursor(Qt.CrossCursor)
                        else: # attaque en cours
                            flag_attack = self.game.can_attack_monster((self.i_card_attacking, self.j_card_attacking), (i, j))
                            if flag_attack[0]: # monstre peut être attaqué ?
                                self.refresh(flag_attack)
                                if not isinstance(self.grid[i][j].card, Placeholder):
                                    self.color[self.i_card_attacking][self.j_card_attacking] = QColor(105, 105, 105, 200)
                                    self.color[i][j] = QColor(105, 105, 105, 200)
                            self.color[self.i_card_attacking][self.j_card_attacking].setAlpha(200)
                            self.ongo_attack = False
                            self.qapp.restoreOverrideCursor()
            
            # attack a player
            if self.player_medal[(self.tour+1)%2].contains(position):
                if self.ongo_attack: # attaque en cours
                    flag_attack_player = self.game.can_attack_opponent_with_monster((self.i_card_attacking, self.j_card_attacking))
                    if flag_attack_player[0]: # joueur peut être attaqué ?
                        self.color[self.i_card_attacking][self.j_card_attacking] = QColor(105, 105, 105, 200)
                        self.refresh(flag_attack_player)
                        
            # draw a card
#            if QRect(se, , 50, 100).contains(position):
#                if not self.ongo_attack:
        
        self.update()