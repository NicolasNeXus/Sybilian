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
        """
            self.index : index of the player who is playing
        """
        self.board = Board()
        # player_one has access to the first and second lines of the board
        # player_two has access to the third and fourth lines of the board
        self.players = (Player("deckC001.csv", self.board, [1, 0]), Player("deckB001.csv", self.board, [2, 3]))
        self.players[0].other_player = self.players[1]
        self.players[1].other_player = self.players[0]
        self.index = 0 
        self.nb_actions = 2
        self.end = False
    
    def condition_endgame(self) -> bool:
        """
            return True if a player won,
            False otherwise
        """
        if self.players[0].life_points > 0 and self.players[1].life_points > 0:
            return False
        elif self.players[0].life_points == 0:
            print("Le joueur " + str(self.players[0].owner) + " a gagné!")
            return True
        elif self.players[1].life_points == 0:
            print("Le joueur " + str(self.players[1].owner) + " a gagné!")
            return True
    
    def can_play_monster(self, name_player : str, index_card : int, coord : tuple) -> bool:
        """
            return True if the player playing can play the card 
            return False otherwise  
            name_player : name of the owner of the card that we want to play
            index_card : index of the card that we want to play
            coord : position where we want to put the card
        """
        player_playing = self.players[self.index]
        # The owner's card that wants to play is the player who is playing and
        # the card is a monster
        if name_player == player_playing.owner and isinstance(player_playing.hand.read_card(index_card), Monster):
            # The player still have actions left 
            if self.nb_actions > 0:
                # The coordinates are valid 
                if coord[0] in player_playing.lines and coord[1] in [0, 1, 2]:
                        # The spot is empty
                        if isinstance(self.board.get_monster(coord), Placeholder):
                            player_playing.play(index_card, coord)
                            self.nb_actions -=1
                            return True # Refresh the hand and the board
        return False
    
    def can_play_spell(self, name_player : str, index_card : int, coord) -> bool:
        """
            return True if the player playing can play the card 
            return False otherwise  
            name_player : name of the owner of the card that we want to play
            index_card : index of the card that we want to play
        """
        player_playing = self.players[self.index]
        # The owner's card that wants to play is the player who is playing and
        # the card is a spell
        if name_player == player_playing.owner and isinstance(player_playing.hand.read_card(index_card), Spell):
            player_playing.play(index_card)
            return True # Refresh the hand and the board
        return False
    
    def can_draw_card(self, name_player : str):
        """
            return True if the player playing can draw a card from his deck
            and the different decks that need to be updated
            name_player : name of owner of the deck
        """
        player_playing = self.players[self.index]
        # The owner's hand that wants to draw is the player who is playing
        if name_player == player_playing.owner:
            # The player still have actions left
            if self.nb_actions > 0:
                # The player's deck is not empty:
                if player_playing.deck.size > 0:
                    # Verify that the player have less than max_len cards in his hand
                    if player_playing.hand.size < player_playing.hand.max_len:
                        player_playing.hand.draw()
                        self.nb_actions -= 1
                        return (True, ["Deck", "Hand"])
                    # The card is added to the graveyard
                    else:
                        player_playing.grave.add(player_playing.deck.draw())
                        self.nb_actions -= 1
                        return (True, ["Deck", "Graveyard"])
        return False
    
    def can_draw_hp(self, name_player : str):
        """
            return True if the player playing can draw a card from his hp
            and the different decks that need to be updated
        """
        player_playing = self.players[self.index]
        # The owner's hp that wants to draw is the player who is playing
        if name_player == player_playing.owner:
            # The player still have actions left
            if self.nb_actions > 0:
                # The player's hp is not empty:
                if player_playing.life.size > 0:
                    player_playing.life_points -= 1
                    # Verify that the player have less than max_len cards in his hand
                    if player_playing.hand.size < player_playing.hand.max_len:
                        player_playing.hand.draw_hp()
                        self.nb_actions -= 1
                        return (True, ["Life", "Hand"])
                    # The card is added to the graveyard
                    else:
                        player_playing.grave.add(player_playing.life.draw())
                        self.nb_actions -= 1
                        return (True, ["Life", "Graveyard"])
        return False
    
    def can_attack_monster(self, name_player1 : str, coord1 : tuple, name_player2 : str, coord2 : tuple) -> bool:
        """
            Return True if the player can attack an opponent's monster with his
            own monster
            name_player1 : owner of the monster which is supposed to attack
            coord1 : coordinates of the monster which is supposed to attack
            name_player2 : owner of the monster which is supposed to be attacked
            coord2 : coordinates of the monster which is supposed to be attacked
        """
        player_playing = self.players[self.index]
        opponent = player_playing.other_player
        # The player who wants to attack is the player who is playing
        if name_player1 == player_playing.owner and coord1[0] in player_playing.lines and coord1[1] in [0, 1, 2]:
            # The player is attacking his oponent
            if name_player2 == opponent.owner and coord2[0] in opponent.lines and coord2[1] in [0, 1, 2]:
                # We have two monsters
                if isinstance(self.board.get_monster(coord1), Monster) and isinstance(self.board.get_monster(coord2), Monster):
                    player_playing.attack_monster(self.board.get_monster(coord1), self.board.get_monster(coord2))
                    return True # ici il faut tout mettre à jour!!!!!
        return False
    
    def can_attack_opponent_with_monster(self, name_player1 : str, coord1 : tuple, name_player2 : str):
        """
            Return True if the player can attack his opponent with his monster
            name_player1 : owner of the monster which is supposed to attack
            coord1 : coordinates of the monster which is supposed to attack
            name_player2 : name of the opponent
        """
        player_playing = self.players[self.index]
        opponent = player_playing.other_player
        # The player who wants to attack is the player who is playing
        if name_player1 == player_playing.owner and coord1[0] in player_playing.lines and coord1[1] in [0, 1, 2]:
            # The player is attacking his oponent
            if name_player2 == opponent.owner:
                # We have a monster
                if isinstance(self.board.get_monster(coord1), Monster):
                    # The first line of the opponent is empty
                    if player_playing.verify_first_line_opponent_empty():
                        player_playing.attack_player_with_monster(self.board.get_monster(coord1), opponent)
                        return True # ici il faut tout mettre à jour!!!!!
        return False

    def end_turn(self):
        """ 
            Updates the index of the player currently playing and the number
            of actions
        """
        self.index = (self.index + 1)%2
        self.nb_actions = 2
        
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
                elif isinstance(self.players[self.nb_turns%2].hand.read_card(j - 1), Spell):
                    #voir ensuite comment faire pour les sorts 
                    nb_actions -= self.players[self.nb_turns%2].hand.read_card(j).price
                    self.board.purgatory.add(self.players[self.nb_turns%2].hand.play(j)) 
            print("Il vous reste " + str(nb_actions))
        # Player are allowed to attack after their first turn
        if self.nb_turns > 1:
            print("Point de vie: " + str(self.players[self.nb_turns%2].life_points))
            print("Point de vie: " + str(self.players[1 - self.nb_turns%2].life_points))
            attack = str(input("Entrer 'm' pour attaquer un monstre de l'adversaire, 'a' pour attaquer directement votre adversaire, 'c' pour regarder les cartes dans votre main, 't' pour terminer votre tour: "))
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
                            attack = str(input("Entrer 'm' pour attaquer un monstre de l'adversaire, 'a' pour attaquer directement votre adversaire, 'c' pour regarder les cartes dans votre main, 't' pour terminer votre tour: "))
                        else :
                            print("Vous n'attaquez pas un monstre de votre adversaire")
                    else:
                        print("Ce n'est pas un de vos monstre que vous voulez faire attaquer")
                elif attack == 'a':
                    x = int(input("Ligne de votre monstre qui attaque: "))
                    y = int(input("Colonne de votre monstre qui attaque: "))
                    if x in self.players[self.nb_turns%2].lines and y in [0, 1, 2]:
                        self.players[self.nb_turns%2].attack_player_with_monster(self.board.grid[x][y], self.players[(self.nb_turns + 1 )%2])
                    else:
                        print("Ce n'est pas un de vos monstre que vous voulez faire attaquer")
                elif action == 'c':
                    print(self.players[self.nb_turns%2].hand)
            attack = str(input("Entrer 'm' pour attaquer un monstre de l'adversaire, 'a' pour attaquer directement votre adversaire, 'c' pour regarder les cartes dans votre main, 't' pour terminer votre tour: "))
            print(self.board)
    
    def game_loop(self):
        while not self.end:
            self.turn()
            self.nb_turns += 1
            self.end = self.condition_endgame()
            
