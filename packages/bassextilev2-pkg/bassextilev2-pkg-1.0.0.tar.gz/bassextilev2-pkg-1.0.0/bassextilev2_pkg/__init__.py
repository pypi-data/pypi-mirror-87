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

"""
Ce programme test si une année saisie au clavier
est bisextile ou pas
Auteur : Papa Alassane Ndiaye
Superviseur : Mohamed Bah
Version : 1.0.0
Date : Annéé 2020
"""


def bissextile(annee):
    if ((annee % 400 == 0) or (annee % 4 == 0 and annee % 100 != 0)):
        print(f'l\'an {annee} est bissextile')
    else:
        print(f'l\'an {annee} n est pas bissextile')













""""
annee = int(input("Donner une année:"))
if((annee % 400 == 0) or (annee % 4 == 0 and annee % 100 != 0)):
    bissextile = True
else:
    bissextile = False

#Affichage du resultat
print(f'{annee} bissextile ?: {bissextile}')
"""