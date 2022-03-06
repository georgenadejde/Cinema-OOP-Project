import pandas as pd
from Repository.file_repository import FileRepository
from openpyxl.workbook import Workbook

class ExportExcel():
    def __init__(self, filmRepository: FileRepository):
        self.__filmRepository = filmRepository

    def exportExcel(self):
        filme = self.__filmRepository.getAll()
        filmeBun = {}

        sir = []
        for film in filme:
            sir.append(film.idEntitate)
        filmeBun['id film'] = sir

        sir = []
        for film in filme:
            sir.append(film.titluFilm)
        filmeBun['Titlu'] = sir

        sir = []
        for film in filme:
            sir.append(film.anAparitie)
        filmeBun['An aparitie'] = sir

        sir = []
        for film in filme:
            sir.append(film.pretFilm)
        filmeBun['Pret bilet'] = sir

        sir = []
        for film in filme:
            sir.append(film.inProgram)
        filmeBun['In program'] = sir

        df = pd.DataFrame(filmeBun, columns=['id film', 'Titlu', 'An aparitie', 'Pret bilet', 'In program'])
        df.to_excel(r'C:\Users\SirBunger\Desktop\Python\ProiectLab8-9\ExportDateExcel.xlsx', index=False, header=True)

        # fileName= 'ExportDateExcel.xlsx'
        # df.to_excel(fileName)