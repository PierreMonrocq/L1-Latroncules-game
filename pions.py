from tkinter import *
import plateau as plateau
import gestionnaire_images as g_images
import gestionnaire_evenements as g_evenements

"""
Created on Mon Mar 20 18:52:54 2017

@author: Pierre Monrocq
"""
tour = 0

def generer_grille_pions(n,char):
    """
    genere une grille de dimension n avec comme lettre char
        
   :param n: dimension
   :type n: entier
   :param char: caractére à mettre dans la grille
   :type char: caractére
   :return: une grille de dimension n
   :rtype: liste
   """
    grille=[0]*n
    for i in range(n):
        grille[i]= [char]*n
    return grille

def ajouter_pions_grille(n):
    """
    Ajoute les pions a une grille de dimension n
        
   :param n: dimension
   :type n: entier
   :return: une grille de dimension n
   :rtype: liste
   """
    grille = generer_grille_pions(n,"-")
    for i in range(8):
        if i%2 == 0:#cases paires
            grille[i] [0] = "f"
            grille[i] [1] = "c"
            grille[i] [6] = "F"
            grille[i] [7] = "C"
        else:#cases impaires
            grille[i] [0] = "c"
            grille[i] [1] = "f"
            grille[i] [6] = "C"
            grille[i] [7] = "F"
    return grille

def afficher_pions_plateau_plat(grille,canvas):
    """
    affiche le plateau isometrique a partir de la grille
        
   :param grille: grille du plateau
   :type grille: liste
   :param canvas: canvas tkinter
   :type canvas: objet tkinter
   :rtype: void
   """
    for j in range(8):
        for i in range(8):
            x,y = plateau.position_cases_plat(i,j)
            if grille[i][j] == "f":
                case = canvas.create_image(x,y,image=g_images.fantassin_noir_plat)
                plateau.ajouter_id_element(canvas,"img",case)
            elif grille[i][j] == "c":
                case = canvas.create_image(x,y,image=g_images.cavalier_noir_plat)
                plateau.ajouter_id_element(canvas,"img",case)
            elif grille[i][j] == "C":
                case = canvas.create_image(x,y,image=g_images.cavalier_blanc_plat)
                plateau.ajouter_id_element(canvas,"img",case)
            elif grille[i][j] == "F":
                case = canvas.create_image(x,y,image=g_images.fantassin_blanc_plat)
                plateau.ajouter_id_element(canvas,"img",case)
    canvas.pack()
    
def afficher_pions_plateau_iso(grille,canvas):
    """
    affiche le plateau isometrique a partir de la grille
        
   :param grille: grille du plateau
   :type grille: liste
   :param canvas: canvas tkinter
   :type canvas: objet tkinter
   :rtype: void
   """
    for j in range(8):
        for i in range(8):
            x,y = plateau.position_cases_iso(i,j)
            if grille[i][j] == "f":
                case_iso = canvas.create_image(x,y,image=g_images.fantassin_noir_iso)
                plateau.ajouter_id_element(canvas,"img_iso",case_iso)
            elif grille[i][j] == "c":
                case_iso = canvas.create_image(x,y,image=g_images.cavalier_noir_iso)
                plateau.ajouter_id_element(canvas,"img_iso",case_iso)
            elif grille[i][j] == "C":
                case_iso = canvas.create_image(x,y,image=g_images.cavalier_blanc_iso)
                plateau.ajouter_id_element(canvas,"img_iso",case_iso)
            elif grille[i][j] == "F":
                case_iso = canvas.create_image(x,y,image=g_images.fantassin_blanc_iso)
                plateau.ajouter_id_element(canvas,"img_iso",case_iso)
    canvas.pack()
            

def deplacer_pions(canvas,grille,i,j,x,y,*debug):
    """
    déplace un pion sur le plateau
    
   :param canvas: canvas tkinter
   :type canvas: objet tkinter
   :param grille: grille du plateau
   :type grille: liste
   :param i: coordonnée de départ i
   :type i: entier
   :param j: coordonnée de départ j
   :type j: entier
   :param x: coordonnée d'arrivé x
   :type x: entier
   :param y: coordonnée d'arrivé y
   :type y: entier
   :return: grille
   :rtype: liste
   """
    grille[x][y] = grille[i][j]
    grille[i][j] = "-"
    canvas.delete("img")
    canvas.delete("img_iso")
    if True in debug:
        print(grille)
    if "log" in debug:
        print("[LOG] Déplacement du pion " + str(grille[x][y]) + " case " + str((i,j)) + " à la case " + str((x,y)))
    return grille

        
def afficher_indicateur(canvas,i,j,nom,image):
    """
    Affiche un indicateur à l'emplacement de la selection
    
   :param canvas: canvas tkinter
   :type canvas: objet tkinter
   :param grille: grille du plateau
   :type grille: liste
   :param i: coordonnée de départ i
   :type i: entier
   :param j: coordonnée de départ j
   :type j: entier
   :param nom: nom de l'indicateur
   :type x: caractére
   :param image: image convertie tkinter
   :type image: image
   :rtype: void
   """
    x,y = plateau.position_cases_plat(i,j)
    indicateur = canvas.create_image(x,y,image=image)
    canvas.addtag_withtag(nom, indicateur)
    
def selectionner_pion(event,grille,can,*debug):
    """
    selectionne un pion
   
   :param event: evenement tkinter
   :type event: evenement tkinter
   :param can: canvas tkinter
   :type cans: objet tkinter
   :param grille: grille du plateau
   :type grille: liste
   :rtype: void
   """
    global xs,ys
    try:
        plateau.supprimer_indicateur(can,"dep")
        plateau.supprimer_indicateur(can,"dep_imp")
        plateau.supprimer_indicateur(can,"ind")
        xs,ys = plateau.correspond(event.x,event.y)
        
        if(g_evenements.vue !=-1 and grille[xs][ys] != "-" and xs > -1 and ys > -1 and xs<8):
            if g_evenements.tour_joueur(tour) == 'n':
                if grille[xs][ys] == "f":
                    g_evenements.calculs_deplacements(can,grille,"f",xs,ys)
                    g_evenements.afficher_deplacements(can)
                    afficher_indicateur(can,xs,ys,"ind",g_images.selecteur)
                elif grille[xs][ys] == "c":
                    g_evenements.calculs_deplacements(can,grille,"c",xs,ys)
                    g_evenements.afficher_deplacements(can)
                    afficher_indicateur(can,xs,ys,"ind",g_images.selecteur)
            else:
                if grille[xs][ys] == "F":
                    g_evenements.calculs_deplacements(can,grille,"F",xs,ys)
                    g_evenements.afficher_deplacements(can)
                    afficher_indicateur(can,xs,ys,"ind",g_images.selecteur)
                elif grille[xs][ys] == "C":
                    g_evenements.calculs_deplacements(can,grille,"C",xs,ys)
                    g_evenements.afficher_deplacements(can)
                    afficher_indicateur(can,xs,ys,"ind",g_images.selecteur)
        if debug:
            print(xs,ys)
    except IndexError as ex:#Pass IndexError: clique en dehors de la fenetre
        plateau.supprimer_indicateur(can,"ind")
        plateau.supprimer_indicateur(can,"dep")
        plateau.supprimer_indicateur(can,"dep_imp")
        pass
    
def deplacer_pion(event,fenetre,grille,can):
    """
    deplace un pion
   
   :param event: evenement tkinter
   :type event: evenement tkinter
   :param fenetre: fenetre tkinter
   :type fenetre: fenetre tkinter
   :param can: canvas tkinter
   :type can: objet tkinter
   :param grille: grille du plateau
   :type grille: liste
   :rtype: void
   """
    global x,y
    global tour
    x,y = plateau.correspond(event.x,event.y)    
    try:
        if g_evenements.tour_joueur(tour) == 'b' and g_evenements.case_vide(grille,x,y) == True and (grille[xs][ys] == "C" or grille[xs][ys] == "F"):
            if g_evenements.confirmer_deplacement(x,y) == True:
                plateau.supprimer_indicateur(can,"ind")
                deplacer_pions(can,grille,xs,ys,x,y,"log")
                g_evenements.capture(grille,x,y)
                tour +=1
            plateau.supprimer_indicateur(can,"dep")
            plateau.supprimer_indicateur(can,"dep_imp")
        elif g_evenements.tour_joueur(tour) == 'n'and g_evenements.case_vide(grille,x,y) == True and (grille[xs][ys] == "c" or grille[xs][ys] == "f"):
            if g_evenements.confirmer_deplacement(x,y) == True:
                plateau.supprimer_indicateur(can,"ind")
                deplacer_pions(can,grille,xs,ys,x,y,"log")
                g_evenements.capture(grille,x,y)
                tour +=1
            plateau.supprimer_indicateur(can,"dep")
            plateau.supprimer_indicateur(can,"dep_imp")
        promotion_pions(grille,0,7,"F","C","f","c")
        afficher_pions_captures(can,grille,"C","c",g_images.cavalier_blanc_plat,g_images.cavalier_noir_plat)
        afficher_pions_plateau_plat(grille,can)
        afficher_pions_plateau_iso(grille,can)
        gagnant = g_evenements.gagner_partie(grille,"F","C","f","c")
        g_evenements.afficher_tour(can,tour,g_images.tourn,g_images.tourb)
        if gagnant != False:
            tour = 0
            g_evenements.partie_gagner(fenetre,can,gagnant,"blancs","noires")
    except IndexError:#Pass IndexError: clique en dehors de la fenetre
        plateau.supprimer_indicateur(can,"ind")
        plateau.supprimer_indicateur(can,"dep")
        plateau.supprimer_indicateur(can,"dep_imp")
        print("erreur")
        pass
    
def pion_captures(grille,pion):
    """
    fonction qui gère la capture d'un pion
   
   :param grille: grille du plateau
   :type grille: evenement tkinter
   :return: nombre de pion restant
   :rtype: entier
   """
    compteur = 8
    for i in range(len(grille)):
        for j in range(len(grille)):
            if grille[i][j] == pion:
                compteur -= 1
    return compteur

def promotion_pions(grille,y1,y2,pion1,pion1_promo,pion2,pion2_promo):
    for i in range(len(grille)):
        if grille[i][y1] == pion1:
            if pion_captures(grille,pion1_promo) > 0:
                grille[i][y1] = pion1_promo
        elif grille[i][y2] == pion2:
            if pion_captures(grille,pion2_promo) > 0:
                grille[i][y2] = pion2_promo
                      
def afficher_pions_captures(can,grille,pion1,pion2,image_pion1,image_pion2):
    plateau.supprimer_indicateur(can,"pion_capture")
    p1 = pion_captures(grille,pion1)
    p2 = pion_captures(grille,pion2)
    for i in range(p1):
        y = 0
        x = 0
        if i>3:
            y = 60
            x = -240
        pion = can.create_image(30+i*60+x,100+y,image=image_pion1)
        plateau.ajouter_id_element(can,"pion_capture",pion)
    for i in range(p2):
        y = 0
        x = 0
        if i>3:
           y = 60
           x = -240
        pion = can.create_image(785+i*60+x,460+y,image=image_pion2)
        plateau.ajouter_id_element(can,"pion_capture",pion)    
                