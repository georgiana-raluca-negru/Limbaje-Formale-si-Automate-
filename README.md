# Limbaje Formale si Automate

În acest repository am integrat temele de laborator la care am lucrat de-a lungul acestui semestru, in cadrul cursul CS112: Limbaje Formale si Automate (Formal Languages and Automata Theory). Proiectul cuprinde definirea și implementarea mai multor automate, precum:
- DFA (Deterministic Formal Automata)
- NFA (Non-Deterministic Formal Automata)
- PDA (Push-Down Automata)
- Turing Machine
  
Descrierea fiecărui tip de automat se găsește, sub forma unui comentariu, la începutul fiecărui fișier .py. În repository se găsesc atât fișierele .py corespunzătoare fiecărei teme de laborator cât și fișiere text din care am preluat datele. Fișierele text corespunzatoare automatelor au extensia dată de numele automatului (exemplu, am folosit fișierul text input.pda pentru a-mi prelua datele necesare PDA-ului).

Codul este scris în Python, însoțit de comentarii succinte care fac înțelegerea codului mai ușoară. 
Am încercat implmentarea cât mai modulară a proiectelor: cod structurat în funcții care, în funcție de context și automat, au fost reinterpretate.

Pentru a rula fișierele, este necesar ca Python să fie instalat; în cazul în care nu îl aveți deja, îi puteți da download de aici: [python.org](https://www.python.org/downloads/).
După ce vă asigurați că aveți Python instalat pe dispozitiv, deschideți un IDE și rulați unul dintre fișiere.


## Structura fișierelor și a comentariilor
Fișiere cu extensia .dfa
===================================


    [States]
    state1, * , **                 //Initial state (*)
    state2, **                     //Final state (**)
    state3
    ----------
    stateN, **
    END

    [Symbols]
    symbol1
    symbol2
    ----------
    symbolN
    END

    [Rules]
    current_state1, symbol, dest_state1
    current_state2, symbol, dest_state2
    ----------
    END


