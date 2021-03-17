from tkinter import *
import plateau as plateau
import time

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:48:54 2017

@author: Pierre Monrocq
"""

#classe dedié au debug du programme. Certaines fonction pourront être réutiliser dans un second temps

def calcul_offset(fenetre_hauteur):
    """
    Calcul l'offset
    
   :param fenetre_hauteur: hauteur de la fenetre
   :type fenetre_hauteur: entier
   :return: coordonnées x et y
   :rtype: tuple
   """
    x = fenetre_hauteur/2-(plateau.CASE_PLAT*8)
    y = plateau.CASE_PLAT-10
    return(x,y)

def rechercher_case(i,j,canvas,image_selecteur,*debug):
    """
    recherche une case dans le plateau isometrique

   """
    x,y = plateau.position_cases_iso(i,j)
    canvas.create_image(x,y,image=image_selecteur)
    if debug:
        print("coordonnées_recherche: "+str(x)+","+str(y))
    canvas.pack()
    
def afficher_objets(canvas):
    """
    Affiche un objet dans un canvas
    
   :param canvas: canvas tkinter
   :type canvas: objet tkinter
   """
    liste_objets = canvas.find_alltags()
    return liste_objets
    
def afficher_temps_execution_debut():
    """
    Fonction complementaire de afficher_temps_execution_fin
    
   :param fenetre_hauteur: hauteur de la fenetre
   :return:
   :rtype: flottant
   """
    start_time = time.time()
    return start_time


def afficher_temps_execution_fin(start_time,task):
    """
    Affiche le temps d'execution
    
   :param start_time: debut
   :type start_time: entier
   :return: affiche le temps d'execution dans la console
   """
    print("--- "+ task +" %f ---" % (time.time() - start_time))