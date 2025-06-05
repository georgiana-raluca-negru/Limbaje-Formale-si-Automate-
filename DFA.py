#Un DFA este definit ca fiind un 5-tuple (Σ, Q, δ, q0, F) unde:
#    - Σ este alfabetul automatului (lista de simboluri) -> symbols 
#    - Q este multimea de stari ale automatului (lista de stari) -> states
#    - δ : Q x (Σ) -> P(Q)  a automatului (lista de tranzitii) -> rules
#    - q0 este starea inițiala a automatului -> start_state
#    - F este multimea de stari de acceptare ale automatului (lista de stari de acceptare) -> final_states

def parse_file(fisier):
    symbols = []
    rules = {}
    states = []
    start_state = None
    final_states = set()
    found = False
    
    #Incercam sa deschidem fisierul, folosim structura de try-catch pentru eventualele erori la deschiderea acestuia
    try:
        with open(fisier, "r") as f:
            #Sectiunea curenta, se refera la una dintre States, Symbols sau Rules
            current_section = None
            
            for line in f:
                line= line.strip()
                
                #Trecem peste liniile goale sau comentarii
                if not line or line.startswith("//"):
                    continue
                
                #Daca se indeplineste conditia, inseamna ca am ajuns la o noua sectiune si vom actualiza current_section
                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1]
                    continue
                
                #Cand se ajunge la 'END' inseamna ca am terminat de memorat intreaga sectiune/o parte din aceasta
                if line == "END":
                    current_section = None
                    continue
                
                #Putem avea si comentarii inline; verificam daca exista si, in caz afirmativ, trecem cu vedera comentariul
                if "//" in line:
                    line = line.split("//")[0].strip()
                
                #Actualizam, in functie de sectiunea curenta la care ne aflam, lista respectiva
                if current_section == "States":

                    #Prezenta virgulei semnaleaza faptul ca starea este fie incipienta, fie finala
                    if ", " in line:
                        state, info = line.split(", ", 1)
                        state = state.strip()
                        info = info.strip()
                        markers = [marker.strip() for marker in info.split()]
                        
                        for marker in markers:

                            #Conventie stabilita - '*' pentru starea de inceput 
                            if marker == "*":
                                if found == False:
                                    start_state = state
                                    found = True

                                #Daca exista mai mult de o stare de inceput, DFA ul este invalid
                                else:
                                    print("Eroare: A fost deja identificata o stare de inceput; Nu pot exista mai mult de una.")
                                    return None, None, None, None, None

                            #Conventie stabilita - '**' pentru starea/starile finale
                            elif marker == "**":
                                final_states.add(state)
                    else:
                        state = line
                    
                    #Verificam daca starile sunt duplicate
                    if state not in states:  
                        states.append(state)  
                    else:
                        print(f"Eroare: Starea {state} este duplicata.")
                        return None, None, None, None, None
                    
                elif current_section == "Symbols":

                    #Verficam daca simbolurile sunt duplicate
                    if line not in symbols:
                        symbols.append(line)
                    else:
                        print(f"Eroare: Simbolul {symbol} este duplicat.")
                        return None, None, None, None, None
                
                #Folosim un dictionar pentru a indentifica mai usor tuplul (current_state, symbol)
                elif current_section == "Rules":
                    parts = [part.strip() for part in line.split(", ")]
                    if len(parts) == 3:
                        current_state, symbol, dest_state = parts
                        key = (current_state, symbol)
                        
                        #Verficam daca nu cumva tranzitia a fost deja definita, fie cu alta stare destinatie sau aceeasi
                        #Facem verificarea corectitudinii in momentul parsarii din fisier caci, folosind un dictionar, intalnirea unei tranzitii duplicate nu va produce
                        #nicio eroare in cadrul functiei de validare; Prin definitie, dictionarul nu poate avea o cheie duplicata, iar o ulterioara alta definire a tranzitiei doar va suprascrie prima definire a acesteia
                        if key in rules:
                            if rules[key] != dest_state:
                                print(f"Eroare: Tranzitie duplicata cu stari destinatii diferite!")
                                print(f"  ({current_state}, {symbol}) --> {rules[key]} (prima definire)")
                                print(f"  ({current_state}, {symbol}) --> {dest_state} (a doua definire)")
                                return None, None, None, None, None
                            else:
                                print(f"Tranzitia ({current_state}, {symbol}) --> {dest_state} este deja definita.")
                                return None, None, None, None, None
                        else:
                            rules[key] = dest_state

                    else:
                        print("Eroare: Formatul tranzitiei este invalid.")
                        return None, None, None, None, None

    
    #Eroare la deschiderea fisierului
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{fisier}' nu a fost gasit.")
        return None, None, None, None, None
    
    #Eroare neasteptata
    except Exception as e:
        print(f"Eroare la citirea fisierului: {e}")
        return None, None, None, None, None
    
    return symbols, rules, states, start_state, final_states



def validate_dfa(symbols, rules, states, start_state, final_states):
    if not symbols and not states and not start_state and not final_states:
        return False
    #DFA invalid daca nu avem cel putin un simbol in alfabet
    if not symbols:
        print("Eroare: Nu este definit niciun simbol.")
        return False
    
    #DFA invalid daca nu avel cel putin o stare
    if not states:
        print("Eroare: Nu este definita nicio stare.")
        return False

    #DFA invalid daca nu avem stare de inceput
    if not start_state:
        print("Eroare: Nu exista definitia unei stari finale.")
        return False
    
    #DFA invalid daca nu avem cel putin o stare de final
    if not final_states:
        print("Eroare: Nu sunt date definitii ale unor stari finale.")
        return False
    
    for (current_state, symbol), dest_state in rules.items():
        #Verificam daca starea curenta exista in definirea starilor
        if current_state not in states:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {symbol}) --> {dest_state}, starea curenta nu este definita.")
            return False
        
        #Verificam daca starea destinatie exista in definirea starilor
        if dest_state not in states:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {symbol}) --> {dest_state}, starea destinatie nu este definita.")
            return False
        
        #Verificam daca simbolul din cadrul tranzitiei exista in definirea alfabetului
        if symbol not in symbols:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {symbol}) -> {dest_state}, simbolulu nu este definit in alfabet.")
            return False

    return True



def print_dfa_details(symbols, rules, states, start_state, final_states):
    #Afisam detaliile despre DFA
    print("---------------Definitia DFA-ului------------------")
    print("Stari: ",end = "")
    print(*states)
    print("Alfabetul: ", end = "")
    print(*symbols)
    print(f"Starea initiala: {start_state}")
    print("Stari finale: ", end = "")
    print(*final_states)
    print("Functia de tranzitie:")
    for (stare_sursa, simbol), stare_dest in rules.items():
        print(f"  δ({stare_sursa}, {simbol}) --> {stare_dest}")
    print()



def process_input(input_string, symbols, rules, start_state, final_states):
    #Functia de procesare a unui sir dat
    current_state = start_state
    #Retinem si tranzitiile care au loc pe parcusrsul parcurgerii simbolurilor
    path = [current_state]
    
    for symbol in input_string:
        if symbol not in symbols:
            #Eroare daca simbolul nu este recunoscut de DFA
            print(f"Simbolul {symbol} nu este definit in alfabet.")
            return False, current_state, path
        
        transition = (current_state, symbol)
        
        if transition not in rules:
            #Eroare daca tranzitia nu este recunoscuta de DFA
            print(f"Nu exista tranzitie din starea {current_state} cu simbolul {symbol}.")
            return False, current_state, path
        
        current_state = rules[transition]
        path.append(current_state)
    
    accept = current_state in final_states
    return accept, current_state, path


def main():
    symbols, rules, states, start_state, final_states = parse_file("input.dfa")
    #Daca nu trece testul de validare, nu facem nimic cu DFA-ul
    if not validate_dfa(symbols, rules, states, start_state, final_states):
        return
    
    print_dfa_details(symbols, rules, states, start_state, final_states)
    
    #Implementam o structura repetitiva pentru a putea introduce mai multe inputuri ale aceluiasi DFA
    while True:
        try:
            input_string = input("Introduceti un sir sau 'QUIT' pentru a iesi: ").strip()
            
            #Conditia de a iesi din bucla while - introducem sirul QUIT sau orice variatie de majusucule
            if input_string.upper() == 'QUIT':
                break
            
            accept, final_state, path= process_input(input_string, symbols, rules, start_state, final_states)
            
            print(f"Input: '{input_string}'")
            print(f"Tranzitiile: {' -> '.join(path)}")
            print(f"Starea finala: {final_state}")
            print(f"Rezultat: {'INPUT ACCEPTAT' if accept else 'INPUT RESPINS'}")
            
            print()
            print("-" * 100)
            print()
            
        except EOFError:
            break


if __name__ == "__main__":
    main()
