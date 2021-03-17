from tkinter import *

fenetre = Tk()

import debug as de
import sauvegarde as sauvegarde
import plateau as plateau
import pions as pions
import gestionnaire_evenements as g_evenements
import menu as menu
import gestionnaire_images as g_images
import ast



# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:48:54 2017

@author: Pierre Monrocq
"""

#Paramètres d'affichage
fenetre.title('Latroncules')
FENETRE_LARGEUR = "1000"
FENETRE_HAUTEUR = "580"
fenetre.geometry(FENETRE_LARGEUR+"x"+FENETRE_HAUTEUR)
fenetre.resizable(0, 0)
can = Canvas(fenetre,height=FENETRE_HAUTEUR,width=FENETRE_LARGEUR,bg="#d5d5d5")

#Menu
imgmenu = can.create_image(500,290,image=g_images.menu)
bm = Button(can, text="NOUVELLE PARTIE",fg="#f5f5f5",bg="#262625",highlightthickness = 0,bd=0,borderwidth=5,font = ('Helvetica',12))
bm2 = Button(can, text="CONTINUER PARTIE",fg="#f5f5f5",bg="#262625",highlightthickness = 0,bd=0,borderwidth=5,font = ('Helvetica',12))
bm4 = Button(can, text="QUITTER",fg="#f5f5f5",bg="#262625",highlightthickness = 0,bd=0,borderwidth=5,font = ('Helvetica',12))
bm3 = Button(can, text="AIDE",fg="#f5f5f5",bg="#262625",highlightthickness = 0,bd=0,borderwidth=5,font = ('Helvetica',12))

bm.configure(width=20,height=1,activebackground = "#b9b8b6", relief = FLAT, command= lambda: lancer_jeu(can))
bm2.configure(width=20,height=1,activebackground = "#b9b8b6", relief = FLAT, command= lambda: lancer_jeu(can,True),state=DISABLED)
bm3.configure(width=20,height=1,activebackground = "#b9b8b6", relief = FLAT,command= lambda: print("Merci de consulter le mode mode d’emploi, situé dans le dossier rapport."))
bm4.configure(width=20,height=1,activebackground = "#b9b8b6", relief = FLAT, command=fenetre.destroy)

bm.place(relx=0.5,rely=0.48,anchor=CENTER)
bm2.place(relx=0.5,rely=0.38,anchor=CENTER)
bm4.place(relx=0.5,rely=0.68,anchor=CENTER)
bm3.place(relx=0.5,rely=0.58,anchor=CENTER)
can.pack()

if(sauvegarde.fichier_existant() == True):#Si il y a déjà une partie enregistrée
    bm2.configure(state=NORMAL)
    can.pack()

def lancer_jeu(can,*continuer):
    """
    Lance le jeu et appel les autres fonctions

   :param can: Canvas Tkinter
   :type can: Objet Tkinter
   :param continuer: Si la condition continuer est vraie le jeu charge une partie existante (default false) (facultatif)
   :type continuer: Booléen
   """
    #Debut du calcul du temps d'execution
    deb = de.afficher_temps_execution_debut()

    #suppression du menu
    global bm,bm2,bm3,bm4,imgmenu
    bm2.configure(state=NORMAL)
    menu.supprimer_boutons_menu(bm,bm2,bm3,bm4)
    menu.supprimer_fond_menu(can,imgmenu)

    #Fonctions de création du plateau
    plateau.generer_plateaux(can,g_images.case_noire_iso,g_images.case_blanche_iso,g_images.case_noire_plat,g_images.case_blanche_plat)
    if(True in continuer):#Chargement d'une partie existante
        grille = ast.literal_eval(sauvegarde.charger_grille_partie())
        pions.tour = int(sauvegarde.charger_tour_partie())
        pions.afficher_pions_captures(can,grille,"C","c",g_images.cavalier_blanc_plat,g_images.cavalier_noir_plat)
    else:#sinon creation d'une nouvelle partie
        grille = pions.ajouter_pions_grille(8)
    pions.afficher_pions_plateau_plat(grille,can)
    pions.afficher_pions_plateau_iso(grille,can)
    g_evenements.afficher_tour(can,pions.tour,g_images.tourn,g_images.tourb)
    de.afficher_temps_execution_fin(deb, "Lancement en")

    #Boutons en jeu
    but = Button(can, text="CHANGER DE VUE", command= lambda: g_evenements.changement_vue(can),fg="#f5f5f5",bg="#8c8c8b",highlightthickness = 0,bd=0,borderwidth=5)
    but.configure(width = 14, activebackground = "#b9b8b6", relief = FLAT)
    but.place(relx=0.1,rely=0.05,anchor=CENTER)
    b2 = Button(can, text="NOUVELLE PARTIE",fg="#f5f5f5",bg="#8c8c8b",highlightthickness = 0,bd=0,borderwidth=5)
    b2.configure(width = 14, activebackground = "#b9b8b6", relief = FLAT,command=lambda: g_evenements.partie_termine(fenetre,can))
    b2.place(relx=0.9,rely=0.05,anchor=CENTER)

    #Evenements
    can.bind("<Button-1>",lambda event: pions.selectionner_pion(event,grille,can))
    can.bind("<Button-3>",lambda event: pions.deplacer_pion(event,fenetre,grille,can))
    fenetre.protocol("WM_DELETE_WINDOW",lambda: g_evenements.confirmer_quitter(fenetre,grille,pions.tour))

#Execution de la boucle principale Tkinter
fenetre.mainloop()
