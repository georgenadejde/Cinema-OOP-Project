from Tests.test_card_service import testAdaugareCard, testStergereCard, testModificareCard
from Tests.test_domain import testFilm, testCard, testRezervare
from Tests.test_film_repository import testAdaugareFilmRepo, testStergereFilmRepo, testModificareFilmRepo
from Tests.test_film_service import testModificareFilm, testStergereFilm, testAdaugareFilm
from Tests.test_rezervare_service import testAdaugareRezervare, testStergereRezervare, testModificareRezervare


def runAllTests():
    testFilm()
    testCard()
    testRezervare()

    # testAdaugareFilm()
    # testStergereFilm()
    # testModificareFilm()
    #
    # testAdaugareCard()
    # testStergereCard()
    # testModificareCard()
    #
    # testAdaugareRezervare()
    # testStergereRezervare()
    # testModificareRezervare()
    #
    # testAdaugareFilmRepo()
    # testStergereFilmRepo()
    # testModificareFilmRepo()
