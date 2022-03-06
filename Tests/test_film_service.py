from Domain.film_validator import FilmValidator
from Repository.file_repository import FileRepository
from Service.film_service import FilmService
from Service.undo_redo_service import UndoRedoService
from Tests.utils import clear_file


def testAdaugareFilm():
    clear_file("filmTest.txt")
    filmRepository = FileRepository("filmTest.txt")
    filmValidator = FilmValidator()
    undo_redo_service = UndoRedoService()
    service = FilmService(filmRepository, filmValidator, undo_redo_service)

    service.adaugare('1', "abc", 2000, 12, "da")
    assert len(service.getAll()) == 1
    added = filmRepository.getById('1')
    assert added is not None
    assert added.idFilm == '1'
    assert added.titluFilm == 'abc'
    assert added.anAparitie == 2000
    assert added.pretFilm == 12
    assert added.inProgram == 'da'

    try:
        service.adaugare('1', "abc", 2000, 12, "da")
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

def testStergereFilm():
    clear_file("filmTest.txt")
    filmRepository = FileRepository("filmTest.txt")
    filmValidator = FilmValidator()
    undo_redo_service = UndoRedoService()
    service = FilmService(filmRepository, filmValidator, undo_redo_service)
    service.adaugare('1', "abc", 2000, 12, "da")
    service.adaugare('2', "abcd", 2001, 12, "da")

    try:
        service.stergere('3')
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False

def testModificareFilm():
    clear_file("filmTest.txt")
    filmRepository = FileRepository("filmTest.txt")
    filmValidator = FilmValidator()
    undo_redo_service = UndoRedoService()
    service = FilmService(filmRepository, filmValidator, undo_redo_service)
    service.adaugare('1', "abc", 2000, 12, "da")
    service.adaugare('2', "abcd", 2001, 12, "da")

    service.modificare('1', "xyz", 2002, 12, "da")
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
        service.modificare('3', "xyz", 2002, 12, "da")
        assert False
    except KeyError:
        assert True
    except Exception:
        assert False