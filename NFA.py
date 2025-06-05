#Un NFA este definit ca fiind un 5-tuplu (Σ, Q, δ, q0, F) unde:
#    - Σ este alfabetul automatului (lista de simboluri) -> symbols
#    - Q este multimea de stari ale automatului (lista de stari) -> states
#    - δ : Q x (Σ U {ε}) -> P(Q)  este functia de tranzitie a automatului (lista de tranzitii) -> rules
#    - q0 este starea inițiala a automatului (start_state) -> start_state
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
                line = line.strip()
            
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
                      
                        if "ε" not in symbols and line != "epsilon":
                            pass 
                    else:
                        print(f"Eroare: Simbolul {line} este duplicat.")
                        return None, None, None, None, None
                
                #Folosim un dictionar pentru a indentifica mai usor tuplul (current_state, symbol)
                elif current_section == "Rules":
                    parts = [part.strip() for part in line.split(", ")]
                    if len(parts) == 3:
                        current_state, symbol, dest_state = parts
                        key = (current_state, symbol)
                        
                        #NFA-ul accepta ca cheia sa aiba mai multe tranzitii, prim urmare ii vom asocia cheii o lista de stari
                        if key not in rules:
                            rules[key] = []
                        
                        #Adaugam o noua stare destinatie
                        if dest_state not in rules[key]:
                            rules[key].append(dest_state)
                        else:
                            print(f"Tranzitia ({current_state}, {symbol}) --> {dest_state} este deja definita.")
                            return None, None, None, None, None
                    
                    else:
                        print("Eroare: Formatul tranzitiei este invalid.")
                        return None, None, None, None, None
    
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{fisier}' nu a fost gasit.")
        return None, None, None, None, None
    except Exception as e:
        print(f"Eroare la citirea fisierului: {e}")
        return None, None, None, None, None
    
    return symbols, rules, states, start_state, final_states


def validate_nfa(symbols, rules, states, start_state, final_states):
    if not symbols and not states and not start_state and not final_states:
        return False
    
    #NFA invalid daca nu avem cel putin un simbol in alfabet
    if not symbols:
        print("Eroare: Nu este definit niciun simbol.")
        return False
    
    #NFA invalid daca nu avel cel putin o stare
    if not states:
        print("Eroare: Nu este definita nicio stare.")
        return False

    #NFA invalid daca nu avem stare de inceput
    if not start_state:
        print("Eroare: Nu exista definitia unei stari finale.")
        return False
    
    #NFA invalid daca nu avem cel putin o stare de final
    if not final_states:
        print("Eroare: Nu sunt date definitii ale unor stari finale.")
        return False
    
    for (current_state, symbol), dest_states in rules.items():
        #Verificam daca starea curenta exista in definirea starilor
        if current_state not in states:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {symbol}) --> {dest_state}, starea curenta nu este definita.")
            return False
        
        #Verificam daca starea destinatie exista in definirea starilor
        for dest_state in dest_states:
            if dest_state not in states:
                print(f"Eroare: Starea destinatie '{dest_state}' din tranzitie nu este definita.")
                return False
        
        #Verificam daca simbolul din cadrul tranzitiei exista in definirea alfabetului
        if symbol not in symbols:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {symbol}) -> {dest_state}, simbolul nu este definit in alfabet.")
            return False

    return True


def print_nfa_details(symbols, rules, states, start_states, final_states):
    print("---------------Definitia NFA-ului------------------")
    print("Stari: ", end="")
    print(*states)
    print("Alfabetul: ", end="")
    print(*symbols)
    print("Starea initiala: ", end="")
    print(*start_states)
    print("Stari finale: ", end="")
    print(*final_states)
    print("Functia de tranzitie:")
    for (stare_sursa, simbol), stari_dest in rules.items():
        for stare_dest in stari_dest:
            print(f"  δ({stare_sursa}, {simbol}) --> {stare_dest}")
    print()

def epsilon_states(start_state, rules):

    #Verificam starile in care putem ajunge, incepand dintr-o anumita stare, consumand cuvantul nul ε
    reachable_states = set(start_state)
    
    #Lista pentru starile pe care le avem de verificat in continuare
    states_to_check = list(start_state)
    
    #Trecem prin toate starile pe care le avem de verificat
    while states_to_check:
        current_state = states_to_check.pop()
        
        #Verficiam daca putem consuma caracterul ε din starea curenta la care ne aflam
        if (current_state, "epsilon") in rules:
            #Luam toate starile accesibile prin ε
            epsilon_destinations = rules[(current_state, "epsilon")]
            
            #Adaugam starile in care putem ajunge in reachable_states
            for destination in epsilon_destinations:
                if destination not in reachable_states:
                    reachable_states.add(destination)
                    #Vom da append starii destinatie in lista starilor ce urmeaza a fi verificate pentru a vedea daca acestea, 
                    # la randul lor, au tranzitii cu ε
                    states_to_check.append(destination)
    
    return reachable_states


#Functie care returneaza toate starile din care putem ajunge dintr-un set de stari la care ne aflam
#Daca nu are nicio tranzitie cu simbolul respectiv, ramanem in starea curenta
def move(states_set, symbol, rules):
    result = set()
    for state in states_set:
        if (state, symbol) in rules:
            result.update(rules[(state, symbol)])
        else:
            result.add(state)
    return result


def process_input(input_string, symbols, rules, start_state, final_states):

    #Cautam daca putem ajunge mai departe prin ε
    current_states = epsilon_states({start_state}, rules)
    
    print(f"Starea initiala (cu epsilon-closure): {sorted(list(current_states))}")
    
    #Verificam daca simbolul exista in alfabet
    for symbol in input_string:
        if symbol not in symbols:
            print(f"Simbolul '{symbol}' nu este definit in alfabet.")
            return False, current_states
        
        #Calculam starile in care putem ajunge prin consumarea simbolului curent
        next_states = move(current_states, symbol, rules)
        if not next_states:

            #Ne-am blocat si nu putem continua mai departe
            print(f"Nu exista tranzitie din starile {sorted(list(current_states))} cu simbolul '{symbol}'.")
            return False, current_states
        
        #Consumam cuvantul nul ε, acolo unde putem si reactualizam current_states pentru a trece la urmatorul simbol
        current_states = epsilon_states(next_states, rules)
        
        print(f"Dupa simbolul '{symbol}': {sorted(list(current_states))}")
    
    #Intersectam starile curente la care nu aflam cu lista starilor finale si, in cazul in care intersectia este o multime nevida, inseamna
    #ca avem cel putin o stare de accept

    accepted = bool(current_states.intersection(final_states))
    return accepted, current_states


def main():
    symbols, rules, states, start_state, final_states = parse_file("input.nfa")
      
    if not validate_nfa(symbols, rules, states, start_state, final_states):
        return
    
    print_nfa_details(symbols, rules, states, start_state, final_states)
    
    #Implementam o structura repetitiva pentru a putea introduce mai multe inputuri ale aceluiasi DFA
    while True:
        try:
            input_string = input("Introduceti un sir sau 'QUIT' pentru a iesi: ").strip()
            
             #Conditia de a iesi din bucla while - introducem sirul QUIT sau orice variatie de majusucule
            if input_string.upper() == 'QUIT':
                break
            
            accepted, final_states_reached = process_input(input_string, symbols, rules, start_state, final_states)
            
            print(f"\nRezultat final:")
            print(f"Stari finale atinse: {sorted(list(final_states_reached))}")
            print(f"Rezultat: {'INPUT ACCEPTAT' if accepted else 'INPUT RESPINS'}")
            
            print()
            print("-"*100)
            print()
            
        except EOFError:
            break

if __name__ == "__main__":
    main()

