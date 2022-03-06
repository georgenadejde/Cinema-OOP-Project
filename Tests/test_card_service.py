from Domain.card_client_validator import CardClientValidator
from Repository.file_repository import FileRepository
from Service.card_client_service import CardClientService
from Tests.utils import clear_file
from datetime import datetime

def testAdaugareCard():
    clear_file("cardTest.txt")
    cardRepository = FileRepository("cardTest.txt")
    cardValidator = CardClientValidator()
    service = CardClientService(cardRepository, cardValidator)
    dataN = datetime.strptime("11.12.2000", "%d.%m.%Y")
    dataI = datetime.strptime("11.12.2010", "%d.%m.%Y")
    service.adaugare('1', "abc", "cfg", 12, dataN, dataI, 10)
    assert len(service.getAll()) == 1
    added = cardRepository.getById('1')
    assert added is not None
    assert added.idCard == '1'
    assert added.numeCard == 'abc'
    assert added.prenumeCard == "cfg"
    assert added.CNP == 12
    assert added.dataNastere == dataN
    assert added.dataInregistrare == dataI
    assert added.puncteAcumulate == 10

    try:
        service.adaugare('1', "abc", "cfg", 12, dataN, dataI, 10)
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

def testStergereCard():
    clear_file("cardTest.txt")
    cardRepository = FileRepository("cardTest.txt")
    cardValidator = CardClientValidator()
    service = CardClientService(cardRepository, cardValidator)
    dataN = datetime.strptime("11.12.2000", "%d.%m.%Y")
    dataI = datetime.strptime("11.12.2010", "%d.%m.%Y")
    service.adaugare('1', "abc", "cfg", 12, dataN, dataI, 10)
    service.adaugare('2', "abcd", "cfgh", 13, dataN, dataI, 10)

    try:
        service.stergere('3')
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

def testModificareCard():
    clear_file("cardTest.txt")
    cardRepository = FileRepository("cardTest.txt")
    cardValidator = CardClientValidator()
    service = CardClientService(cardRepository, cardValidator)
    dataN = datetime.strptime("11.12.2000", "%d.%m.%Y")
    dataI = datetime.strptime("11.12.2010", "%d.%m.%Y")
    service.adaugare('1', "abc", "cfg", 12, dataN, dataI, 10)
    service.modificare('1', "abcd", "cfgh", 12, dataN, dataI, 10)
    updated = cardRepository.getById('1')
    assert updated is not None
    assert updated.idCard == '1'
    assert updated.numeCard == 'abcd'
    assert updated.prenumeCard == "cfgh"
    assert updated.CNP == 12
    assert updated.dataNastere == dataN
    assert updated.dataInregistrare == dataI
    assert updated.puncteAcumulate == 10


