from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare
from datetime import datetime

def testFilm():
    film = Film('1',"abc",2000,12,"da")
    assert film.idFilm == '1'
    assert film.titluFilm == 'abc'
    assert film.anAparitie == 2000
    assert film.pretFilm == 12
    assert film.inProgram == 'da'

def testCard():
    dataN = datetime.strptime("11.12.2000", "%d.%m.%Y")
    dataI = datetime.strptime("11.12.2010", "%d.%m.%Y")
    card = CardClient('1', "abc", "cfg", 12, dataN, dataI, 10)
    assert card.idCard == '1'
    assert card.numeCard == 'abc'
    assert card.prenumeCard == "cfg"
    assert card.CNP == 12
    assert card.dataNastere == dataN
    assert card.dataInregistrare == dataI
    assert card.puncteAcumulate == 10

def testRezervare():
    dataN = datetime.strptime("11.12.2000", "%d.%m.%Y")
    dataI = datetime.strptime("11.12.2010", "%d.%m.%Y")
    film = Film('1', "abc", 2000, 12, "da")
    card = CardClient('1', "abc", "cfg", 12, dataN, dataI, 10)
    rezervare = Rezervare('1', film, card, "11.12.2000", "19:11")
    assert rezervare.idRezervare == '1'
    assert rezervare.film == film
    assert rezervare.card == card
    assert rezervare.dataRezervare == "11.12.2000"
    assert rezervare.oraRezervare == "19:11"