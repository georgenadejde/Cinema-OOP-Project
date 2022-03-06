from copy import copy

from Domain.add_operation import ModifOperation, DelOperation, AddOperation, RezDelInInterval
from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Repository.file_repository import FileRepository
from datetime import datetime, time, date

from Service.undo_redo_service import UndoRedoService


class RezervareService:
    def __init__(self, rezervareRepository : FileRepository, filmRepository : FileRepository, cardRepository : FileRepository, rezervareValidator : RezervareValidator,
                 undo_redo_service: UndoRedoService):
        self.__rezervareRepository = rezervareRepository
        self.__filmRepository = filmRepository
        self.__cardRepository = cardRepository
        self.__rezervareValidator = rezervareValidator
        self.__undo_redo_service = undo_redo_service

    def mergeSortAlg(self, iter, key=lambda x: x):
        if len(iter) > 1:
            mid = len(iter) // 2
            left = iter[:mid]
            right = iter[mid:]
            self.mergeSortAlg(left, key)
            self.mergeSortAlg(right, key)
            i = 0
            j = 0
            k = 0
            while i < len(left) and j < len(right):
                if key(left[i]) < key(right[j]):
                    iter[k] = left[i]
                    i = i + 1
                else:
                    iter[k] = right[j]
                    j = j + 1
                k = k + 1

            while i < len(left):
                iter[k] = left[i]
                i = i + 1
                k = k + 1

            while j < len(right):
                iter[k] = right[j]
                j = j + 1
                k = k + 1

    def mergeSort(self, iter, key=lambda x: x, reverse=False):
        self.mergeSortAlg(iter, key)
        if reverse is False:
            return iter
        else:
            return iter[::-1]

    def mySortedFunction(self, iter, key=lambda x: x, reverse=False):
        for i in range(len(iter) - 1):
            for j in range(len(iter) - i - 1):
                if key(iter[j]) > key(iter[j + 1]):
                    iter[j], iter[j + 1] = iter[j + 1], iter[j]
        if reverse is False:
            return iter
        else:
            return iter[::-1]

    def filmeOrdonateDescrDupaNrRezervariService(self):
        '''
        ordoneaza filmele dupa numarul de rezervari
        :return: un sir ordonat descrescator al filmelor in functie de numarul rezervarilor
        '''
        filme = self.__filmRepository.getAll()
        # return sorted(filme, key= self.numarRezervariFilm, reverse=True)
        # return self.mySortedFunction(filme, key= self.numarRezervariFilm, reverse=True)
        return self.mergeSort(filme, key= self.numarRezervariFilm, reverse=True)

    def stergereRezervareDinIntervalService(self, zi1, zi2):
        '''
        Sterge rezervarile create intre doua zile date
        :param zi1: o zi (1-31)
        :param zi2: o zi (1-31)
        :return: returneaza mesaje care confirma stergerea rezervarilor
        '''
        rezervari = self.getAll()
        listOfRez = []

        # for rezervare in rezervari:
        #     zi = int(rezervare.dataRezervare.strftime("%d"))
        #     if zi1 <= zi and zi <= zi2:
        #         listToReturn.append(f"A fost stearsa rezervarea cu id = {rezervare.idEntitate}")
        #         # self.stergere(rezervare.idEntitate)
        #         listToDelete.append(rezervare.idEntitate)
        #         listOfRez.append(rezervare)

        listToReturn = map(lambda rezervare: self.mapFunct(zi1, rezervare, zi2), rezervari)

        for rezervare in rezervari:
            zi = int(rezervare.dataRezervare.strftime("%d"))
            if zi1 <= zi and zi <= zi2:
                listOfRez.append(rezervare)
                self.__rezervareRepository.stergere(rezervare.idEntitate)

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(RezDelInInterval(self.__rezervareRepository, listOfRez))

        return list(listToReturn)

    def mapFunct(self, zi1, rezervare, zi2):
        zi = int(rezervare.dataRezervare.strftime("%d"))
        if zi1 <= zi and zi <= zi2:
            return f"A fost stearsa rezervarea cu id = {rezervare.idEntitate}"

    def numarRezervariCard(self, card: CardClient):
        '''
        Calculeaza numarul rezervarilor pentru un card dat
        :param card: un card dat
        :return: numarul rezervarilor pentru un card dat
        '''
        rezervari = self.getAll()
        numar = 0
        for rezervare in rezervari:
            if rezervare.card == card:
                numar = numar +1
        return numar

    def numarRezervariFilmRecursiv(self, film: Film, rezervari):
        if len(rezervari) > 0:
            if rezervari[0].film == film:
                return 1 + self.numarRezervariFilmRecursiv(film, rezervari[1:])
            else:
                return self.numarRezervariFilmRecursiv(film, rezervari[1:])
        return 0

    def numarRezervariFilm(self, film: Film):
        '''
        Calculeaza numarul rezervarilor pentru un film dat
        :param film: un film dat
        :return: numarul rezervarilor pentru un film dat
        '''
        rezervari = self.__rezervareRepository.getAll()
        numar = self.numarRezervariFilmRecursiv(film, rezervari)
        # for rezervare in rezervari:
        #     if rezervare.film == film:
        #         numar = numar +1
        return numar

    def filterFunction(self, ora1, rezervare, ora2):
        if (len(str(datetime.combine(date.min, rezervare.oraRezervare) - datetime.combine(date.min, ora1))) <= 8 and
            len(str(datetime.combine(date.min, ora2) - datetime.combine(date.min, rezervare.oraRezervare))) <= 8):
            return True
        else:
            return False

    def rezervariIntervalOreService(self, ora1, ora2):
        '''
        Determina rezervarile dntre doua ore date
        :param ora1: o ora de tip (HH:MM)
        :param ora2: o ora de tip (HH:MM)
        :return: o lista cu rezervarile create intre cele doua ore date
        '''
        listaRezervari = self.getAll()
        listaToReturn = []
        # for rezervare in listaRezervari:
            # oraRezervare = rezervare.oraRezervare
            # if len(str(datetime.combine(date.min, oraRezervare) - datetime.combine(date.min, ora1))) <= 8 and len(str(datetime.combine(date.min, ora2) - datetime.combine(date.min, oraRezervare))) <= 8:
            #     listaToReturn.append(rezervare)
        listaToReturn = filter(lambda rezervare: self.filterFunction(ora1, rezervare, ora2), listaRezervari)
        return listaToReturn

    def getAll(self):
        return self.__rezervareRepository.getAll()

    def adaugare(self, idRezervare, idFilm, idCard, data, ora):
        '''
        Adauga o rezervare
        :param idRezervare: id rezervare
        :param idFilm: id film
        :param idCard: id card
        :param data: data in care a fost creata rezervarea
        :param ora: ora la care a fost creata rezervarea
        :return:
        '''

        if self.__rezervareRepository.getById(idRezervare):
            raise KeyError(f"Exista deja o rezervare cu id-ul {idRezervare}")

        film = self.__filmRepository.getById(idFilm)
        if idCard != '0':
            card = self.__cardRepository.getById(idCard)
            if card is None:
                raise KeyError(f'ID-ul cardului {idCard} nu exista!')
        else:
            card = None
        rezervare = Rezervare(idRezervare, film, card, data, ora)
        self.__rezervareValidator.valideaza(rezervare)
        if card is not None:
            card.puncteAcumulate = card.puncteAcumulate + film.pretFilm // 10
        self.__rezervareRepository.adaugare(rezervare)

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(AddOperation(self.__rezervareRepository, rezervare))

    def stergere(self, idRezervare):
        '''
        Stergerea unei rezervari din lista de rezervari
        :param idRezervare: id-ul rezervarii de sters
        :return:
        '''
        # stergere puncte de acumulare??

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(DelOperation(self.__rezervareRepository, self.__rezervareRepository.getById(idRezervare)))
        self.__rezervareRepository.stergere(idRezervare)

    def modificare(self, idRezervare, idFilm, idCard, data, ora):
        '''
        modifica o rezervare
        :param idRezervare: id rezervare
        :param idFilm: id film
        :param idCard: id card
        :param data: data in care a fost creata rezervarea
        :param ora: ora la care a fost creata rezervarea
        :return:
        '''
        rezervare = self.__rezervareRepository.getById(idRezervare)
        crezervare = copy(rezervare)
        if rezervare is None:
            raise KeyError(f'ID-ul {idRezervare} nu exista!')
        if idCard != '00':
            if idCard == '0':
                card = None
                rezervare.card = card
            else:
                card = self.__cardRepository.getById(idCard)
                if card is None:
                    raise KeyError("Cardul cu id-ul dat nu exista!")
                rezervare.card = card

        # rezervare = Rezervare(idRezervare, film, card, data, ora)
        if idFilm != '0':
            film = self.__filmRepository.getById(idFilm)
            if film is not None:
                rezervare.film = film
            else:
                raise KeyError("Filmul cu id-ul dat nu exista!")


        if data != "":
            rezervare.dataRezervare = data
        if ora != "":
            rezervare.oraRezervare = ora

        self.__rezervareValidator.valideaza(rezervare)

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(ModifOperation(self.__rezervareRepository, crezervare, rezervare))
        self.__rezervareRepository.modificare(rezervare)

