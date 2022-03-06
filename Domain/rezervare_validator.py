from Domain.rezervare import Rezervare
from copy import copy
from datetime import datetime

class RezervareValidator:
    def valideaza(self, rezervare: Rezervare):
        erori = []

        if rezervare.film == None:
            erori.append("Filmul cu id-ul dat nu exista!")
        elif rezervare.film.inProgram == "nu":
            erori.append("Filmul cu id-ul dat nu este in program!")

        # if rezervare.card == None:
        #     erori.append("Cardul cu id-ul dat nu exista!")
        if len(erori) > 0:
            raise KeyError (erori)