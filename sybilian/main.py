from cards import *
from deck import *
from board import *
from player import *
from game import *
from PyQt5.QtWidgets import QApplication
import sys
            
if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    app.exec_()