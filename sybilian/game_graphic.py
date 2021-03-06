# graphics use
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap, QDrag, QPen, QCursor, QFont, QMouseEvent

from cards import Placeholder
from cards_graphic import GraphicCard
from game import Game


class GameGraphic(QWidget):
    """ Graphic interface of the game """

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
        self.deck_current = QLabel('', self)
        self.deck_current.setVisible(False)
        self.deck_other = QLabel('', self)
        self.deck_other.setVisible(False)
        self.len_current_deck = 27
        self.len_other_deck = 27
        self.current_deck = GraphicCard(Placeholder(), self)
        self.other_deck = GraphicCard(Placeholder(), self)
        self.i_card_attacking, self.j_card_attacking = None, None

        self.finish_turn = QPushButton('FINISH YOUR TURN', self) # button to finish your turn
        self.index_current_card = None
        self.qapp = app
        self.player_medal = [QRect(0, 0, 100, 50), QRect(0, 850, 100, 50)]
        self.color_players = [QColor(255, 0, 0, 200), QColor(0, 0, 255, 200)]
        self.position = [[QRect(150*j + 100, 100 + 150 * i, 50, 100) for j in range(3)] for i in range(2)] + [[QRect(150*j + 100, 400 + 150 * i, 50, 100) for j in range(3)] for i in range(2)]
        self.reference_color = [[QColor(255, 0, 0, 200) for j in range(3)] for i in range(2)] + [[QColor(0, 0, 255, 200) for j in range(3)] for i in range(2)]
        self.color = [[QColor(255, 0, 0, 200) for j in range(3)] for i in range(2)] + [[QColor(0, 0, 255, 200) for j in range(3)] for i in range(2)]
        self.grid = [[Placeholder() for j in range(3)] for i in range(2)] + [[Placeholder() for j in range(3)] for i in range(2)]
        self.players = ("Player1", "Player2")

        self.initUi() # Main window

    def initLife(self, number_card: int, player_name: str) -> None:
        """ Display the Life of a player

        :param number_card : number of cards in the Life
        :param player_name : name of the player
        """

        i = self.players.index(player_name)
        for j in range(number_card):
            card = GraphicCard(Placeholder(), self)
            card.setPixmap(QPixmap("hidden_card.png"))
            card.move(550, 300*i + 100 + 25*j)
            if player_name == self.players[self.tour%2]:
                self.current_life.append(card)
            else:
                self.other_life.append(card)
            card.show()

    def initBoard(self, board: list) -> None:
        """ Display the board

        :param board : list of Cards
        """
        for i in range(len(board)):
            for j in range(len(board[0])):
                self.grid[i][j] = GraphicCard(board[i][j], self)
                if not isinstance(self.grid[i][j].card, Placeholder):
                    if i < 2:
                        self.grid[i][j].setPixmap(QPixmap("monster.png"))
                    else:
                        self.grid[i][j].setPixmap(QPixmap("monster_2.png"))
                    if self.grid[i][j].card.life == 1:
                        self.color[i][j] = QColor(105, 105, 105, 200)
                else:
                    self.color[i][j] = self.reference_color[i][j]
                self.grid[i][j].move(self.position[i][j].x(), self.position[i][j].y())
                self.grid[i][j].show()

    def initHand(self, hand: list, player_name: str) -> None:
        """ Display the hand of a player

        :param hand : Hand's container ie. list of Cards
        :param player_name : name of the player
        """

        i = self.players.index(player_name)
        for j in range(len(hand)):
            card = GraphicCard(hand[j], self)
            if player_name == self.players[self.tour%2]:
                self.current_hand.append(card)
                if self.tour%2 == 0:
                    card.setPixmap(QPixmap("monster.png"))
                else:
                    card.setPixmap(QPixmap("monster_2.png"))
            else:
                self.other_hand.append(card)
                card.setPixmap(QPixmap("hidden_card.png"))
            card.move(130 + 70*j, 10 + 700*i)
            card.show()

    def initDeck(self, player_name: str) -> None:
        """ Display the deck of a player """
        i = self.players.index(player_name)
        if player_name == self.players[self.tour%2]:
            card = self.current_deck
        else:
            card = self.other_deck
        card.setPixmap(QPixmap("deck_card.png"))
        card.move(750, 150 + 325*i)
        card.show()

    def clearHand(self, hand: list) -> None:
        """ Erase (graphically) the hand of the current player

        :param hand: list of GraphicCards
        """

        for card in hand:
            card.hide()
            card.setParent(None)
        if self.current_hand == hand:
            self.current_hand = []
        elif self.other_hand == hand:
            self.other_hand = []

    def clearBoard(self) -> None:
        """ Erase the board """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j].hide()
                self.grid[i][j].setParent(None)
   
    def clearLife(self, player_name: str) -> None:
        """ Erase (graphically) the Life of a player """
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
                card.setParent(None)

    def clearDeck(self, player_name: str) -> None:
        """ Erase (graphically) the Deck of a player """
        if player_name == self.players[self.tour%2]:
            card = self.current_deck
        else:
            card = self.other_deck
        card.hide()

    def initUi(self) -> None:
        """ Main window """

        def change_turn() -> None:
            """ End the turn of the current player if it's OK """
            flag_change_turn = self.game.can_end_turn()
            print('flag_turn', flag_change_turn)
            if flag_change_turn[0]:
                self.tour += 1
                self.refresh(flag_change_turn)
                self.current_deck, self.other_deck = self.other_deck, self.current_deck

                # Remained cards in decks
                if self.tour % 2 == 0:
                    self.deck_current.setText(str(self.len_current_deck))
                    self.deck_other.setText(str(self.len_other_deck))
                else:
                    self.deck_current.setText(str(self.len_other_deck))
                    self.deck_other.setText(str(self.len_current_deck))
                self.ongo_attack = False             

                # Text to indicate the current tour
                self.text_tour.setText("Tour : " + str(self.tour))
                if self.tour%2 == 0:
                    self.text_tour.setStyleSheet("color: red;")
                else:
                    self.text_tour.setStyleSheet("color: blue;")

                # Game is ended ?
                self.end = self.game.condition_endgame()
                if self.end:
                    self.close()

        # Button to change turns
        self.finish_turn.move(700, 350)
        self.finish_turn.clicked.connect(change_turn)

        # Qlabel that displays the number of the current tour
        self.text_tour.setFont(QFont('SimHei', 20))
        self.text_tour.setStyleSheet("color: red;")
        self.text_tour.move(700, 80)

        self.initHand(self.game.get_current_hand(), self.players[0])
        self.initHand([Placeholder() for i in range(4)], self.players[1])

        self.initLife(9, self.players[0])
        self.initLife(9, self.players[1])

        self.initDeck(self.players[0])
        self.initDeck(self.players[1])     

        self.initBoard(self.grid)

        # Number of cards in the decks
        self.deck_current.move(760, 260)
        self.deck_other.move(760, 590)
        self.deck_current.setText(str(self.len_current_deck))
        self.deck_other.setText(str(self.len_other_deck))
        self.deck_current.setVisible(True)
        self.deck_other.setVisible(True)

        # Main window with its properties
        self.setWindowTitle('Sybilian')
        self.setGeometry(50, 50, 1000, 900)
        self.setMouseTracking(True) # mouse tracking on the screen
        self.setAcceptDrops(True)

    def refresh(self, list_area: list) -> None:
        """ Refresh the indicated areas """
        if list_area[1] is not None:
            self.clearHand(self.current_hand)
            self.initHand(list_area[1], self.players[self.tour%2])
        if list_area[2] is not None:
            self.len_current_deck = list_area[2]
        if list_area[3] is not None:
            self.clearLife(self.players[self.tour%2])
            self.initLife(list_area[3], self.players[self.tour%2])
        if list_area[5] is not None:
            self.clearHand(self.other_hand)
            self.initHand([Placeholder() for i in range(list_area[5])], self.players[(self.tour+1)%2])
        if list_area[6] is not None:
            self.len_other_deck = list_area[6]
        if list_area[7] is not None:
            self.clearLife(self.players[(self.tour+1)%2])
            self.initLife(list_area[7], self.players[(self.tour+1)%2])
        if list_area[9] is not None:
            self.clearBoard()
            self.initBoard(list_area[9].grid)

    def dragEnterEvent(self, e: QMouseEvent) -> None:
        """ Beginning of a drag and drop to play a card """
        e.accept()
        for i in range(len(self.current_hand)):
            card = self.current_hand[i] # chosen card
            print('Etat de la boucle :', i)
            if QRect(card.x(), card.y(), card.width, card.height).contains(e.pos()):
                self.index_current_card = i
                print(i)

    def move_card_from_hand_to_board(self, index_current_card: int, position: tuple) -> None:
        """ Move a card to a position """
        self.current_hand[self.index_current_card].move(self.position[position[0]][position[1]].x(), self.position[position[0]][position[1]].y())
        self.index_current_card = None

    def dropEvent(self, e: QMouseEvent) -> None:
        """ End of a drag and drop to play a card """
        position = e.pos()
        flag_spell = self.game.can_play_spell(self.index_current_card)
        if flag_spell[0]: # Spell
            e.accept()
            self.refresh(flag_spell)
        else: # Monster
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

    def paintEvent(self, e: QMouseEvent) -> None:
        """ Color the areas where players put their cards """
        painter = QPainter(self)
        # Display the board
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                painter.eraseRect(self.position[i][j])
                # Black borders with a 3-width pen
                pen = QPen(Qt.black)
                pen.setWidth(3)
                painter.setPen(pen)
                painter.drawRect(self.position[i][j])
                painter.fillRect(self.position[i][j], self.color[i][j])

        # Draw player's medal
        for i in range(len(self.player_medal)):
            painter.fillRect(self.player_medal[i], self.color_players[i])
        painter.end()


    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """ To attack a monster or a player or draw a card from deck """
        position = e.pos()
        # Draw a card from the deck
        if not self.ongo_attack and QRect(self.current_deck.x(), self.current_deck.y(), self.current_deck.width, self.current_deck.height).contains(e.pos()):
            flag_draw = self.game.can_draw_card()
            if flag_draw[0]:
                self.refresh(flag_draw)
                if self.tour%2 == 0:
                    self.deck_current.setText(str(self.len_current_deck))
                    self.deck_other.setText(str(self.len_other_deck))
                else:
                    self.deck_current.setText(str(self.len_other_deck))
                    self.deck_other.setText(str(self.len_current_deck))

        # Attack mode
        if self.tour >= 1: # After the first tour, we can attack
            # Click on the board ?
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    if self.position[i][j].contains(position):
                        if not self.ongo_attack: # No ongoing attack
                            self.i_card_attacking = i
                            self.j_card_attacking = j
                            self.color[i][j].setAlpha(50)
                            if self.game.can_card_attack((i, j)):
                                self.ongo_attack = True # ongoing attack
                                self.qapp.setOverrideCursor(Qt.CrossCursor)
                        else: # Ongoing attack
                            flag_attack = self.game.can_attack_monster((self.i_card_attacking, self.j_card_attacking), (i, j))
                            if flag_attack[0]: # Monster could be attacked ?
                                self.refresh(flag_attack)
                            self.color[self.i_card_attacking][self.j_card_attacking].setAlpha(200)
                            self.ongo_attack = False
                            self.qapp.restoreOverrideCursor()

            # Attack a player
            if self.player_medal[(self.tour+1)%2].contains(position):
                if self.ongo_attack: # Ongoing attack
                    flag_attack_player = self.game.can_attack_opponent_with_monster((self.i_card_attacking, self.j_card_attacking))
                    if flag_attack_player[0]: # Player could be attacked ?
                        self.color[self.i_card_attacking][self.j_card_attacking].setAlpha(200)
                        self.refresh(flag_attack_player)
                        self.ongo_attack = False
                        self.qapp.restoreOverrideCursor()

            # Game is ended ?
            self.end = self.game.condition_endgame()
            if self.end:
                self.close()

        self.update()
