from Domain.card_client import CardClient
from copy import copy
from datetime import datetime

from Repository.file_repository import FileRepository


class CardClientValidator:
    def valideaza(self, card: CardClient, cardRepository: FileRepository):
        erori = []
        carduri = cardRepository.getAll()

        try:
            validDataNastere = copy(card.dataNastere)
            validDataNastere = validDataNastere.strftime("%d") + "." + validDataNastere.strftime("%m") + "." +validDataNastere.strftime("%Y")
            datetime.strptime(validDataNastere, "%d.%m.%Y")
        except ValueError as ve:
            erori.append("Formatul datei de nastere nu este cel corespunzator (dd.mm.yy)!")

        try:
            validDataInregistrare = copy(card.dataInregistrare)
            validDataInregistrare = validDataInregistrare.strftime("%d") + "." + validDataInregistrare.strftime("%m") + "." +validDataInregistrare.strftime("%Y")
            datetime.strptime(validDataInregistrare, "%d.%m.%Y")
        except ValueError as ve:
            erori.append("Formatul datei de inregistrare nu este cel corespunzator (dd.mm.yy)!")

        if len(erori) >0:
            for eroare in erori:
                print(eroare)
            raise ValueError()

