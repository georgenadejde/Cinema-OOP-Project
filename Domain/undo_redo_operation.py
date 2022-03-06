from Repository.file_repository import FileRepository


class UndoRedoOperation:
    def __init__(self, repository: FileRepository):
        self._repository = repository

    def undo(self):
        raise NotImplemented('Trebuie folosita o clasa derivata!')

    def redo(self):
        raise NotImplemented('Trebuie folosita o clasa derivata!')