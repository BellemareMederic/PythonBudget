#!/bin/python
# Look at http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python;

import datetime
import os
from socket import *

from Termcolor import colored

# Version TCP PythonFacture-obj
VERSION = (1, 2, 3)
TAXEPROV = 9.975
TAXEFED = 5
PORT = 5555


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Magasin:
    nom = "N/A"
    total = 0
    totaltaxe = 0
    formatpaye = "N/A"
    categorie = "N/A"
    description = "N/A"
    finaltips = None

    def getfinaltips(self):
        return float(self.finaltips)

    def setfinaltips(self, finaltips):
        self.finaltips = finaltips

    def getnom(self):
        return str(self.nom)

    def getformatpaye(self):
        return str(self.formatpaye)

    def getcategorie(self):
        return str(self.categorie)

    def gettotal(self):
        return float(self.total)

    def getdescription(self):
        return str(self.description)

    def setnom(self, name):
        self.nom = name

    def setformatpaye(self, formatpaye):
        self.formatpaye = formatpaye

    def setcategorie(self, categorie):
        self.categorie = categorie

    def settotal(self, total):
        self.total = total

    def setdescription(self, description):
        self.description = description

    # TODO utiliser la reutilisation car Save ce ressemble beaucoup
    def save(self):
        time = datetime.date.today()
        r = None
        try:
            if os.name == 'nt':
                r = open("Facture.csv", "a")
                path = "./Facture.csv"
            elif os.name == 'posix':
                if os.path.exists("/mnt/sdcard"):
                    r = open("/mnt/sdcard/Facture.csv", "a")
                    path = "/mnt/sdcard/Facture.csv"
                else:
                    r = open("Facture.csv", "a")
                    path = "./Facture.csv"
            r.write(str(time.strftime("%Y-%m-%d")) + ";")
            r.write(str(self.nom) + ";")
            r.write(str(self.formatpaye) + ";")
            r.write(str(self.categorie) + ";")
            if self.categorie != "Restaurant":
                r.write(str(self.totaltaxe).replace(".", ",") + ";")
            else:
                r.write(str(self.totaltaxe + self.finaltips).replace(".", ",") + ";")
            r.write(str(self.description) + ";\n")
        except Exception as e:
            print(colored("Une erreur est survenue durent la sauvgarde du document Facture.CSV.", "red"))
            print(colored("Veuillez verifier que le document sois bien fermer et non proteger.", "red"))
            print(colored(e, "cyan"))
            pass
        print("Le fichier est sauvgarder sous ", path)

    def calc(self):
        self.totaltaxe = self.total + (self.total / 100 * TAXEPROV) + (self.total / 100 * TAXEFED)

    def afficher(self):
        self.calc()
        print("\n---===Facture===---")
        print("Nom :", self.getnom())
        print("Description :", self.description)
        print("Catégorie :", self.categorie)
        print("Sous-total :", "%.2f" % float(self.total))
        if self.categorie == "Restaurant":
            print("Tips :", self.finaltips)
            print("Total :", "%.2f" % (float(self.totaltaxe) + float(self.finaltips)))
        else:
            print("Total :", "%.2f" % float(self.totaltaxe))


choix = 1
while choix != 0:
    clear()
    print("----------==========Gestion Facture==========----------")
    print("1.Achat restauration")
    print("2.Achat en magasin")
    print("3.Envoyer votre fichier CSV")
    print("4.Recevoir votre fichier CSV")
    while True:
        try:
            choix = int(input("Quelle est votre type achat :"))
        except ValueError:
            print("L'entrer n'est pas un nombre")
            continue
        else:
            break

    if choix == 1:

        Restaurent1 = Magasin()

        while True:
            try:
                Restaurent1.settotal(float((input("Quelle est le montant de la facture :"))))
            except ValueError:
                print("L'entrer n'est pas un nombre")
                continue
            else:
                if Restaurent1.gettotal() < 0:
                    print("Le nombre entrer n'est pas positife")
                    continue
                else:
                    break

        for i in range(5, 35, 5):
            print("Tips a", "(" + str(i) + "%) = ", "%.2f" % (Restaurent1.total / 100 * i), "$")
        while True:
            try:
                Restaurent1.setfinaltips(float(input("Quelle est le pourcentage de tips laisser :")))
            except ValueError:
                print("L'entrer n'est pas un nombre")
                continue
            else:
                if Restaurent1.gettotal() < 0:
                    print("Le nombre entrer n'est pas positife")
                    continue
                else:
                    break

        Restaurent1.setcategorie("Restaurant")
        Restaurent1.setformatpaye(str(input("Quelle est le format paiment (VISA,Cash) :")))
        Restaurent1.setnom(str(input("Quelle est le nom du magasin :")))
        Restaurent1.setdescription(str(input("Quelle est la description :")))
        Restaurent1.afficher()
        Restaurent1.save()

    if choix == 2:

        magasin1 = Magasin()

        while True:
            try:
                magasin1.settotal(float((input("Quelle est le montant de la facture :"))))
            except ValueError:
                print("L'entrer n'est pas un nombre")
                continue
            else:
                if magasin1.gettotal() < 0:
                    print("Le nombre entrer n'est pas positife")
                    continue
                else:
                    break
        catego = 0
        list_categorie = {0: "Épicerie", 1: "Activité", 2: "Aménagement", 3: "Hygiène", 4: "Transport", 5: "Logement",
                          6: "Vêtements", 7: "École", 8: "Divers"}
        for i in range(0, len(list_categorie)):
            print(i, ".", list_categorie[i], sep='')

        while True:
            try:
                catego = int(input("Quelle est la catégorie :"))
            except ValueError:
                print("L'entrer n'est pas un nombre")
                continue
            else:
                if catego in list_categorie:
                    break
                else:
                    print("Le nombre entrer ne fais pas partie des choix")

        magasin1.setcategorie(list_categorie[catego])
        magasin1.setformatpaye(str(input("Quelle est le format paiment (VISA,Cash) :")))
        magasin1.setnom(str(input("Quelle est le nom du magasin :")))
        magasin1.setdescription(str(input("Quelle est la description :")))
        magasin1.afficher()
        magasin1.save()
    if choix == 4:
        sockrecv = socket()  # Create a socket object
        host = input("Entrer le nom de l'apparail")  # Get local machine name

        sockrecv.connect((host, PORT))
        sockrecv.send(bytes("Hello server!", 'UTF-8'))
        with open('Facture_android.csv', 'wb') as f:
            while True:
                print('Récuperation du fichier...')
                data = sockrecv.recv(1024)
                if not data:
                    print("Le fichier recu est vide")
                    break
                # write data to a file
                f.write(data)

        f.close()
        print('Fichier Recu !')
        sockrecv.close()
        print('Connection fermer')
    if choix == 3:
        socksend = socket()
        host = gethostname()
        socksend.bind((host, PORT))
        socksend.listen(5)

        print("Nom de l'apparail", host)
        print('En attente de la récupération du fichier CSV....')

        while True:
            conn, addr = socksend.accept()  # Establish connection with client.
            print('Connecter a', addr)
            data = conn.recv(1024)
            print('Envoie du fichier...')
            filename = 'Facture.csv'
            f = open(filename, 'rb')
            l = f.read(1024)
            while (l):
                conn.send(l)
                print('Envoyer ', repr(l))
                l = f.read(1024)
                conn.sendall(data)
            conn.close()

            print('Envoie terminer')
            break

    print("Presser une touche pour continuer")
    input()
