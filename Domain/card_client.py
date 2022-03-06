from datetime import datetime

from Domain.entitate import Entitate


class CardClient(Entitate):
    '''
    creeaza entitatea card client
    '''
    def __init__(self, idCard, nume, prenume, CNP, dataNastere : datetime, dataInregistrare, puncteAcumulate):
        super().__init__(idCard)
        self.__numeCard = nume
        self.__prenumeCard = prenume
        self.__CNP = CNP
        self.__dataNastere = dataNastere
        self.__dataInregistrare = dataInregistrare
        self.__puncteAcumulate = puncteAcumulate

    def __str__(self):

        return f"id card: {self.idEntitate}, nume card: {self.__numeCard}, prenume card: {self.__prenumeCard}, " \
               f"CNP: {self.__CNP}, data nasterii: {str(self.__dataNastere)[8:10]}.{str(self.__dataNastere)[5:7]}.{str(self.__dataNastere)[0:4]}, data inregistrarii: {str(self.__dataInregistrare)[8:10]}.{str(self.__dataInregistrare)[5:7]}.{str(self.__dataInregistrare)[0:4]}, " \
               f"puncte acumulate: {self.__puncteAcumulate}"

    @property
    def idCard(self):
        return self.idEntitate

    @property
    def numeCard(self):
        return self.__numeCard

    @numeCard.setter
    def numeCard(self, numeCardNou):
        self.__numeCard = numeCardNou

    @property
    def prenumeCard(self):
        return self.__prenumeCard

    @prenumeCard.setter
    def prenumeCard(self, prenumeCardNou):
        self.__prenumeCard = prenumeCardNou

    @property
    def CNP(self):
        return self.__CNP

    @CNP.setter
    def CNP(self, CNPNou):
        self.__CNP = CNPNou

    @property
    def dataNastere(self):
        return self.__dataNastere

    @dataNastere.setter
    def dataNastere(self, dataNastereNou):
        self.__dataNastere = dataNastereNou

    @property
    def dataInregistrare(self):
        return self.__dataInregistrare

    @dataInregistrare.setter
    def dataInregistrare(self, dataInregistrareNou):
        self.__dataInregistrare = dataInregistrareNou

    @property
    def puncteAcumulate(self):
        return self.__puncteAcumulate

    @puncteAcumulate.setter
    def puncteAcumulate(self, puncteAcumulateNou):
        self.__puncteAcumulate = puncteAcumulateNou
