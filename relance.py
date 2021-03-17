from tkinter import *
import plateau as plateau
import gestionnaire_evenements as g_evenements
import pions as pions
import debug as de
import gestionnaire_images as g_images

def recommencer_jeu(fenetre,can,*debug):
    """
    Relance le jeu avec certains paramètres

   :param can: Canva Tkinter
   :type can: Objet Tkinter
   :param continuer: Si la condition continuer est vraie le jeu charge une partie existante (default false) (facultatif)
   :type continuer: Booléen
   """
    deb = de.afficher_temps_execution_debut()
  
    #Fonctions
    plateau.generer_plateaux(can,g_images.case_noire_iso,g_images.case_blanche_iso,g_images.case_noire_plat,g_images.case_blanche_plat)
    grille = pions.ajouter_pions_grille(8)
    pions.afficher_pions_plateau_iso(grille,can)
    pions.afficher_pions_plateau_plat(grille,can)
    pions.tour = 0
    g_evenements.afficher_tour(can,pions.tour,g_images.tourn,g_images.tourb)
    pions.afficher_pions_captures(can,grille,"C","c",g_images.cavalier_blanc_plat,g_images.cavalier_noir_plat)
    de.afficher_temps_execution_fin(deb, "Lancement en")

    #Evenements
    can.bind("<Button-1>",lambda event: pions.selectionner_pion(event,grille,can))
    can.bind("<Button-3>",lambda event: pions.deplacer_pion(event,fenetre,grille,can))
    fenetre.protocol("WM_DELETE_WINDOW",lambda: g_evenements.confirmer_quitter(fenetre,grille,pions.tour))
    
    if True in debug:
        print(grille)