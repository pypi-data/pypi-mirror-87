def bisextile(annee):
    if annee % 400 == 0:
        bissextile = True
    elif annee % 100 == 0:
         bissextile = False
    elif annee % 4 == 0:
         bissextile = True
    else:
         bissextile = False
    print(f'{annee} bissextile ?: {bissextile}')

 

if __name__ == "__main__":
    annee = int(input("Saisir l'annee: "))
    bisextile(annee)
