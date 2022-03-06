from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare_validator import RezervareValidator
from Repository.file_repository import FileRepository
from Tests.utils import clear_file
from Service.rezervare_service import RezervareService
from datetime import datetime

def testAdaugareRezervare():
    clear_file("rezervareTest.txt")
    rezervareRepository = FileRepository("rezervareTest.txt")

    clear_file("filmTest.txt")
    filmRepository = FileRepository("filmTest.txt")

    clear_file("cardTest.txt")
    cardRepository = FileRepository("cardTest.txt")

    validator = RezervareValidator()
    service = RezervareService(rezervareRepository, filmRepository, cardRepository, validator)

    film = Film('1', "abc", 2000, 12, "da")
    dataN = datetime.strptime("11.12.2000", "%d.%m.%Y")
    dataI = datetime.strptime("11.12.2010", "%d.%m.%Y")
    card = CardClient('1', "abc", "cfg", 12, dataN, dataI, 10)
    filmRepository.adaugare(film)
    cardRepository.adaugare(card)

    service.adaugare('1', '1', '1', "11.12.2000", "19:11")
    assert len(rezervareRepository.getAll()) == 1
    added = rezervareRepository.getById('1')
    assert added.idRezervare == '1'
    assert added.film == film
    assert added.card == card
    assert added.dataRezervare == "11.12.2000"
    assert added.oraRezervare == "19:11"

    try:
        # film = Film('1', "abc", 2000, 12, "da")
        # card = CardClient('1', "abc", "cfg", 12, "11.12.2000", "11.12.2010", 10)

        service.adaugare('1', '1', '1', "11.12.2000", "19:11")
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

    try:
        # film = Film('1', "abc", 2000, 12, "da")
        # card = CardClient('3', "abc", "cfg", 12, "11.12.2000", "11.12.2010", 10)
        service.adaugare('2', '1', '3', "11.12.2000", "19:11")
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

    try:
        # film = Film('3', "abc", 2000, 12, "da")
        # card = CardClient('1', "abc", "cfg", 12, "11.12.2000", "11.12.2010", 10)
        service.adaugare('2', '3', '1', "11.12.2000", "19:11")
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

def testStergereRezervare():
    clear_file("rezervareTest.txt")
    rezervareRepository = FileRepository("rezervareTest.txt")

    clear_file("filmTest.txt")
    filmRepository = FileRepository("filmTest.txt")

    clear_file("cardTest.txt")
    cardRepository = FileRepository("cardTest.txt")

    validator = RezervareValidator()
    service = RezervareService(rezervareRepository, filmRepository, cardRepository, validator)

    film = Film('1', "abc", 2000, 12, "da")
    dataN = datetime.strptime("11.12.2000", "%d.%m.%Y")
    dataI = datetime.strptime("11.12.2010", "%d.%m.%Y")
    card = CardClient('1', "abc", "cfg", 12, dataN, dataI, 10)
    filmRepository.adaugare(film)
    cardRepository.adaugare(card)
    service.adaugare('1', '1', '1', "11.12.2000", "19:11")

    try:
        service.stergere('2')
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

    service.stergere('1')
    assert len(service.getAll()) == 0

def testModificareRezervare():
    clear_file("rezervareTest.txt")
    rezervareRepository = FileRepository("rezervareTest.txt")

    clear_file("filmTest.txt")
    filmRepository = FileRepository("filmTest.txt")

    clear_file("cardTest.txt")
    cardRepository = FileRepository("cardTest.txt")

    validator = RezervareValidator()
    service = RezervareService(rezervareRepository, filmRepository, cardRepository, validator)

    film = Film('1', "abc", 2000, 12, "da")
    dataN = datetime.strptime("11.12.2000", "%d.%m.%Y")
    dataI = datetime.strptime("11.12.2010", "%d.%m.%Y")
    card = CardClient('1', "abc", "cfg", 12, dataN, dataI, 10)
    filmRepository.adaugare(film)
    cardRepository.adaugare(card)
    service.adaugare('1', film.idFilm, card.idCard, "11.12.2000", "19:11")

    service.modificare('1', '0', '00', "", "")
    updated =rezervareRepository.getById('1')

    assert updated.idRezervare == '1'
    assert updated.film == film
    assert updated.card == card
    assert updated.dataRezervare == "11.12.2000"
    assert updated.oraRezervare == "19:11"