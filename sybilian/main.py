import sys
from PyQt5.QtWidgets import QApplication

from game_graphic import GameGraphic


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    GAME_GRAPH = GameGraphic(APP)
    GAME_GRAPH.show()
    APP.exec_()
