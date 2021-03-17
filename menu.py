from tkinter import *
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:48:54 2017

@author: Pierre Monrocq
"""

#menu et options

def supprimer_boutons_menu(*but):
    for button in but:
        button.destroy()
        
def supprimer_fond_menu(can,*image):
    for img in image:
        can.delete(img)
        
def supprimer_boutons_menu_liste(liste):
    for button in liste:
        button.destroy()
        
def supprimer_fond_menu_liste(can,liste):
    for img in liste:
        can.delete(img)
    