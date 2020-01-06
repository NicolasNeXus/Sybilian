from cards import *
from deck import *
from board import *
from player import *
from game import *
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap, QDrag, QPen, QCursor

if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    game = Game()
    game.game_loop()
    game.show()
    app.exec_()
