from tkinter import *
from pathlib import Path

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:48:54 2017

@author: Pierre Monrocq
"""

def sauvegarder_partie(grille,tour,*log):
    """
    Sauvegarde une partie
    
   :param grille: grille du plateau
   :type grille: liste
   :param tour: tour de la partie
   :type tour: entier
   :rtype: void
   """
    fichier = open("save/partie.txt","w")
    fichier.write(str(grille)+"\n")
    fichier.write(str(tour))
    fichier.close()
    if True in log:
        print("Sauvegarde de la partie avec succès!")
    
def charger_grille_partie(*log):
    """
    Charge une partie
    
   :param log: affiche des informations dans la console
   :return: grille
   :rtype: liste
   """
    fichier = open("save/partie.txt","r")
    lignes = fichier.readlines()
    grille = lignes[0]
    fichier.close()
    if True in log:
        print("Chargement de la partie avec succès!")
    return grille

def charger_tour_partie(*log):
    """
    Charge le tour d'une partie
    
   :param log: affiche des informations dans la console
   :return: tour
   :rtype: entier
   """
    fichier = open("save/partie.txt","r")
    lignes = fichier.readlines()
    tour = lignes[1]
    fichier.close()
    if True in log:
        print("Chargement de la partie avec succès!")
    return tour
    
def fichier_existant(*log):
    """
    Verifie si un fichier existe
    
   :param log: affiche des informations dans la console
   :return: Vrai existe, faux n'existe pas
   :rtype: booléen
   """
    my_file = Path("save/partie.txt")
    if my_file.is_file():
        if True in log:
            print("Un fichier a été trouvé!")
        return True
    if True in log:
            print("Aucun fichier n'a été trouvé!")
    return False