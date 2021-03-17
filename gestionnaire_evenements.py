from tkinter import *
from tkinter import messagebox
import plateau as plateau
import pions as pions
import sauvegarde as sauvegarde
import gestionnaire_images as g_images
import copy

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:48:54 2017

@author: Pierre Monrocq
"""


vue = 1
Liste_deplacements = []
Liste_deplacements_impossible = []
Liste_deplacements_final = []

def changement_vue(canvas,*debug):
    """
    Permet le changement de vue du plateau, interverti des éléments de places
    
   :param canvas: canvas Tkinter
   :type canvas: objet Tkinter
   :param *debug: affiche des informations de debug dans la console
   :type *debug: booléen
   :rtype: void
   """
    global vue
    vue *= -1
    if vue == 1:
        canvas.move("iso",0,580)#offscreen
        canvas.move("plat",0,-580)#onscreen
        canvas.move("img",0,-580)
        canvas.move("img_iso",0,580)
    else:
        canvas.move("iso",0,-580)#onscreen
        canvas.move("img",0,580)
        canvas.move("img_iso",0,-580)
        canvas.move("plat",0,580)#offscreen
    if True in debug:
            print("iso: "+str(canvas.find_withtag("iso")))
            print("plat: "+str(canvas.find_withtag("plat")))

def tour_joueur(nbtour):
    """
    Détermine le tour du joueur
    
   :param nbtour: Nombre total de tour
   :type nbtour: entier
   :return: n si c'est le tour des pions noirs, b si c'est le tour des pions blancs
   :rtype: caractères
   """
    if nbtour%2 != 0:
        return "n"
    else:
        return "b"
        
def afficher_tour(canvas,tour,im1,im2):
    """
    Affiche le tour sous forme d'image
    
   :param canvas: canvas Tkinter
   :type canvas: objet Tkinter
   :param tour: Nombre total de tour
   :type tour: entier
   :param im1: image
   :type im1: image convertie
   :param im2: image
   :type im2: image convertie
   :param *debug: affiche des informations de debug dans la console
   :type *debug: booléen
   """
    plateau.supprimer_indicateur(canvas,"tour_j")
    lettre = tour_joueur(tour)
    if lettre == "n":
        tour_j = canvas.create_image(int(1000)/2,25,image=im1)
        plateau.ajouter_id_element(canvas,"tour_j",tour_j)
    elif lettre == "b":
        tour_j = canvas.create_image(int(1000)/2,25,image=im2)
        plateau.ajouter_id_element(canvas,"tour_j",tour_j)
        
    
def case_vide(grille,x,y,*debug):
    """
    Détermine si une case est vide ou non
    
   :param grille: grille du plateau
   :type grille: liste
   :param x: position x de la case à déterminer
   :type x: entier
   :param y: position y de la case à déterminer
   :type y: entier
   :param *debug: affiche des informations de debug dans la console
   :type *debug: booléen
   :rtype: void
   """
    if grille[x][y] == "-":
        if True in debug:
            print("Case vide")
        return True
    if debug:
        print("Case non vide")
    return False

def case_avec_pion(grille,x,y,pion):
    """
    Verifie si le pion est bien à la case x y
    
   :param grille: grille du plateau
   :type grille: liste
   :param x: position x de la case à déterminer
   :type x: entier
   :param y: position y de la case à déterminer
   :type y: entier
   :param pion: pion du plateau
   :type pion: caractère
   :param *debug: affiche des informations de debug dans la console
   :type *debug: booléen
   :return: True ou False
   :rtype: booléen
   """
    if grille[x][y] == pion:
        return True
    return False
    

def calculs_deplacements(canvas,grille,pion,x,y,*debug):
    """
    Calcule les déplacements possible d'un pion dans le plateau (grille)
    
   :param grille: grille du plateau
   :type grille: liste
   :param x: position x de la case à déterminer
   :type x: entier
   :param y: position y de la case à déterminer
   :type y: entier
   :param pion: pion du plateau
   :type pion: caractère
   :param *debug: affiche des informations de debug dans la console
   :type *debug: booléen
   :rtype: liste
   """
    global Liste_deplacements
    Liste_deplacements = []
    global Liste_deplacements_impossible
    Liste_deplacements_impossible = []
    
    if pion == "f":#fantassin noir
        if(case_vide(grille,x,y+1) == True and plateau.dans_plateau(x,y+1) == True):
            Liste_deplacements.append((x,y+1))
    if pion == "F":
        if(case_vide(grille,x,y-1) == True and plateau.dans_plateau(x,y-1) == True):
            Liste_deplacements.append((x,y-1))
    if pion == "C" or pion =="c":#cavalier blanc ou noir
        if plateau.couleur_case(x,y) == True:#si case blanche
            for i in range(3):
                for j in range(3):
                    if plateau.dans_plateau(x+i-1,y+1-j) == True:
                        if(case_vide(grille,x+i-1,y+1-j)) == True:
                            Liste_deplacements.append((x+i-1,y+1-j))
                        if (pion == "C" and (grille[x+i-1][y+1-j] == "c" or grille[x+i-1][y+1-j] == "f") or pion =="c" and (grille[x+i-1][y+1-j] == "C" or grille[x+i-1][y+1-j] == "F")):
                            x0,y0 = x+i-1,y+1-j
                            if y == y0:
                                if x>x0:
                                   if plateau.dans_plateau(x0-1,y0) == True and case_vide(grille,x0-1,y0) == True:
                                     Liste_deplacements.append((x0-1,y0))  
                                else:
                                   if plateau.dans_plateau(x0+1,y0) == True and case_vide(grille,x0+1,y0) == True:
                                     Liste_deplacements.append((x0+1,y0))
                            if x == x0:
                                if y>y0:
                                   if plateau.dans_plateau(x0,y0-1) == True and case_vide(grille,x0,y0-1) == True:
                                     Liste_deplacements.append((x0,y0-1))  
                                else:
                                   if plateau.dans_plateau(x0,y0+1) == True and case_vide(grille,x0,y0+1) == True:
                                     Liste_deplacements.append((x0,y0+1))
                            if x > x0 and y0 != y:
                                if y>y0:
                                    if plateau.dans_plateau(x0-1,y0-1) == True and case_vide(grille,x0-1,y0-1) == True:
                                     Liste_deplacements.append((x0-1,y0-1))
                                else:
                                    if plateau.dans_plateau(x0-1,y0+1) == True and case_vide(grille,x0-1,y0+1) == True:
                                     Liste_deplacements.append((x0-1,y0+1))
                            if x < x0 and y0!=y:
                                if y0>y:
                                    if plateau.dans_plateau(x0+1,y0+1) == True and case_vide(grille,x0+1,y0+1) == True:
                                     Liste_deplacements.append((x0+1,y0+1))
                                else:
                                    if plateau.dans_plateau(x0+1,y0-1) == True and case_vide(grille,x0+1,y0-1) == True:
                                     Liste_deplacements.append((x0+1,y0-1))
                                     
        else:
            if (y == 2 or y == 5 ) and plateau.dans_plateau(x-1,y) == True:
                if case_vide(grille,x-1,y) == True:
                    Liste_deplacements.append((x-1,y))
                elif (pion == "C" and (grille[x-1][y] == "c" or grille[x-1][y] == "f") or pion =="c" and (grille[x-1][y] == "C" or grille[x-1][y] == "F")):
                    if plateau.dans_plateau(x-2,y) == True and case_vide(grille,x-2,y) == True:
                        Liste_deplacements.append((x-2,y))
                        
            if (y == 2  or y == 5 ) and plateau.dans_plateau(x+1,y) == True:
                if case_vide(grille,x+1,y) == True:
                   Liste_deplacements.append((x+1,y))
                elif (pion == "C" and (grille[x+1][y] == "c" or grille[x+1][y] == "f") or pion =="c" and (grille[x+1][y] == "C" or grille[x+1][y] == "F")):
                    if plateau.dans_plateau(x+2,y) == True and case_vide(grille,x+2,y) == True:
                        Liste_deplacements.append((x+2,y))
                
            if (y > -1 and y < 2 or y == 5 and x <3 or y==2 and x>4 or y == 4 and x>3 or y ==3 and x<4) and plateau.dans_plateau(x+1,y+1) == True:
               if case_vide(grille,x+1,y+1) == True:#/
                    Liste_deplacements.append((x+1,y+1))
               elif (pion == "C" and (grille[x+1][y+1] == "c" or grille[x+1][y+1] == "f") or pion =="c" and (grille[x+1][y+1] == "C" or grille[x+1][y+1] == "F")):
                   if plateau.dans_plateau(x+2,y+2) == True and case_vide(grille,x+2,y+2) == True:
                       Liste_deplacements.append((x+2,y+2))
                
            if (y<8 and y > 5 or y>-1 and y<2 or y == 5 and x <3 or y==2 and x>4 or y == 4 and x>3 or y ==3 and x<4) and plateau.dans_plateau(x-1,y-1) == True:
               if case_vide(grille,x-1,y-1) == True:
                   Liste_deplacements.append((x-1,y-1))
               elif (pion == "C" and (grille[x-1][y-1] == "c" or grille[x-1][y-1] == "f") or pion =="c" and (grille[x-1][y-1] == "C" or grille[x-1][y-1] == "F")):
                   if plateau.dans_plateau(x-2,y-2) == True and case_vide(grille,x-2,y-2) == True:
                       Liste_deplacements.append((x-2,y-2)) 
                
            if (y > -1 and y < 2 or y < 8 and y > 5 or y == 5 and x >3 or y==2 and x<4 or y == 4 and x<4 or y==3 and x>3) and plateau.dans_plateau(x+1,y-1) == True: 
                if case_vide(grille,x+1,y-1) == True:#\
                   Liste_deplacements.append((x+1,y-1))
                elif (pion == "C" and (grille[x+1][y-1] == "c" or grille[x+1][y-1] == "f") or pion =="c" and (grille[x+1][y-1] == "C" or grille[x+1][y-1] == "F")):
                   if plateau.dans_plateau(x+2,y-2) == True and case_vide(grille,x+2,y-2) == True:
                       Liste_deplacements.append((x+2,y-2))
                
            if (y < 8 and y > 5 or y > -1 and y < 2 or y == 5 and x >3 or y==2 and x<4 or y == 4 and x<4 or y==3 and x>3) and plateau.dans_plateau(x-1,y+1) == True:
                if case_vide(grille,x-1,y+1) == True:
                    Liste_deplacements.append((x-1,y+1))
                elif (pion == "C" and (grille[x-1][y+1] == "c" or grille[x-1][y+1] == "f") or pion =="c" and (grille[x-1][y+1] == "C" or grille[x-1][y+1] == "F")):
                    if plateau.dans_plateau(x-2,y+2) == True and case_vide(grille,x-2,y+2) == True:
                       Liste_deplacements.append((x-2,y+2))
            
            if (y == 4 or y==3) and plateau.dans_plateau(x,y+1) == True: 
                if case_vide(grille,x,y+1) == True:#|haut
                    Liste_deplacements.append((x,y+1))
                elif (pion == "C" and (grille[x][y+1] == "c" or grille[x][y+1] == "f") or pion =="c" and (grille[x][y+1] == "C" or grille[x][y+1] == "F")):
                    if plateau.dans_plateau(x,y+2) == True and case_vide(grille,x,y+2) == True:
                       Liste_deplacements.append((x,y+2))
                
            if (y == 4 or y ==3) and plateau.dans_plateau(x,y-1) == True:
               if case_vide(grille,x,y-1) == True:#|bas
                    Liste_deplacements.append((x,y-1))
               elif (pion == "C" and (grille[x][y-1] == "c" or grille[x][y-1] == "f") or pion =="c" and (grille[x][y-1] == "C" or grille[x][y-1] == "F")):
                    if plateau.dans_plateau(x,y-2) == True and case_vide(grille,x,y-2) == True:
                       Liste_deplacements.append((x,y-2))
    
    deplacements_impossibles(grille,pion)
    if True in debug:
        print(Liste_deplacements)      

def afficher_deplacements(canvas):
    """
    Affiche les déplacements sous forme d'image sur le plateau de jeu

   :param canvas: Canvas Tkinter
   :type canvas: Objet Tkinter
   :rtype: void
   """
    plateau.supprimer_indicateur(canvas,"dep")
    plateau.supprimer_indicateur(canvas,"dep_imp")
    for i in range(len(Liste_deplacements_final)):
        v,w = Liste_deplacements_final[i]
        pions.afficher_indicateur(canvas,v,w,"dep",g_images.deplacement)
    for i in range(len(Liste_deplacements_impossible)):
        v,w = Liste_deplacements_impossible[i]
        pions.afficher_indicateur(canvas,v,w,"dep_imp",g_images.deplacement_impossible)
        
def deplacements_impossibles(grille,pion,*debug):
    """
    Verifie si un pions peut aller à une case précise sans être sous une capture
    
   :param grille: grille du plateau
   :type grille: liste
   :param pion: pion du plateau
   :type pion: caractère
   :param *debug: affiche des informations de debug dans la console
   :type *debug: booléen
   :rtype: liste
   """
    global Liste_deplacements_final
    Liste_deplacements_final = copy.copy(Liste_deplacements)#On copie l'ancienne liste de deplacement par un nouvelle liste
    for i in range(len(Liste_deplacements)):
        v,w = Liste_deplacements[i]
        if pion == "C" or pion == "F":
            if v-1 > -1 and v+1<8:#Direction horizontale
                if(grille[v-1][w] == "c" or grille[v-1][w] == "f") and (grille[v+1][w] == "c" or grille[v+1][w] == "f"):
                    Liste_deplacements_final.remove((v,w))
                    Liste_deplacements_impossible.append((v,w))
            if w-1 > -1 and w+1<8:#Direction Verticale
                if(grille[v][w-1] == "c" or grille[v][w-1] == "f") and (grille[v][w+1] == "c" or grille[v][w+1] == "f"):
                    Liste_deplacements_final.remove((v,w))
                    Liste_deplacements_impossible.append((v,w))
            if v-1 > -1 and v+1<8 and w-1>-1 and w+1<8:#Direction diagonale coin superieur gauche
                if(grille[v-1][w-1] == "c" or grille[v-1][w-1] == "f") and (grille[v+1][w+1] == "c" or grille[v+1][w+1] == "f"):
                    Liste_deplacements_final.remove((v,w))
                    Liste_deplacements_impossible.append((v,w))
            if v-1 > -1 and v+1<8 and w-1>-1 and w+1<8:#Direction diagonale coin superieur droit
                if(grille[v+1][w-1] == "c" or grille[v+1][w-1] == "f") and (grille[v-1][w+1] == "c" or grille[v-1][w+1] == "f"):
                    Liste_deplacements_final.remove((v,w))
                    Liste_deplacements_impossible.append((v,w))
        if pion == "c" or pion == "f":
            if v-1 > -1 and v+1<8:
                if(grille[v-1][w] == "C" or grille[v-1][w] == "F") and (grille[v+1][w] == "C" or grille[v+1][w] == "F"):
                    Liste_deplacements_final.remove((v,w))
                    Liste_deplacements_impossible.append((v,w))
            if w-1 > -1 and w+1<8: 
                if(grille[v][w-1] == "C" or grille[v][w-1] == "F") and (grille[v][w+1] == "C" or grille[v][w+1] == "F"):
                    Liste_deplacements_final.remove((v,w))
                    Liste_deplacements_impossible.append((v,w))
            if v-1 > -1 and v+1<8 and w-1>-1 and w+1<8:
                if(grille[v-1][w-1] == "C" or grille[v-1][w-1] == "F") and (grille[v+1][w+1] == "C" or grille[v+1][w+1] == "F"):
                    Liste_deplacements_final.remove((v,w))
                    Liste_deplacements_impossible.append((v,w))
            if v-1 > -1 and v+1<8 and w-1>-1 and w+1<8:
                if(grille[v+1][w-1] == "C" or grille[v+1][w-1] == "F") and (grille[v-1][w+1] == "C" or grille[v-1][w+1] == "F"):
                    Liste_deplacements_final.remove((v,w))
                    Liste_deplacements_impossible.append((v,w))
    if True in debug:
        print(v,w)

def confirmer_deplacement(x,y):
    """
    Verifie si le deplacement aux coordonnées x y est possible

   :param x: position x de la case à déterminer
   :type x: entier
   :param y: position y de la case à déterminer
   :type y: entier
   :return: True ou False
   :rtype: booléen
   """
    global Liste_deplacements
    for i in range(len(Liste_deplacements)):
        if Liste_deplacements[i] == (x,y):
            return True
    return False

def confirmer_quitter(fenetre,grille,tour):
     """
     Demande à l'utilisateur si il veut quitter la partie, sauvegarde la partie et ferme la fenêtre
    
   :param fenetre: fenêtre Tkinter
   :type fenetre: objet Tkinter
   :param grille: plateau de jeu
   :type grille: liste
   :param tour: Nombre total de tour
   :type tour: entier
   :rtype: void
   """
     if messagebox.askokcancel("Voulez-vous quitter?"," La partie sera sauvegardée."):
         sauvegarde.sauvegarder_partie(grille,tour)
         fenetre.destroy()
                
    
def partie_gagner(fenetre,can,gagnant,nom1,nom2):
    """
    Détermine si une partie est terminée
    
   :param fenetre: fenêtre Tkinter
   :type fenetre: objet Tkinter
   :param can: Canvas Tkinter
   :type can: Objet Tkinter
   :param gagnant: nombre
   :type gagnant: entier
   :param nom1: nom du joueur 1
   :type nom1: chaine de caractères
   :param nom2: nom du joueur 2
   :type nom2: chaine de caractères
   :rtype: void
   """
    if gagnant == 1:
        messagebox.showinfo("Partie terminée!","Le joueur avec les pions " +nom1+ " à gagné la partie!")
        can.delete("all")
        can.pack()
        import relance as relance
        relance.recommencer_jeu(fenetre,can)
    elif gagnant == 2:
        messagebox.showinfo("Partie terminée!","Le joueur avec les pions " +nom2+ ";à gagné la partie!")
        can.delete("all")
        can.pack()
        import relance as relance
        relance.recommencer_jeu(fenetre,can)
    else:
        print("Erreur lors de l'attribution du gagnant")
        

def partie_termine(fenetre,can):
    """
    Demande a l'utilisateur si il veut recommencer une nouvelle partie, puis lance la partie si oui
    
   :param fenetre: fenêtre Tkinter
   :type fenetre: objet Tkinter
   :param can: Canvas Tkinter
   :type can: Objet Tkinter
   :rtype: void
   """
    if messagebox.askokcancel("Recommencer une partie?"," Voulez-vous recommencer la partie et finir la partie sur une égalité?"):
        can.delete("all")
        can.pack()
        import relance as relance
        relance.recommencer_jeu(fenetre,can)
    
def capture(grille,i,j):
    """
    Verifie si un des pions font une capture, modifie la grille en conséquence
    
   :param grille: Plateau de jeu
   :type grille: liste
   :param i: x de la case i
   :type i: entier
   :param j: y de la case j
   :type j: entier
   :rtype: void
   """
    z = 0
    for z in range(-1,2):
        if z == 0:
            continue
        if plateau.dans_plateau(i+2*z,j) == True and (grille[i][j] == "c" or grille[i][j] == "f") and (grille[i+1*z][j] == "C" or grille[i+1*z][j] =="F") and (grille[i+2*z][j] == "c" or grille[i+2*z][j] == "f"):
            grille[i+1*z][j] = "-"
        if plateau.dans_plateau(i+2*z,j) == True and (grille[i][j] == "C" or grille[i][j] == "F") and (grille[i+1*z][j] == "c" or grille[i+1*z][j] =="f") and (grille[i+2*z][j] == "C" or grille[i+2*z][j] == "F"):
            grille[i+1*z][j] = "-"
        if plateau.dans_plateau(i,j+2*z) == True and (grille[i][j] == "c" or grille[i][j] == "f") and (grille[i][j+1*z] == "C" or grille[i][j+1*z] =="F") and (grille[i][j+2*z] == "c" or grille[i][j+2*z] == "f"):
            grille[i][j+1*z] = "-"
        if plateau.dans_plateau(i,j+2*z) == True and (grille[i][j] == "C" or grille[i][j] == "F") and (grille[i][j+1*z] == "c" or grille[i][j+1*z] =="f") and (grille[i][j+2*z] == "C" or grille[i][j+2*z] == "F"):
            grille[i][j+1*z] = "-"
        if plateau.dans_plateau(i+2*z,j+2*z) == True and (grille[i][j] == "c" or grille[i][j] == "f") and (grille[i+1*z][j+1*z] == "C" or grille[i+1*z][j+1*z] =="F") and (grille[i+2*z][j+2*z] == "c" or grille[i+2*z][j+2*z] == "f"):
            grille[i+1*z][j+1*z] = "-"
        if plateau.dans_plateau(i+2*z,j+2*z) == True and (grille[i][j] == "C" or grille[i][j] == "F") and (grille[i+1*z][j+1*z] == "c" or grille[i+1*z][j+1*z] =="f") and (grille[i+2*z][j+2*z] == "C" or grille[i+2*z][j+2*z] == "F"):
            grille[i+1*z][j+1*z] = "-"
        if plateau.dans_plateau(i-2*z,j+2*z) == True and (grille[i][j] == "c" or grille[i][j] == "f") and (grille[i-1*z][j+1*z] == "C" or grille[i-1*z][j+1*z] =="F") and (grille[i-2*z][j+2*z] == "c" or grille[i-2*z][j+2*z] == "f"):
            grille[i-1*z][j+1*z] = "-"
        if plateau.dans_plateau(i-2*z,j+2*z) == True and (grille[i][j] == "C" or grille[i][j] == "F") and (grille[i-1*z][j+1*z] == "c" or grille[i-1*z][j+1*z] =="f") and (grille[i-2*z][j+2*z] == "C" or grille[j-2*z][j+2*z] == "F"):
            grille[i-1*z][j+1*z] = "-"
    for w in range(2):
        if (grille[0+w*7][0] == "F" or grille[0+w*7][0] == "C") and (grille[abs(1-w*7)][0] == "f" or grille[abs(1-w*7)][0] == "c") and (grille[0+w*7][0+w] == "f" or grille[0+w*7][0+w] == "c"):
            grille[0+w*7][0] = "-"
        if (grille[0+w*7][0] == "f" or grille[0+w*7][0] == "c") and (grille[abs(1-w*7)][0] == "F" or grille[abs(1-w*7)][0] == "C") and (grille[0+w*7][0+w] == "F" or grille[0+w*7][0+w] == "C"):
            grille[0+w*7][0] = "-"
        if (grille[0+w*7][7] == "F" or grille[0+w*7][7] == "C") and (grille[abs(1-w*7)][7] == "f" or grille[abs(1-w*7)][7] == "c") and (grille[0+w*7][6] == "f" or grille[0+w*7][6] == "c"):
            grille[0+w*7][7] = "-"
        if (grille[0+w*7][7] == "f" or grille[0+w*7][7] == "c") and (grille[abs(1-w*7)][7] == "F" or grille[abs(1-w*7)][7] == "C") and (grille[0+w*7][6] == "F" or grille[0+w*7][6] == "C"):
            grille[0+w*7][7] = "-"
                    
                  
def gagner_partie(grille,pion1,pion1_2,pion2,pion2_2,*debug):
    """
    Vérifie les conditions nécessaires pour qu'un joueur gagne une partie
    
   :param grille: plateau du jeu
   :type grille: liste
   :param pion1: pion du plateau
   :type pion1: caractère
   :param pion1_2: pion du plateau
   :type pion1_2: caractère
   :param pion2: pion du plateau
   :type pion2: caractère
   :param pion2_2: pion du plateau
   :type pion2_2: caractère
   :param *debug: affiche des informations de debug dans la console (optionel)
   :type *debug: booléen
   :return: Si 1 le joueur 1 gagne, si 2 le joueur gagne, si false aucun ne gagne
   :rtype: booléen/entier
   """
    if pions.pion_captures(grille,pion1) == 8 and pions.pion_captures(grille,pion1_2) ==8:
        return 2
    elif pions.pion_captures(grille,pion2) == 8 and pions.pion_captures(grille,pion2_2) ==8:
        return 1
    if True in debug:
        print(pion1 + ":" +str(pions.pion_captures(grille,pion1)))
        print(pion1_2 + ":" +str(pions.pion_captures(grille,pion1_2)))
        print(pion2 + ":" +str(pions.pion_captures(grille,pion2)))
        print(pion2_2 + ":" +str(pions.pion_captures(grille,pion2_2)))
    return False