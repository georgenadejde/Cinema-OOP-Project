from copy import copy

from Domain.add_operation import AddOperation, DelOperation, ModifOperation
from Domain.film import Film
from Domain.film_validator import FilmValidator
import random, string

from Repository.export_excel import ExportExcel
from Repository.file_repository import FileRepository
from Service.undo_redo_service import UndoRedoService


class FilmService:
    def __init__(self, filmRepository : FileRepository, filmValidator : FilmValidator, undo_redo_service: UndoRedoService):
        self.__filmRepository = filmRepository
        self.__filmValidator = filmValidator
        self.__undo_redo_service = undo_redo_service

    def getFilm(self, idFilm):
        return self.__filmRepository.getById(idFilm)

    def exportService(self):
        export = ExportExcel(self.__filmRepository)
        export.exportExcel()

    def cautareFullText(self, string, stringList):
        '''
        Cauta dupa un string dat in caracteristicile filmelor
        :param string: string ul dupa care se cauta
        :param stringList: lista in care se retin parametrii in care se gaseste stringul
        :return: stringList
        '''
        listaFilme = self.__filmRepository.getAll()
        for film in listaFilme:
            findFunction = lambda stringToFind, string: string.find(stringToFind)

            if findFunction(string,film.idEntitate) != -1:
                stringList.append(f"id film : {film.idEntitate}")
            if findFunction(string,film.titluFilm) != -1:
                stringList.append(f"titlu film: {film.titluFilm}")
            if findFunction(string,str(film.anAparitie)) != -1:
                stringList.append(f"an aparitie film: {film.anAparitie}")
            if findFunction(string,str(film.pretFilm)) != -1:
                stringList.append(f"pret film: {film.pretFilm}")
            if findFunction(string,film.inProgram) != -1:
                stringList.append(f"in program: {film.inProgram}")
        return stringList


    def getRandomString(self):
        # Random string with the combination of lower and upper case
        # letters = string.ascii_letters
        # result_str = ''.join(random.choice(letters) for i in range(length))
        # print("Random string is:", result_str)
        '''
        Genereaza un string random de lungime intre 1 si 10 caractere
        :return:
        '''
        return ''.join(random.choice(string.ascii_letters) for _ in range(random.choice(range(1, 10))))

    def getRandomNumber(self, l, r):
        '''
        genereaza un numar random intre l si r
        :param l: un numar l
        :param r: un numar r
        :return: un numar random inre l si r
        '''
        return random.randint(l, r)

    def generateFilm(self, n):
        '''
        Genereaza n filme
        :param n: numarul de filme de generat
        :return:
        '''
        for i in range (n):
            idFilm = self.getRandomNumber(1,1000)
            while self.__filmRepository.getById(idFilm) != None:
                idFilm = self.getRandomNumber(1, 1000)
            titluFilm = self.getRandomString()
            anAparitie = self.getRandomNumber(1900, 2020)
            pretFilm = self.getRandomNumber(1,30)
            inProgram = self.getRandomNumber(1,2)
            if inProgram == 1:
                inProgram = "da"
            else:
                inProgram = "nu"
            self.adaugare(str(idFilm), titluFilm, anAparitie, pretFilm, inProgram)

    def getAll(self):
        '''
        Preia filmele din repository
        :return:
        '''
        return self.__filmRepository.getAll()

    def adaugare(self, idFilm, titluFilm, anAparitie, pretFilm, inProgram):
        '''
        Adauga un film
        :param idFilm: id-ul filmului de adaugat
        :param titluFilm: titlul filmului de adaugat
        :param anAparitie: anul aparitiei filmului de adaugat
        :param pretFilm: pretul filmului de adaugat
        :param inProgram: daca filmul este sau nu in program
        :return:
        '''
        film = Film(idFilm, titluFilm, anAparitie, pretFilm, inProgram)

        if self.__filmRepository.getById(idFilm):
            raise KeyError(f"Exista deja un film cu id-ul {idFilm}")

        self.__filmValidator.valideaza(film)
        self.__filmRepository.adaugare(film)

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(AddOperation(self.__filmRepository, film))

    def stergere(self, idFilm):
        '''
        Stergerea unui film din lista de filme
        :param idFilm: id-ul filmului de sters
        :return:
        '''
        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(DelOperation(self.__filmRepository, self.__filmRepository.getById(idFilm)))
        self.__filmRepository.stergere(idFilm)

    def modificare(self, idFilm, titluFilm, anAparitie, pretFilm, inProgram):
        '''
        Modifica un film
        :param idFilm: id-ul filmului de adaugat
        :param titluFilm: titlul filmului de adaugat
        :param anAparitie: anul aparitiei filmului de adaugat
        :param pretFilm: pretul filmului de adaugat
        :param inProgram: daca filmul este sau nu in program
        :return:
        '''
        film = self.__filmRepository.getById(idFilm)
        cfilm = copy(film)
        if film is None:
            raise KeyError(f'ID-ul {idFilm} nu exista!')
        if titluFilm != "":
            film.titluFilm = titluFilm
        if anAparitie != 0:
            film.anAparitie = anAparitie
        if pretFilm != 0:
            film.pretFilm = pretFilm
        if inProgram != "":
            film.inProgram = inProgram
        self.__filmValidator.valideaza(film)

        self.__undo_redo_service.redoClear()
        self.__undo_redo_service.add_to_undo(ModifOperation(self.__filmRepository, cfilm, film))
        self.__filmRepository.modificare(film)

