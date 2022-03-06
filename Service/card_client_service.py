from Domain.add_operation import ModifOperation, DelOperation, AddOperation, Incrementare
from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from copy import copy
from datetime import datetime

from Repository.file_repository import FileRepository
from Service.undo_redo_service import UndoRedoService


class CardClientService:
    def __init__(self, cardRepository : FileRepository, cardValidator : CardClientValidator,  undo_redo_service: UndoRedoService):
        self.__cardRepository = cardRepository
        self.__cardValidator = cardValidator
        self.__undo_redo_service = undo_redo_service

    def getCard(self, idCard):
        return self.__cardRepository.getById(idCard)

    def incrementareCarduriZiDeNastereService(self, valoare, data1, data2):
        '''
        Incrementeaza cu o valoare valoare punctule acumuluate de pe cardurile a caror
        proprietari sunt nascuti intre doua date date
        :param valoare: valoare de incrementat
        :param data1: o data de tip dd.mm.yyyy
        :param data2: o data de tip dd.mm.yyyy
        :return:
        '''
        listaCarduri = self.getAll()
        listToReturn = []
        listOfModif = []
        for card in listaCarduri:
            data = card.dataNastere
            delta0 = data - data
            delta1 = data - data1
            delta2 = data2 - data
            if delta1 >= delta0 and delta2 >= delta0:
                listToReturn.append(f"A fost modificat cardul cu id: {card.idEntitate}")
                ccard = copy(card)
                self.__cardRepository.modificare(CardClient(card.idEntitate, card.numeCard, card.prenumeCard, card.CNP, card.dataNastere, card.dataInregistrare, card.puncteAcumulate + valoare))
                listOfModif.append([ccard, self.__cardRepository.getById(card.idEntitate)])

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(Incrementare(self.__cardRepository, listOfModif))
        return listToReturn

    def cautareFullText(self, string, stringList):
        listaCarduri = self.__cardRepository.getAll()
        for card in listaCarduri:

            findFunction = lambda stringToFind, string: string.find(stringToFind)
            if findFunction(string,card.idEntitate) != -1:
                stringList.append(f"id card : {card.idEntitate}")
            if findFunction(string,card.numeCard) != -1:
                stringList.append(f"nume card: {card.numeCard}")
            if findFunction(string,card.prenumeCard) != -1:
                stringList.append(f"prenume card: {card.prenumeCard}")
            if findFunction(string,card.CNP) != -1:
                stringList.append(f"CNP: {card.CNP}")
            data = card.dataNastere.strftime("%d.%m.%Y")
            if findFunction(string,data) != -1:
                stringList.append(f"data nastere: {data}")
            data = card.dataInregistrare.strftime("%d.%m.%Y")
            if findFunction(string,data) != -1:
                stringList.append(f"data inregistrare: {data}")
            if findFunction(string,str(card.puncteAcumulate)) != -1:
                stringList.append(f"puncte acumulate: {card.puncteAcumulate}")


            # if card.idEntitate.find(string) != -1:
            #     stringList.append(f"id card : {card.idEntitate}")
            # if card.numeCard.find(string) != -1:
            #     stringList.append(f"nume card: {card.numeCard}")
            # if card.prenumeCard.find(string) != -1:
            #     stringList.append(f"prenume card: {card.prenumeCard}")
            # if card.CNP.find(string) != -1:
            #     stringList.append(f"CNP: {card.CNP}")
            # data = card.dataNastere.strftime("%d.%m.%Y")
            # if data.find(string) != -1:
            #     stringList.append(f"data nastere: {data}")
            # data = card.dataInregistrare.strftime("%d.%m.%Y")
            # if data.find(string) != -1:
            #     stringList.append(f"data inregistrare: {data}")
            # if str(card.puncteAcumulate).find(string) != -1:
            #     stringList.append(f"puncte acumulate: {card.puncteAcumulate}")
        return stringList

    def ordonareDescrescatorPuncte(self):
        lista = sorted(self.__cardRepository.getAll(), key = lambda card: card.puncteAcumulate, reverse = True)
        return lista

    def getAll(self):
        return self.__cardRepository.getAll()

    def adaugare(self, idCard, nume, prenume, CNP, dataNastere, dataInregistrare, puncteAcumulate):
        '''
        Adauga un card
        :param idCard: id-ul cardului
        :param nume: numele persoanei
        :param prenume: prenumele persoanei
        :param CNP: cnp ul persoanei
        :param dataNastere: data nasterii persoanei
        :param dataInregistrare: data inregistrarii
        :param puncteAcumulate: punctele acumulate pe card
        :return:
        '''
        card = CardClient(idCard, nume, prenume, CNP, dataNastere, dataInregistrare, puncteAcumulate)

        if self.__cardRepository.getById(idCard):
            raise KeyError(f"Exista deja un card cu id-ul {idCard}")

        carduri = self.__cardRepository.getAll()
        for aCard in carduri:
            if aCard.CNP == card.CNP:
                raise KeyError("CNP-ul nu este unic!")

        self.__cardValidator.valideaza(card, self.__cardRepository)
        self.__cardRepository.adaugare(card)

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(AddOperation(self.__cardRepository, card))

    def stergere(self, idCard):
        '''
        Stergerea unui card din lista de carduri
        :param idCard: id-ul carduri de sters
        :return:
        '''

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(DelOperation(self.__cardRepository, self.__cardRepository.getById(idCard)))
        self.__cardRepository.stergere(idCard)

    def modificare(self, idCard, nume, prenume, CNP, dataNastere, dataInregistrare, puncteAcumulate):
        card = self.__cardRepository.getById(idCard)
        ccard = copy(card)
        if card is None:
            raise KeyError(f'ID-ul {idCard} nu exista!')
        if nume != "":
            card.numeCard = nume
        if prenume != "":
            card.prenumeCard = prenume
        if CNP != "":
            card.CNP = CNP
        if dataNastere != "":
            card.dataNastere = dataNastere
        if dataInregistrare != "":
            card.dataInregistrare = dataInregistrare
        if puncteAcumulate != 0:
            card.puncteAcumulate = puncteAcumulate

        carduri = self.__cardRepository.getAll()
        if CNP != "":
            for aCard in carduri:
                if aCard.CNP == card.CNP and aCard.idCard != card.idCard:
                    raise KeyError("CNP-ul nu este unic!")
        self.__cardValidator.valideaza(card, self.__cardRepository)

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(ModifOperation(self.__cardRepository, ccard, card))
        self.__cardRepository.modificare(card)



