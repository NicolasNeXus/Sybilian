import sys
from PyQt5.QtWidgets import QApplication

from game_graphic import Game_Graphic


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    GAME_GRAPH = Game_Graphic(APP)
    GAME_GRAPH.show()
    APP.exec_()
