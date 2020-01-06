from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData, QRect
from PyQt5.QtGui import QPainter, QColor, QPixmap, QDrag, QPen, QCursor

class Card(QLabel):
    """
        A card has a name, a price
        a color and an effect that
        is stored as a dict
    """
    def __init__(self, name : str, parent, price : int, color : str, effect : dict, game_text : str, owner : str = None) -> None:
        super().__init__(name, parent)
        self.name = name
        self.price = price
        self.color = color
        self.effect = effect
        self.owner = owner
        self.game_text = game_text
        self.setAcceptDrops(True)
        self.explanation = QLabel('', parent)
        self.parent = None # stuck to which area
        self.win = parent # parent window
        self.image = "monster.png" # card representation
        self.width = 50
        self.height = 100

    def __str__(self) -> str:
        """
            Create a string from
            a card
        """
        printable_content = self.__class__.__name__ + " | "
        printable_content+= "Name : "+self.name+ " | "
        printable_content+= "Price : "+str(self.price) + " | "
        printable_content+= "Game Text : "+self.game_text
        return printable_content

    def mouseMoveEvent(self, e):
        if not self.placed:
            if e.buttons() != Qt.LeftButton:
                return
    
            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(e.pos() - self.rect().topLeft())
            #dropAction = drag.exec_(Qt.MoveAction)
    
    def enterEvent(self, e):  
        self.explanation.move(680, 400)
        self.explanation.setText(self.name + "\n" + self.game_text)
        self.explanation.show()
        
        # invalid cards : they have been already used
        if self.placed:
            self.win.setOverrideCursor(Qt.ForbiddenCursor)
        
    def leaveEvent(self, e):
        self.explanation.hide()
        
        if self.placed:
            self.win.restoreOverrideCursor()

class Placeholder(Card):
    """
        A object used for the
        interface. It's a
        placeholder for cards.
    """
    def __init__(self):
        self.name = "placeholder"
        self.price = 0
        self.effect = {}
        self.game_text = " . "
        self.image = ""
        

class Monster(Card):
    """
        A monster is a card that cost 1
        and has a kin
    """
    def __init__(self, name : str, parent : QWidget, price : int, color : str, kin : str, effect : dict, game_text : str, owner : str = None) -> None:
        super().__init__(name, parent, price, color, effect, game_text, owner)
        self.kin = kin
        self.life = 2
        self.coord = (0,0)

    def attack(self, card_2):
        """
            A card can attack an other card
        """
        assert(self.life > 0)
        if self.effect["Puissante"]==1:
            if card_2.effect["Puissante"]==1:
                card_2.life-=1
            else:
                card_2.life = 0
            self.life-=1
        else:
            if card_2.effect["Puissante"]==1:
                self.life = 0
            else:
                self.life-=1
            card_2.life-=1

class Spell(Card):
    """
        A spell is a card that cost 0
        and that has effects.
    """
    def __init__(self, name : str, parent : QWidget, price : int, color : str, effect : dict, game_text : str, owner : str = None) -> None:
        super().__init__(name, parent, 0, color, effect, game_text, owner)

class Counterspell(Card):
    """
        A Counterspell is a card that
        cost 0 but that can only be played
        when the other player plays a card
    """
    def __init__(self, name : str, parent : QWidget, price : int, color : str, effect : dict, game_text : str, owner : str = None) -> None:
        super().__init__(name, parent, 0, color, effect, game_text, owner)
