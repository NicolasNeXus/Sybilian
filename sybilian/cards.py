class Cards():
    def __init__(self, name : str, price : int, color : str, effect : str):
        self.name = name
        self.price = price
        self.color = color
        self.effect = effect

    def __str__(self):
        printable_content = self.__class__.__name__ + " | "
        printable_content+= "Name : "+self.name+ " | "
        printable_content+= "Price : "+str(self.price) + " | "
        printable_content+= "Effect : "+self.effect
        return printable_content

class Monster(Cards):
    def __init__(self, name : str, price : int, color : str, kin : str, effect : dict):
        super().__init__(name, price, color, effect)
        self.kin = kin
        self.life = 2

    def attack(self, card_2):
        assert(self.life > 0)
        if effect["Puissante"]==1:
            if card_2.effect["Puissante"]==1:
                card_2.life--
            else
                card_2.life = 0
            life--
        else:
            if card_2.effect["Puissante"]==1:
                life = 0
            else
                life--
            card_2.life--

class Spell(Cards):
    def __init__(self, name : str, price : int, color : str, effect : dict):
        super().__init__(name, price, color, effect)

class Counterspell(Cards):
    def __init__(self, name : str, price : int, color : str, effect : dict):
        super().__init__(name, price, color, effect)


