"""
Ce programme affiche la table de multiplication
 à partir d'une base saisie au clavier
Auteur : Papa Alassane Ndiaye
Superviseur : Mohamed Bah
Version : 1.0.0
Date : Annéé 2020
"""

def multibase(base):
    compteur = 1
    while (compteur <= 12):
        print(f"{base} X {compteur} = {base * compteur}")
        compteur += 1

"""
base = int(input("Donner une base:"))
compteur = 1
while(compteur <= 12):
    print(f"{base} X {compteur} = {base * compteur}")
    compteur += 1
"""