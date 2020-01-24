from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap, QDrag, QPen, QCursor

from cards import *

class Card_Graphic(QLabel):
    """
        A card has a name, a price
        a color and an effect that
        is stored as a dict
    """
    def __init__(self, card: Card, parent: QApplication) -> None:
        super().__init__('', parent)
        self.card = card
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.explanation = QLabel('', parent)
        self.explanation.setVisible(False)
        self.image = "monster.png" # card representation
        self.width = 50
        self.height = 100
        
    def __str__(self):
        return self.card.__str__()

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
    
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)
    
    def enterEvent(self, e):
        self.explanation.move(680, 400)
        self.explanation.setText(self.card.name + "\n\n" + self.card.game_text)
        self.explanation.setVisible(True)
        
    def leaveEvent(self, e):
        self.explanation.hide()