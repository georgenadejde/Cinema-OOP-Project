class Entitate:
    def __init__(self, idEntitate):
        self.__idEntitate = idEntitate

    def __eq__(self, other):
        return type(self) == type(other) and self.__idEntitate == other.__idEntitate

    @property
    def idEntitate(self):
        return self.__idEntitate
