from Domain.film import Film
from Repository.file_repository import FileRepository
from Tests.utils import clear_file


def testAdaugareFilmRepo():
    clear_file("repositoryTest.txt")
    filmRepository = FileRepository("repositoryTest.txt")

    filmRepository.adaugare(Film('1', "abc", 2000, 12, "da"))
    assert len(filmRepository.getAll()) == 1
    added = filmRepository.getById('1')
    assert added is not None
    assert added.idFilm == '1'
    assert added.titluFilm == 'abc'
    assert added.anAparitie == 2000
    assert added.pretFilm == 12
    assert added.inProgram == 'da'


def testStergereFilmRepo():
    clear_file("repositoryTest.txt")
    filmRepository = FileRepository("repositoryTest.txt")

    filmRepository.adaugare(Film('1', "abc", 2000, 12, "da"))
    filmRepository.adaugare(Film('2', "abcd", 2001, 12, "da"))

    try:
        filmRepository.stergere('3')
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

    filmRepository.stergere('1')
    assert len(filmRepository.getAll()) == 1
    deleted = filmRepository.getById('1')
    assert deleted is None
    remaining = filmRepository.getById('2')
    assert remaining is not None
    assert remaining.idFilm == '2'
    assert remaining.titluFilm == 'abcd'
    assert remaining.anAparitie == 2001
    assert remaining.pretFilm == 12
    assert remaining.inProgram == 'da'

def testModificareFilmRepo():
    clear_file("repositoryTest.txt")
    filmRepository = FileRepository("repositoryTest.txt")

    filmRepository.adaugare(Film('1', "abc", 2000, 12, "da"))
    filmRepository.adaugare(Film('2', "abcd", 2001, 12, "da"))

    filmRepository.modificare(Film('1', "xyz", 2002, 12, "da"))
    updated = filmRepository.getById('1')

    assert updated is not None
    assert updated.idFilm == '1'
    assert updated.titluFilm == 'xyz'
    assert updated.anAparitie == 2002
    assert updated.pretFilm == 12
    assert updated.inProgram == 'da'

    unchanged = filmRepository.getById('2')
    assert unchanged is not None
    assert unchanged.idFilm == '2'
    assert unchanged.titluFilm == 'abcd'
    assert unchanged.anAparitie == 2001
    assert unchanged.pretFilm == 12
    assert unchanged.inProgram == 'da'

    try:
        filmRepository.modificare(Film('3', "xyz", 2002, 12, "da"))
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False