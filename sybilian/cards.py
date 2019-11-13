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
    def __init__(self, name : str, price : int, color : str, effect : dict):
        super().__init__(name, price, color, effect)

class Spell(Cards):
    def __init__(self, name : str, price : int, color : str, effect : dict):
        super().__init__(name, price, color, effect)

class Counterspell(Cards):
    def __init__(self, name : str, price : int, color : str, effect : dict):
        super().__init__(name, price, color, effect)


if __name__=="__main__":
    card_1 = Monster("Devorombre", 1, "Violet", "Transforme en ombre la créature attaquée")
    card_2 = Counterspell("Armistice", 0, "Gris", "Toutes les prochaines attaques sont contrés")
    card_3 = Spell("Boule de feu", 0, "Rouge", "L'adversaire perd un point de vie")
    deck = Deck([card_1, card_2, card_3])
