from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap, QDrag, QPen
import sys

class Card(QRect):
  
    def __init__(self, parent):
        super().__init__(parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


#    def mousePressEvent(self, e):
#      
#        super().mousePressEvent(e)
#        
#        if e.button() == Qt.LeftButton:
#            print('press')

class Carte:
    def __init__(self, life, pos, col):
        self.life = life
        self.position = pos
        self.color = col

class Example(QWidget):
  
    def __init__(self):
        super().__init__()
        self.play1 = []
        self.play2 = []
        for i in range(2):
            for j in range(3):
                card = Carte(2, QRect(150*j + 10, 10 + 150 * i, 50, 100), QColor(255, 0, 0, 200)) 
                self.play1.append(card)
                card = Carte(2, QRect(150*j + 10, 400 + 150 * i, 50, 100), QColor(0, 0, 255, 200))
                self.play2.append(card)
        self.finish_turn = QPushButton('FINISH YOUR TURN', self)
        self.turn = 0 # game tour
        self.attempt = 2 # number of maximum acts to realize 
        self.attack = False
        self.initUI()
        
    
    def initUI(self):

        self.setAcceptDrops(True)

        self.carte = Card(600, 65, 50, 100)
        
        #self.carte.move(600, 65)
        
        # event for changing turns 
        def change_turn():
            self.turn += 1
            self.attempt = 2

        self.finish_turn.move(700, 300)
        self.finish_turn.clicked.connect(change_turn)

        self.setWindowTitle('Click or Move')
        self.setGeometry(50, 50, 900, 900)
        
    
    def paintEvent(self, e):
        painter = QPainter(self)
        for i in range(len(self.play1)):
            painter.eraseRect(self.play1[i].position)
            pen = QPen(Qt.black)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawRect(self.play1[i].position)
            painter.fillRect(self.play1[i].position, self.play1[i].color)
            painter.eraseRect(self.play2[i].position)
            painter.fillRect(self.play2[i].position, self.play2[i].color)
            painter.drawRect(self.play2[i].position)
        painter.end()
        
        
    def mouseReleaseEvent(self, e):
        for i in range(len(self.play1)):
            # Joueur 1
            if self.turn % 2 == 0 and self.play1[i].position.contains(e.pos()) and self.attack == False:
                self.play1[i].color.setAlpha(50)
                app.setOverrideCursor(Qt.CrossCursor)
                self.attack = True
            elif self.attack == True and self.turn % 2 == 0:
                for i in range(len(self.play1)):
                    if self.play2[i].position.contains(e.pos()):
                        self.play2[i].color = QColor(105, 105, 105, 200)
                        self.play2[i].life -= 1
                        self.attack = False
                        app.restoreOverrideCursor()
            
            # Joueur 2
            if self.turn % 2 == 1 and self.play2[i].position.contains(e.pos()) and self.attack == False:
                self.play2[i].color.setAlpha(50)
                app.setOverrideCursor(Qt.CrossCursor)
                self.attack = True
            elif self.attack == True and self.turn % 2 == 1:
                for i in range(len(self.play1)):
                    if self.play1[i].position.contains(e.pos()):
                        self.play1[i].color = QColor(105, 105, 105, 200)
                        self.play1[i].life -= 1
                        self.attack = False
                        app.restoreOverrideCursor()
        self.update()


    def dragEnterEvent(self, e):
        e.accept()
        

    def dropEvent(self, e):
        position = e.pos()
        for i in range(len(self.play1)):
            if self.turn % 2 == 0 and self.attempt > 0:
                if self.play1[i].position.contains(position):
                    self.carte.move(self.play1[i].position.x(), self.play1[i].position.y())
                    e.setDropAction(Qt.MoveAction)
                    e.accept()
                    self.attempt -= 1
            elif self.turn % 2 == 1 and self.attempt > 0:
                if self.play2[i].position.contains(position):
                    self.carte.move(self.play2[i].position.x(), self.play2[i].position.y())
                    e.setDropAction(Qt.MoveAction)
                    e.accept()
                    self.attempt -= 1


if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_() 