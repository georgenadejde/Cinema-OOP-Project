from Domain.film import Film


class FilmValidator:
    def valideaza(self, film : Film):
        erori = []
        if film.inProgram not in ["da", "nu"]:
            erori.append("In program poate sa fie doar 'da' sau 'nu'")
        if len(erori) > 0:
            raise ValueError(erori)