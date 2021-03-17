from tkinter import *

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:48:54 2017

@author: Pierre Monrocq
"""

CASE_LARGEUR = 120
CASE_HAUTEUR = 60

DECALAGE_X = 80 # decalage axe x a partir de la gauche de la fenetre
DECALAGE_Y = 100 # decalage axe y a partir du haut de la fenetre


CASE_PLAT = 60
DECALAGE_X_PLAT = 290
DECALAGE_VUE_Y = 580
x0_plat,y0_plat = 260,70


def generation_plateau_iso(canvas,image1,image2,*debug):
    """
    Génère le plateau isometrique dans un canvas
    
   :param canvas: canvas Tkinter
   :type canvas: objet Tkinter
   :param image1: image d'une case isometrique
   :type image1: image convertie
   :param image2: image d'une case isometrique
   :type image2: image convertie
   :param *debug: affiche des informations de debug dans la console
   :type *debug: booléen
   :rtype: void
   """
    for j in range(8):#lignes
        for i in range(8):#colonnes
            x,y = position_cases_iso(i,j)
            if (j+i)%2 == 0: #si case blanche
                case_iso = canvas.create_image(x,y,image=image2)
                ajouter_id_element(canvas,"iso",case_iso)
                if True in debug:
                    print("case_blanche: "+str(x)+","+str(y))
            else:#si case noire
                case_iso = canvas.create_image(x,y,image=image1)
                ajouter_id_element(canvas,"iso",case_iso)
                if True in debug:
                    print("case_noire: "+str(x)+","+str(y))
    canvas.pack()

def generation_plateau_plat(canvas,image1,image2,*debug):
    """
    Génère le plateau plat dans un canvas
    
   :param canvas: canvas Tkinter
   :type canvas: objet Tkinter
   :param image1: image d'une case plate
   :type image1: image convertie
   :param image2: image d'une case plate
   :type image2: image convertie
   :param *debug: affiche des informations de debug dans la console
   :type *debug: booléen
   :rtype: void
   """
    dessous = canvas.create_rectangle(x0_plat-5,y0_plat-5,x0_plat+8*60+5,y0_plat+8*60+5,fill="#8c8c8b")
    ajouter_id_element(canvas,"plat",dessous)
    for j in range(8):#lignes
        for i in range(8):#colonnes
            x,y = position_cases_plat(i,j)
            if (j+i)%2 == 0:
              case_plat = canvas.create_image(x,y,image=image2)
              ajouter_id_element(canvas,"plat",case_plat)
              if True in debug:
                    print("case_blanche: "+str(x)+","+str(y))
            else:
              case_plat = canvas.create_image(x,y,image=image1)
              ajouter_id_element(canvas,"plat",case_plat)
              if True in debug:
                    print("case_noire: "+str(x)+","+str(y))
    canvas.pack()

def position_cases_iso(i,j): #calcul inspiré et adapté d'un article: http://clintbellanger.net/articles/isometric_math/
    """
    Associes des coordonnées à des cases par rapport à des valeurs en pixel et renvoit leurs positions 
    dans un espace isometrique
    
   :param i: coordonnée i correspond à l'abscisse d'une case
   :type i: entier
   :param j: coordonnée j correspond à l'ordonné d'une case
   :type i: entier
   :rtype: tuple
   :return: position des cases i,j en pixel
   >>>position_cases_iso(0,0)
   (450,250)
   """
    debut_x = (-j+7)*CASE_LARGEUR/2+DECALAGE_X
    debut_y = (j*CASE_HAUTEUR/2)+DECALAGE_Y + DECALAGE_VUE_Y
    x = debut_x + (i*CASE_LARGEUR/2)
    y = debut_y + (i*CASE_HAUTEUR/2)
    return(x,y)
    
def position_cases_plat(i,j):
    """
    Associes des coordonnées à des cases par rapport à des valeurs en pixel et renvoit leurs positions 
    dans un espace plat
    
   :param i: coordonnée i correspond à l'abscisse d'une case
   :type i: entier
   :param j: coordonnée j correspond à l'ordonné d'une case
   :type i: entier
   :rtype: tuple
   :return: position des cases i,j en pixel
       >>>position_cases_iso(0,0)
        (450,250)
   """
    debut_x = DECALAGE_X_PLAT+(CASE_PLAT/2*i)
    debut_y = DECALAGE_Y+(CASE_PLAT/2*j) 
    x = debut_x + (i*CASE_PLAT/2)
    y = debut_y + (j*CASE_PLAT/2)
    return(x,y)

def generer_plateaux(canvas,image1,image2,image3,image4,*debug):
    """
    Génère les plateau isometrique et plat
    
   :param canvas: canvas Tkinter
   :type canvas: objet Tkinter
   :param image1: image d'une case plate
   :type image1: image convertie
   :param image2: image d'une case plate
   :type image2: image convertie
   :param image3: image d'une case plate
   :type image3: image convertie
   :param image4: image d'une case plate
   :type image4: image convertie
   :param *debug: affiche des informations de debug dans la console (optionel)
   :type *debug: booléen
   :rtype: void
   """
    try:
        if(debug):
            generation_plateau_iso(canvas,image1,image2,True)
            generation_plateau_plat(canvas,image3,image4,True)
        else:
            generation_plateau_plat(canvas,image3,image4)
            generation_plateau_iso(canvas,image1,image2)   
    except Exception as ex: #fonction d'exception récupérée sur stackoverflow
        template = "Une erreur de type {0} a eu lieu. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def couleur_case(i,j):
    """
    Détermine la couleur d'une case dans le plateau au coordonnées (i,j)
    
   :param i: coordonnée i correspond à l'abscisse d'une case
   :type i: entier
   :param j: coordonnée j correspond à l'ordonnée d'une case
   :type j: entier
   :rtype: booléen
   :return: True pour la couleur blanc, False pour la couleur noire
   """
    if (i+j)%2 == 0:
        return True #Blanc
    return False

def dans_plateau(x,y):
    """
    Verifie si des coordonnées x,y sont bien comprises dans le plateau de jeu
    
   :param x: coordonnée x
   :type x: entier
   :param y: coordonnée y
   :type y: entier
   :rtype: booléen
   :return: True dans le plateau sinon False en dehors
   """
    if x > -1 and x < 8 and y > -1 and y < 8:
        return True
    return False

def correspond(x,y):
    """
    Associe une valeur en pixel x,y à une case du plateau plat
    
   :param x: valeur x en pixel (abscisse)
   :type x: entier
   :param y: valeur y en pixel (abscisse)
   :type y: entier
   :rtype: tuple
   :return: valeur des cases i et j
   >>>correspond(350,850)
   (5,4)
   """
    return [(x-x0_plat)//CASE_PLAT,(y-y0_plat)//CASE_PLAT]

def supprimer_indicateur(canvas,nom):
    """
    Supprime un indicateur dans un canvas
    
   :param canvas: canvas Tkinter
   :type canvas: objet Tkinter
   :param nom: tag associé à l'objet
   :type nom: chaine caractéres
   :rtype: void
   """
    canvas.delete(nom)

def ajouter_id_element(canvas,tag,element):
    """
    Ajoute un tag (identification Tkinter) a un element
    
   :param canvas: canvas Tkinter
   :type canvas: objet Tkinter
   :param tag: tag à associer à l'objet
   :type tag: chaine caractéres
   :param element: variable
   :rtype: void
   """
    return canvas.addtag_withtag(tag, element)

def recuperer_id_element(canvas,tag):
    """
    Recupere un element à partir d'un tag et renvoit son id
    
   :param canvas: canvas Tkinter
   :type canvas: objet Tkinter
   :param tag: tag à associer à l'objet
   :type tag: chaine caractéres
   :rtype: id tkinter
   """
    return canvas.find_withtag(tag)