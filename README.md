# Python OOP Project 

## Cinema

- Functionalities:

1. CRUD film: id, titlu, an apariție, preț bilet, în program. Prețul să fie strict pozitiv.
2. CRUD card client: id, nume, prenume, CNP, data nașterii (dd.mm.yyyy), data înregistrării
(dd.mm.yyyy), puncte acumulate. CNP-ul trebuie să fie unic.
3. CRUD rezervare: id, id_film, id_card_client (poate fi nul), data și ora. Clientul
acumulează pe card 10% (parte întreagă) din prețul filmului Se tipărește numărul total
de puncte de pe card. Rezervarea se poate face doar dacă filmul este încă în program.
4. Căutare filme și clienți după titlu, nume, prenume, CNP etc. Căutare full text.
5. Afișarea tuturor rezervărilor dintr-un interval de ore dat, indiferent de zi.
6. Afișarea filmelor ordonate descrescător după numărul de rezervări.
7. Afișarea cardurilor client ordonate descrescător după numărul de puncte de pe card.
8. Ștergerea tuturor rezervărilor dintr-un anumit interval de zile.
9. Incrementarea cu o valoare dată a punctelor de pe toate cardurile a căror zi de naștere
se află într-un interval dat.
10. Generare filme random
11. Undo and redo
12. Validatori, teste.
13. Export date intr-un fisier excel