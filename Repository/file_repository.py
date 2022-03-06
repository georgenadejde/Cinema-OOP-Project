from copy import deepcopy

import jsonpickle as jsonpickle

from Domain.entitate import Entitate


class FileRepository:
    def __init__(self, fileName):
        self.__fileName = fileName
        self.__storage = {}  # dictionar avand drept chei id-urile entitatilor si drept valori entitatile in sine

    def __readFile(self):
        try:
            with open(self.__fileName, "r") as fp:
                self.__storage = jsonpickle.decode(fp.read())
        except:
            self.__storage = {}

    def __writeFile(self):
        with open(self.__fileName, "w") as fp:
            fp.write(jsonpickle.encode(self.__storage))

    def getById(self, idEntitate):
        self.__readFile()
        if idEntitate in self.__storage:
            return deepcopy(self.__storage[idEntitate])
        return None

    def getAll(self):
        self.__readFile()
        return deepcopy(list(self.__storage.values()))

    def adaugare(self, entitate: Entitate):
        '''

        :param id_masina:
        :param indicativ:
        :param nivel_confort:
        :param plata_card:
        :param model:
        :return:
        '''

        self.__storage[entitate.idEntitate] = entitate
        self.__writeFile()

    def stergere(self, idSters):
        '''

        :param id_de_sters:
        :return:
        '''
        if self.getById(idSters) is None:
            raise KeyError(f'ID-ul {idSters} nu exista!')
        del self.__storage[idSters]
        self.__writeFile()

    def modificare(self, entitate: Entitate):
        if self.getById(entitate.idEntitate) is None:
            raise KeyError(f'ID-ul {entitate.idEntitate} nu exista!')
        self.__storage[entitate.idEntitate] = entitate
        self.__writeFile()
