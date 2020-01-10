# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:08:41 2019

@author: clari
and @Nicolas
"""

from cards import *
from deck import *
from board import *
from player import *

class Game:
    def __init__(self) -> None:
        self.board = Board()
        # player_one has access to the first and second lines of the board
        # player_two has access to the third and fourth lines of the board
        self.players = (Player("deckC001.csv", self.board, [0, 1], 2), Player("deckB001.csv", self.board, [2, 3], 1))
        self.players[0].other_player = self.players[1]
        self.players[1].other_player = self.players[0]
        self.nb_turns = 0
        self.end = False
    
    def condition_endgame(self) -> bool:
        """
            return True if a player won,
            False otherwise
        """
        if self.players[0].life_points > 0 and self.players[1].life_points > 0:
            return False
        elif self.players[0].life_points == 0:
            print("Le joueur 2 a gagné!")
            return True
        elif self.players[1].life_points == 0:
            print("Le joueur 1 a gagné!")
            return True
    
    def turn(self):
        """
            /!\ pour l'instant un joueur peut juste jouer des monstres
        """
        nb_actions = 2
        while nb_actions > 0:
            print(self.board)
            action = str(input("Entrer 'p' pour piocher une carte, 'j' pour jouer une carte, 'c' pour regarder les cartes dans votre main: "))
            if action == 'p':
                self.players[self.nb_turns%2].draw()
                nb_actions -= 1
            elif action == 'c':
                print(self.players[self.nb_turns%2].hand)
            elif action == 'j':
                j = int(input("Quelle carte voulez-vous jouer (entrer un nombre entre 1 et "+ str(self.players[self.nb_turns%2].hand.size) +"): "))
                if isinstance(self.players[self.nb_turns%2].hand.read_card(j - 1), Monster):
                    x = int(input("Sur quelle ligne voulez-vous jouer votre carte (" + str(self.players[self.nb_turns%2].lines[0]) +" ou " + str(self.players[self.nb_turns%2].lines[1]) + "): "))
                    y = int(input("Sur quelle colonnes voulez-vous jouer votre carte (0 ou 1 ou 2): "))
                    # The card is actually played
                    if self.players[self.nb_turns%2].play(j, (x, y)):
                        nb_actions -= self.board.grid[x][y].price
                        print("Il vous reste " + str(nb_actions))
                elif isinstance(self.players[self.nb_turns%2].hand.read_card(j - 1), Spell):
                    #voir ensuite comment faire pour les sorts 
                    nb_actions -= self.players[self.nb_turns%2].hand.read_card(j).price
                    self.board.purgatory.add(self.players[self.nb_turns%2].hand.play(j)) 
                    
        # Player are allowed to attack after their first turn
        if self.nb_turns > 1:
            print("Point de vie: " + str(self.players[self.nb_turns%2].life_points))
            print("Point de vie: " + str(self.players[1 - self.nb_turns%2].life_points))
            attack = str(input("Entrer 'm' pour attaquer un monstre de l'adversaire, 'a' pour attaquer directement votre adversaire, 'c' pour regarder les cartes dans votre main, 't' pour terminer votre tour"))
            while attack != 't':
                if attack == 'm':
                    #vérifier que c'est bien le monstre du joueur???
                    x = int(input("Ligne de votre monstre qui attaque: "))
                    y = int(input("Colonne de votre monstre qui attaque: "))
                    x_other_player = int(input("Ligne du monstre que vous voulez attaquer: "))
                    y_other_player = int(input("Colonne du monstre que vous voulez attaquer: "))
                    if x in self.players[self.nb_turns%2].lines and y in [0, 1, 2]:
                        if self.players[self.nb_turns%2].verify_coord_attack((x_other_player, y_other_player)):
                            self.players[self.nb_turns%2].attack_monster(self.board.grid[x][y], self.board.grid[x_other_player][y_other_player])
                            attack = str(input("Entrer 'm' pour attaquer un monstre de l'adversaire, 'a' pour attaquer directement votre adversaire, 'c' pour regarder les cartes dans votre main, 't' pour terminer votre tour"))
                        else :
                            print("Vous n'attaquez pas un monstre de votre adversaire")
                    else:
                        print("Ce n'est pas un de vos monstre que vous voulez faire attaquer")
                elif attack == 'a':
                    x = int(input("Ligne de votre monstre qui attaque: "))
                    y = int(input("Colonne de votre monstre qui attaque: "))
                    if x in self.players[self.nb_turns%2] and y in [0, 1, 2]:
                        self.players[self.nb_turns%2].attack_player_with_monster(self.board.grid[x][y], self.players[(self.nb_turns + 1 )%2])
                    else:
                        print("Ce n'est pas un de vos monstre que vous voulez faire attaquer")
                elif action == 'c':
                    print(self.players[self.nb_turns%2].hand)
            attack = str(input("Entrer 'm' pour attaquer un monstre de l'adversaire, 'a' pour attaquer directement votre adversaire, 'c' pour regarder les cartes dans votre main, 't' pour terminer votre tour"))
            print(self.board)
    
    def game_loop(self):
        while not self.end:
            self.turn()
            self.nb_turns += 1
            self.end = self.condition_endgame()
            
