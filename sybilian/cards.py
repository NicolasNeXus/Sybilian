class Card():
    """
        A card has a name, a price
        a color and an effect that
        is stored as a dict
    """
    def __init__(self, name : str, price : int, color : str, effect : dict, game_text : str,owner : str = None) -> None:
        self.name = name
        self.price = price
        self.color = color
        self.effect = effect
        self.owner = owner
        self.game_text = game_text

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


class Monster(Card):
    """
        A monster is a card that cost 1
        and has a kin
    """
    def __init__(self, name : str, price : int, color : str, kin : str, effect : dict, game_text : str, owner : str = None) -> None:
        super().__init__(name, price, color, effect, game_text, owner)
        self.kin = kin
        self.life = 2
        self.coord = (0,0)


    def attack(self, card_2):
        """
            A card can attack an other card
        """
        assert(self.life > 0)
        if "Powerful" in self.effect.keys() and self.effect["Powerful"]=="No_condition":
            if "Powerful" in card_2.effect.keys() and card_2.effect["Powerful"]=="No_condition":
                card_2.life-=1
            else:
                card_2.life = 0
            self.life-=1
        else:
            if "Powerful" in card_2.effect.keys() and card_2.effect["Powerful"]=="No_condition":
                self.life = 0
            else:
                self.life-=1
            card_2.life-=1


class Spell(Card):
    """
        A spell is a card that cost 0
        and that has effects.
    """
    def __init__(self, name : str, price : int, color : str, effect : dict, game_text : str, owner : str = None) -> None:
        super().__init__(name, 0, color, effect, game_text, owner)

class Counterspell(Card):
    """
        A Counterspell is a card that
        cost 0 but that can only be played
        when the other player plays a card
    """
    def __init__(self, name : str, price : int, color : str, effect : dict, game_text : str, owner : str = None) -> None:
        super().__init__(name, 0, color, effect, game_text, owner)
