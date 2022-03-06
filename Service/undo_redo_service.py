from Domain.undo_redo_operation import UndoRedoOperation


class UndoRedoService:
    def __init__(self):
        self.__undo_stack = []
        self.__redo_stack = []

    def redoClear(self):
        self.__redo_stack.clear()

    def add_to_undo(self, operation: UndoRedoOperation):
        self.__undo_stack.append(operation)

    def do_undo(self):
        if len(self.__undo_stack) > 0:
            self.__redo_stack.append(self.__undo_stack[-1])
            self.__undo_stack.pop().undo()

    def do_redo(self):
        if len(self.__redo_stack) > 0:
            self.add_to_undo(self.__redo_stack[-1])
            self.__redo_stack.pop().redo()
