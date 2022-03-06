from Domain.card_client import CardClient
from Domain.entitate import Entitate
from Domain.film import Film


class Rezervare(Entitate):
    '''
    creeaza entitatea rezervare
    '''
    def __init__(self, idRezervare, film: Film, card: CardClient, data, ora):
        super().__init__(idRezervare)
        self.__film = film
        self.__card = card
        self.__dataRezervare = data
        self.__oraRezervare = ora

    def __str__(self):
        if self.__card == None:
            return f"Rezervarea cu id: {self.idEntitate} nu are un card client"
        else:
            return f"Rezervarea cu id: {self.idEntitate} are {self.__card.puncteAcumulate} puncte acumulate pe cardul de client"

    @property
    def idRezervare(self):
        return self.idEntitate

    @property
    def film(self):
        return self.__film

    @film.setter
    def film(self, filmNou :Film):
        self.__film = filmNou

    @property
    def card(self):
        return self.__card

    @card.setter
    def card(self, cardNou:CardClient):
        self.__card = cardNou

    @property
    def dataRezervare(self):
        return self.__dataRezervare

    @dataRezervare.setter
    def dataRezervare(self, dataRezervareNou):
        self.__dataRezervare = dataRezervareNou

    @property
    def oraRezervare(self):
        return self.__oraRezervare

    @oraRezervare.setter
    def oraRezervare(self, oraRezervareNou):
        self.__oraRezervare = oraRezervareNou
