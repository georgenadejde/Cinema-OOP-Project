from Domain.film_validator import FilmValidator
from Domain.card_client_validator import CardClientValidator
from Domain.rezervare_validator import RezervareValidator
from Repository.file_repository import FileRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Tests.run_all import runAllTests
from UserInterface.console import Console


def main():
    undo_redo_service = UndoRedoService()

    filmValidator = FilmValidator()
    cardValidator = CardClientValidator()
    rezervareValidator = RezervareValidator()

    filmRepository = FileRepository("filme.txt")               #FilmRepository()
    cardRepository = FileRepository("carduri.txt")                #CardClientRepository()
    rezervareRepository = FileRepository("rezervari.txt")           #RezervareRepository()

    filmService = FilmService(filmRepository, filmValidator, undo_redo_service)
    cardService = CardClientService(cardRepository, cardValidator, undo_redo_service)
    rezervareService = RezervareService(rezervareRepository, filmRepository, cardRepository, rezervareValidator, undo_redo_service)

    ui = Console(filmService, cardService, rezervareService, undo_redo_service)
    ui.runMenu()

runAllTests()
main()
