from game_graphic import *
from PyQt5.QtWidgets import QApplication
import sys

           
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_graph = Game_Graphic(app)
    game_graph.show()
    app.exec_()

