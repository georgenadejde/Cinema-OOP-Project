from Domain.entitate import Entitate


class Film(Entitate):
    '''
    creeaza entitatea film
    '''
    def __init__(self, id_film, titlu_film, an_aparitie, pret_film, in_program):
        super().__init__(id_film)
        self.__titluFilm = titlu_film
        self.__anAparitie = an_aparitie
        self.__pretFilm = pret_film
        self.__inProgram = in_program

    def __str__(self):
        return f"id film: {self.idEntitate}, titlu film: {self.__titluFilm}, an aparitie: {self.__anAparitie}, " \
               f"pret bilet: {self.__pretFilm}, in program: {self.__inProgram}"

    @property
    def idFilm(self):
        return self.idEntitate

    @property
    def titluFilm(self):
        return self.__titluFilm

    @titluFilm.setter
    def titluFilm(self, titluNou):
        self.__titluFilm = titluNou

    @property
    def anAparitie(self):
        return self.__anAparitie

    @anAparitie.setter
    def anAparitie(self, anNou):
        self.__anAparitie = anNou

    @property
    def pretFilm(self):
        return self.__pretFilm

    @pretFilm.setter
    def pretFilm(self, pretNou):
        self.__pretFilm = pretNou

    @property
    def inProgram(self):
        return self.__inProgram

    @inProgram.setter
    def inProgram(self, inProgramNou):
        self.__inProgram = inProgramNou