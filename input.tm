//Band reprezinta banda pe care lucram. Vom pune spatiu intre fiecare 2 caractere
//Se va adauga, la final simbolul '$' pentru a marca finalulu benzii


[Band]
1 1 1 1 + 1 1 1 1 1 $
END


//Starile
//Starea finala este marcata cu **, iar starea initiala cu *
//De precizat ca o stare poate fi, concomitent, initiala si finala (este scrisa sub forma 'q, *, **')
[States]
q0, *                        //Stare initiala (*)
q1
q2, **                       //Stare finala (**)
END


//Simboluri (s este tratat separat, si este pe post de spatiu)
[Symbols]
1
+
$
END


//Reguli
//Sunt scrise sub forma: stare_curenta, simbol -> stare_destinatie, simbol_nou, directie
[Rules]
q0, 1 -> q0, 1, R               //Daca suntem in q0 si intalnim simboulul '1', ramanem in q0, pastram '1' si mergem in dreapta
q0, + -> q0, 1, R               //Daca suntem in q0 si intalnim '+', ramanen in q0, suprascriem '+' cu '1' si mergem in dreapta
q0, $ -> q1, s, L               //Daca suntem in qo si intalnim sfarsotul benzii (simbolul '$'), trecem in q1, punem spatiu in locul lui '$' si mergem in stanga
q1, 1 -> q2, $, R               //Daca suntem in q1 si intalnim 1 (suntem la final si avem un 1 in plus), trecem in starea finala, supracsriem '1' cu simbolulu final '$' si mergem in dreapta spre finalulu benzii
END