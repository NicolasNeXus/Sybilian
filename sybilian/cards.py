class Card():
    """
        A card has a name, a price
        a color and an effect that
        is stored as a dict
    """
    def __init__(self, name : str, price : int, color : str, effect : str, owner : str = None) -> None:
        self.name = name
        self.price = price
        self.color = color
        self.effect = effect
        self.owner = owner

    def __str__(self) -> str:
        """
            Create a string from
            a card
        """
        printable_content = self.__class__.__name__ + " | "
        printable_content+= "Name : "+self.name+ " | "
        printable_content+= "Price : "+str(self.price) + " | "
        printable_content+= "Effect : "+self.effect
        return printable_content

class Monster(Card):
    """
        A monster is a card that cost 1
        and has a kin
    """
    def __init__(self, name : str, price : int, color : str, kin : str, effect : dict, owner : str = None) -> None:
        super().__init__(name, price, color, effect, owner)
        self.kin = kin
        self.life = 2
        self.coord = (0,0)

    def attack(self, card_2):
        """
            A card can attack an other card
        """
        assert(self.life > 0)
        if effect["Puissante"]==1:
            if card_2.effect["Puissante"]==1:
                card_2.life-=1
            else:
                card_2.life = 0
            life-=1
        else:
            if card_2.effect["Puissante"]==1:
                life = 0
            else:
                life-=1
            card_2.life-=1

class Spell(Card):
    """
        A spell is a card that cost 0
        and that has effects.
    """
    def __init__(self, name : str, price : int, color : str, effect : dict, owner : str = None) -> None:
        super().__init__(name, 0, color, effect, owner)

class Counterspell(Card):
    """
        A Counterspell is a card that
        cost 0 but that can only be played
        when the other player plays a card
    """
    def __init__(self, name : str, price : int, color : str, effect : dict, owner : str = None) -> None:
        super().__init__(name, 0, color, effect, owner)


