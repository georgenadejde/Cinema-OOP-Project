from Domain.undo_redo_operation import UndoRedoOperation
from Repository.file_repository import FileRepository


class AddOperation(UndoRedoOperation):
    def __init__(self, repository: FileRepository, added_object):
        super().__init__(repository)
        self.__added_object = added_object

    def undo(self):
        self._repository.stergere(self.__added_object.idEntitate)

    def redo(self):
        self._repository.adaugare(self.__added_object)

class DelOperation(UndoRedoOperation):
    def __init__(self, repository: FileRepository, del_object):
        super().__init__(repository)
        self.__del_object = del_object

    def undo(self):
        self._repository.adaugare(self.__del_object)

    def redo(self):
        self._repository.stergere(self.__del_object.idEntitate)

class ModifOperation(UndoRedoOperation):
    def __init__(self, repository: FileRepository, unmodif_object, modif_object):
        super().__init__(repository)
        self.__unmodif_object = unmodif_object
        self.__modif_object = modif_object

    def undo(self):
        self._repository.stergere(self.__unmodif_object.idEntitate)
        self._repository.adaugare(self.__unmodif_object)

    def redo(self):
        self._repository.stergere(self.__unmodif_object.idEntitate)
        self._repository.adaugare(self.__modif_object)

class RezDelInInterval(UndoRedoOperation):
    def __init__(self, repository: FileRepository, listOfRezToDel):
        super().__init__(repository)
        self.__listOfRezToDel = listOfRezToDel

    def undo(self):
        for rez in self.__listOfRezToDel:
            self._repository.adaugare(rez)

    def redo(self):
        for rez in self.__listOfRezToDel:
            self._repository.stergere(rez.idEntitate)

class Incrementare(UndoRedoOperation):
    def __init__(self, repository: FileRepository, listOfModAndUnmodCards):
        super().__init__(repository)
        self.__listOfModAndUnmodCards = listOfModAndUnmodCards

    def undo(self):
        for card in self.__listOfModAndUnmodCards:
            self._repository.stergere(card[0].idEntitate)
            self._repository.adaugare(card[0])

    def redo(self):
        for card in self.__listOfModAndUnmodCards:
            self._repository.stergere(card[1].idEntitate)
            self._repository.adaugare(card[1])