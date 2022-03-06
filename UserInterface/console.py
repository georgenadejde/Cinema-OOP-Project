from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from datetime import datetime, time, date
from copy import copy

from Service.undo_redo_service import UndoRedoService


class Console:
    def __init__(self, filmService : FilmService, cardClientService : CardClientService, rezervareService : RezervareService,
                 undo_redo_service: UndoRedoService):
        self.filmService = filmService
        self.cardClientService = cardClientService
        self.rezervareService = rezervareService
        self.undo_redo_service = undo_redo_service

    def runMenu(self):
        while True:
            print("1. CRUD Filme")
            print("2. CRUD Carduri Client")
            print("3. CRUD Rezervari")
            print("4. Operatii")
            print("g. Genereaza filme")
            print("x. Iesire")
            optiune = input("Selectati optiunea: ")

            if optiune == '1':
                self.runCrudFilme()
            elif optiune == '2':
                self.runCrudCarduri()
            elif optiune == '3':
                self.runCrudRezervari()
            elif optiune == '4':
                self.runOperationsMenu()
            elif optiune == 'g':
                self.genereazaFilme()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida!")

    def runOperationsMenu(self):
        while True:
            print("4. Cautare full text in filme si carduri clienti")
            print("5. Afișarea tuturor rezervărilor dintr-un interval de ore dat, indiferent de zi.")
            print("6. Afișarea filmelor ordonate descrescător după numărul de rezervări.")
            print("7. Afișarea cardurilor client ordonate descrescător după numărul de puncte de pe card.")
            print("8. Ștergerea tuturor rezervărilor dintr-un anumit interval de zile.")
            print("9. Incrementarea cu o valoare dată a punctelor de pe toate cardurile a căror zi de naștere se află într-un interval dat.")
            print("x. Iesire")
            optiune = input("Selectati optiunea: ")

            if optiune == '4':
                self.cautareFullText()
            elif optiune == '5':
                self.rezervariIntervalOre()
            elif optiune == '6':
                self.filmeOrdonateDescrDupaNrRezervari()
            elif optiune == '7':
                self.runCarduriDescrescator()
            elif optiune == '8':
                self.stergereRezervareDinInterval()
            elif optiune == '9':
                self.incrementareCarduriZiDeNastere()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida!")

    def incrementareCarduriZiDeNastere(self):
        try:
            valoare = int(input("Valoarea de incrementat: "))
            data1 = input("Dati prima data(dd.mm.yyyy): ")
            data1 = datetime.strptime(data1, "%d.%m.%Y")
            data2 = input("Dati a doua data(dd.mm.yyyy): ")
            data2 = datetime.strptime(data2, "%d.%m.%Y")
            delta = data2 - data1
            if delta.days >= 0:
                lista = self.cardClientService.incrementareCarduriZiDeNastereService(valoare, data1, data2)
            else:
                lista = self.cardClientService.incrementareCarduriZiDeNastereService(valoare, data2, data1)

            for mesaj in lista:
                print(mesaj)

        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def stergereRezervareDinInterval(self):
        zi1 = input("Dati prima zi(1 - 31): ")
        while True:
            if zi1.isdigit() == False or int(zi1) < 1 or int(zi1) > 31:
                print("Ziua introdusa nu corespunde formatului. Reincercati!")
                zi1 = input("Dati prima zi(1 - 31): ")
            else:
                break

        zi1 = int(zi1)

        zi2 = input("Dati a doua zi(1 - 31): ")
        while True:
            if zi2.isdigit() == False or int(zi2) < 1 or int(zi2) > 31:
                print("Ziua introdusa nu corespunde formatului. Reincercati!")
                zi2 = input("Dati a doua zi(1 - 31): ")
            else:
                break

        zi2 = int(zi2)

        if zi1 <= zi2:
            lista = self.rezervareService.stergereRezervareDinIntervalService(zi1, zi2)
        else:
            lista = self.rezervareService.stergereRezervareDinIntervalService(zi2, zi1)

        for mesaj in lista:
            print(mesaj)

    def filmeOrdonateDescrDupaNrRezervari(self):
            lista = self.rezervareService.filmeOrdonateDescrDupaNrRezervariService()
            for film in lista:
                rezervari = self.rezervareService.numarRezervariFilm(film)
                print(film, f"({rezervari} rezervari)")

    def rezervariIntervalOre(self):
        print("Dati intervalul de ore")
        while True:
            try:
                ora1 = input("Ora1(HH:MM): ")
                datetime.strptime(ora1, "%H:%M")
                ora = int(str(ora1)[:2])
                minute = int(str(ora1)[3:5])
                ora1 = time(ora, minute)
                break
            except ValueError as ve:
                print("Formatul orei nu este cel corespunzator (HH:MM)! Reincercati!")

        while True:
            try:
                ora2 = input("Ora2(HH:MM): ")
                datetime.strptime(ora2, "%H:%M")
                ora = int(str(ora2)[:2])
                minute = int(str(ora2)[3:5])
                ora2 = time(ora, minute)
                break
            except ValueError as ve:
                print("Formatul orei nu este cel corespunzator (HH:MM)! Reincercati!")

        duration = datetime.combine(date.min, ora2) - datetime.combine(date.min, ora1)
        if len(str(duration)) > 8:
            lista = self.rezervareService.rezervariIntervalOreService(ora2, ora1)
        else:
            lista =self.rezervareService.rezervariIntervalOreService(ora1, ora2)

        for rezervare in lista:
            ora = rezervare.oraRezervare.strftime("%H:%M")
            print(f"id rezervare: {rezervare.idRezervare} \nfilm: {rezervare.film} \ncard: {rezervare.card}\ndata rezervare: {rezervare.dataRezervare} \nora rezervare: {ora}\n")

    def cautareFullText(self):
        string = input("Dati stringul de cautat: ")
        stringsList = []
        stringsList = self.filmService.cautareFullText(string, stringsList)
        stringsList = self.cardClientService.cautareFullText(string, stringsList)
        for x in stringsList:
            print(x)

    def runCarduriDescrescator(self):
        lista = self.cardClientService.ordonareDescrescatorPuncte()
        for card in lista:
            print(card)

    def genereazaFilme(self):
        n = int(input("dati numarul de filme de generat: "))
        self.filmService.generateFilm(n)

    def runCrudFilme(self):
        while True:
            print("1. Adaugare film")
            print("2. Stergere film")
            print("3. Modificare film")
            print("u. Undo")
            print("r. Redo")
            print("e. Export date intr-un fisier Excel")
            print("a. Afisarea filmelor")
            print("x. Inapoi in meniu")
            optiune = input("Selectati optiunea: ")
            if optiune == '1':
                self.uiAdaugareFilm()
            elif optiune == '2':
                self.uiStergereFilm()
            elif optiune == '3':
                self.uiModificareFilm()
            elif optiune == 'a':
                self.uiAfisareFilme()
            elif optiune == 'e':
                self.export()
            elif optiune == 'u':
                self.undo_redo_service.do_undo()
            elif optiune == 'r':
                self.undo_redo_service.do_redo()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida!")

    def export(self):
        self.filmService.exportService()

    def uiAdaugareFilm(self):
        try:
            idFilm = input("Dati id-ul: ")
            while idFilm.isdigit() == False or idFilm[0] == '0':
                print("Id incorect! Reincercati!")
                idFilm = input("Dati id-ul: ")
            titluFilm = input("Dati titlul: ")
            anAparitie = int(input("Dati anul aparitiei: "))
            pretFilm = int(input("Dati pretul: "))
            while pretFilm <= 0:
                print("Pretul trebuie sa fie strict pozitiv! Reincercati!")
                pretFilm = int(input("Dati pretul: "))
            inProgram = input("E in program (da/nu): ")
            self.filmService.adaugare(idFilm,titluFilm, anAparitie, pretFilm, inProgram)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)


    def uiStergereFilm(self):
        try:
            idStergere = input("Dati id-ul filmului de sters: ")
            while idStergere.isdigit() == False or idStergere[0] == '0':
                print("Id incorect! Reincercati!")
                idStergere = input("Dati id-ul: ")
            film = self.filmService.getFilm(idStergere)
            if film != None:
                numar = self.rezervareService.numarRezervariFilm(film)
                if numar > 0:
                    raise ValueError("Filmul nu se poate sterge! Exista o rezervare la filmul dat!")
            self.filmService.stergere(idStergere)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def uiModificareFilm(self):
        try:
            idFilm = input("Dati id-ul filmului de modificat: ")
            while idFilm.isdigit() == False or idFilm[0] == '0':
                print("Id incorect! Reincercati!")
                idFilm = input("Dati id-ul: ")
            titluFilm = input("Dati titlul filmului de modificat sau ENTER daca nu vreti sa il modificati: ")
            anAparitie = int(input("Dati anul aparitiei filmului de modificat sau 0 daca nu vreti sa il modificati: "))
            pretFilm = int(input("Dati pretul filmului de modificat sau 0 daca nu vreti sa il modificati: "))
            while pretFilm < 0:
                print("Pretul trebuie sa fie pozitiv! Reincercati!")
                pretFilm = int(input("Dati pretul: "))
            inProgram = input("E in program (da/nu) sau ENTER daca nu vreti sa il modificati: ")

            film = self.filmService.getFilm(idFilm)
            if film != None:
                numar = self.rezervareService.numarRezervariFilm(film)
                if numar > 0:
                   raise ValueError("Filmul nu se poate modifica! Exista o rezervare la filmul dat!")

            self.filmService.modificare(idFilm, titluFilm, anAparitie, pretFilm, inProgram)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def uiAfisareFilme(self):
        filme = self.filmService.getAll()
        for film in filme:
            print(film)

    def runCrudCarduri(self):
        while True:
            print("1. Adaugare card")
            print("2. Stergere card")
            print("3. Modificare card")
            print("u. Undo")
            print("r. Redo")
            print("a. Afisarea cardurilor")
            print("x. Inapoi in meniu")
            optiune = input("Selectati optiunea: ")
            if optiune == '1':
                self.uiAdaugareCard()
            elif optiune == '2':
                self.uiStergereCard()
            elif optiune == '3':
                self.uiModificareCard()
            elif optiune == 'u':
                self.undo_redo_service.do_undo()
            elif optiune == 'r':
                self.undo_redo_service.do_redo()
            elif optiune == 'a':
                self.uiAfisareCarduri()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida!")

    def uiAdaugareCard(self):
        try:
            idCard = input("Dati id-ul: ")
            while idCard.isdigit() == False or idCard[0] == '0':
                print("Id incorect! Reincercati!")
                idCard = input("Dati id-ul: ")
            numeCard = input("Dati numele: ")
            prenumeCard = input("Dati prenumele: ")
            CNP = input("Dati CNP-ul: ")
            while CNP.isdigit() == False or CNP[0] == '0':
                print("CNP-ul nu este valid! Reincercati!")
                CNP = input("Dati CNP-ul: ")
            dataNastere = input("Dati data nasterii (dd.mm.yyyy): ")
            dataNastere = datetime.strptime(dataNastere, "%d.%m.%Y")
            dataInregistrare = input("Dati data inregistrarii (dd.mm.yyyy): ")
            dataInregistrare = datetime.strptime(dataInregistrare, "%d.%m.%Y")
            puncteAcumulate = int(input("Puncte acumulate: "))
            self.cardClientService.adaugare(idCard, numeCard, prenumeCard, CNP, dataNastere, dataInregistrare, puncteAcumulate)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def uiStergereCard(self):
        try:
            idStergere = input("Dati id-ul cardului de sters: ")
            while idStergere.isdigit() == False or idStergere[0] == '0':
                print("Id incorect! Reincercati!")
                idStergere = input("Dati id-ul: ")

            card = self.cardClientService.getCard(idStergere)
            if card != None:
                numar = self.rezervareService.numarRezervariCard(card)
                if numar > 0:
                    raise ValueError("Cardul nu se poate sterge! Exista o rezervare cu cardul dat!")

            self.cardClientService.stergere(idStergere)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def uiModificareCard(self):
        try:
            idCard = input("Dati id-ul cardului de modificat: ")
            while idCard.isdigit() == False or idCard[0] == '0':
                print("Id incorect! Reincercati!")
                idCard = input("Dati id-ul: ")
            numeCard = input("Dati numele noii persoane (sau ENTER daca nu doriti sa modificati): ")
            prenumeCard = input("Dati prenumele noii persoane (sau ENTER daca nu doriti sa modificati): ")
            CNP = input("Dati CNP-ul noii persoane (sau ENTER daca nu doriti sa modificati): ")

            if CNP != "":
                while CNP.isdigit() == False :
                    print("CNP-ul nu este valid! Reincercati!")
                    CNP = input("Dati CNP-ul: ")
                    if CNP == "":
                        break

            dataNastere = input("Dati data nasterii (dd.mm.yyyy) sau ENTER daca nu doriti sa modificati: ")
            if dataNastere != "":
                dataNastere = datetime.strptime(dataNastere, "%d.%m.%Y")
            dataInregistrare = input("Dati data inregistrarii (dd.mm.yyyy) sau ENTER daca nu doriti sa modificati: ")
            if dataInregistrare != "":
                dataInregistrare = datetime.strptime(dataInregistrare, "%d.%m.%Y")

            puncteAcumulate = int(input("Puncte acumulate (sau 0 daca nu doriti sa modificati): "))

            card = self.cardClientService.getCard(idCard)
            if card != None:
                numar = self.rezervareService.numarRezervariCard(card)
                if numar > 0:
                    raise ValueError("Cardul nu se poate modifica! Exista o rezervare cu cardul dat!")

            self.cardClientService.modificare(idCard, numeCard, prenumeCard, CNP, dataNastere, dataInregistrare, puncteAcumulate)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def uiAfisareCarduri(self):
        carduri = self.cardClientService.getAll()
        for card in carduri:
            print(card)

    def runCrudRezervari(self):
        while True:
            print("1. Adaugare rezervare")
            print("2. Stergere rezervare")
            print("3. Modificare rezervare")
            print("u. Undo")
            print("r. Redo")
            print("a. Afisarea rezervarilor")
            print("x. Inapoi in meniu")
            optiune = input("Selectati optiunea: ")
            if optiune == '1':
                self.uiAdaugareRezervare()
            elif optiune == '2':
                self.uiStergereRezervare()
            elif optiune == '3':
                self.uiModificareRezervare()
            elif optiune == 'a':
                self.uiAfisareRezervari()
            elif optiune == 'u':
                self.undo_redo_service.do_undo()
            elif optiune == 'r':
                self.undo_redo_service.do_redo()
            elif optiune == 'x':
                break
            else:
                print("Optiune invalida!")

    def uiAdaugareRezervare(self):
        try:
            idRezervare = input("Dati id-ul rezervarii: ")
            while idRezervare.isdigit() == False or idRezervare[0] == '0':
                print("Id incorect! Reincercati!")
                idRezervare = input("Dati id-ul: ")
            idFilm = input("Dati id-ul filmului: ")
            while idFilm.isdigit() == False or idFilm[0] == '0':
                print("Id incorect! Reincercati!")
                idFilm = input("Dati id-ul: ")
            idCard = input("Dati id-ul cardului: ")
            while idCard.isdigit() == False or (idCard[0] == '0' and len(idCard) > 1):
                print("Id incorect! Reincercati!")
                idCard = input("Dati id-ul: ")
            dataRezervare = input("Dati data rezervarii(dd.mm.yyyy): ")
            try:
                dataRezervare = datetime.strptime(dataRezervare, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Formatul datei rezervarii nu este cel corespunzator (dd.mm.yy)!")
            oraRezervare = input("Dati ora rezervarii(HH:MM): ")
            try:
                datetime.strptime(oraRezervare, "%H:%M")
                ora = int(str(oraRezervare)[:2])
                minute = int(str(oraRezervare)[3:5])
                oraRezervare = time(ora, minute)
            except ValueError as ve:
                raise ValueError("Formatul orei nu este cel corespunzator (HH:MM)!")

            self.rezervareService.adaugare(idRezervare, idFilm, idCard, dataRezervare, oraRezervare)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def uiStergereRezervare(self):
        try:
            idStergere = input("Dati id-ul rezervarii de sters: ")
            while idStergere.isdigit() == False or idStergere[0] == '0':
                print("Id incorect! Reincercati!")
                idStergere = input("Dati id-ul: ")

            self.rezervareService.stergere(idStergere)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def uiModificareRezervare(self):
        try:
            idRezervare = input("Dati id-ul rezervarii: ")
            while idRezervare.isdigit() == False or idRezervare[0] == '0':
                print("Id incorect! Reincercati!")
                idRezervare = input("Dati id-ul: ")
            idFilm = input("Dati id-ul filmului: ")
            while idFilm.isdigit() == False or (idFilm[0] == '0' and len(idFilm) > 1):
                print("Id incorect! Reincercati!")
                idFilm = input("Dati id-ul: ")
            idCard = input("Dati id-ul cardului(sau 00 pentru a nu modifica): ")
            while idCard.isdigit() == False or (idCard[0] == '0' and len(idCard) > 2):
                print("Id incorect! Reincercati!")
                idCard = input("Dati id-ul: ")

            dataRezervare = input("Dati data rezervarii(dd.mm.yyyy): ")
            if dataRezervare != "":
                try:
                    dataRezervare = datetime.strptime(dataRezervare, "%d.%m.%Y")
                except ValueError:
                    raise ValueError("Formatul datei rezervarii nu este cel corespunzator (dd.mm.yy)!")

            oraRezervare = input("Dati ora rezervarii(HH:MM): ")
            if oraRezervare != "":
                try:
                    datetime.strptime(oraRezervare, "%H:%M")
                    ora = int(str(oraRezervare)[:2])
                    minute = int(str(oraRezervare)[3:5])
                    oraRezervare = time(ora, minute)
                except ValueError as ve:
                    raise ValueError("Formatul orei nu este cel corespunzator (HH:MM)!")

            self.rezervareService.modificare(idRezervare, idFilm, idCard, dataRezervare, oraRezervare)

        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)

    def uiAfisareRezervari(self):
        rezervari = self.rezervareService.getAll()
        # ora1 = rezervari[0].oraRezervare
        # ora2 = rezervari[1].oraRezervare
        # duration = datetime.combine(date.min, ora2) - datetime.combine(date.min, ora1)
        # print(duration)
        for rezervare in rezervari:
            ora = rezervare.oraRezervare.strftime("%H:%M")
            data = rezervare.dataRezervare.strftime("%d.%m.%Y")
            print(f"id rezervare: {rezervare.idRezervare} \nfilm: {rezervare.film} \ncard: {rezervare.card}\ndata rezervare: {data} \nora rezervare: {ora}\n")
        for rezervare in rezervari:
            print(rezervare)
