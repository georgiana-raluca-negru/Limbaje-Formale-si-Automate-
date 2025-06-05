def parse_file(fisier):
    symbols = []
    rules = {}
    states = []
    start_state = None
    final_states = set()
    tape = []
    found = False
    
    #Incercam sa deschidem fisierul, folosim structura de try-catch pentru eventualele erori
    try:
        with open(fisier, "r") as f:
            #Sectiunea curenta: Band, States, Symbols sau Rules
            current_section = None
            
            for line in f:
                line = line.strip()
                
                #Trecem peste liniile goale sau comentarii
                if not line or line.startswith("//"):
                    continue
                
                #Daca se indeplineste conditia, inseamna ca am ajuns la o noua sectiune
                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1]
                    continue
                
                #Cand se ajunge la 'END' inseamna ca am terminat sectiunea curenta
                if line == "END":
                    current_section = None
                    continue
                
                #Putem avea si comentarii inline; verificam si eliminam comentariul
                if "//" in line:
                    line = line.split("//")[0].strip()
                
                #Actualizam, in functie de sectiunea curenta, structura respectiva
                if current_section == "Band":
                    # Banda initiala a masinii Turing - handle spaces
                    if ' ' in line:
                        tape = line.split()
                    else:
                        tape = list(line)
                
                elif current_section == "States":
                    #Prezenta virgulei semnaleaza faptul ca starea este fie initiala, fie finala
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
                                #Daca exista mai mult de o stare de inceput, MT este invalid
                                else:
                                    print("Eroare: A fost deja identificata o stare de inceput; Nu pot exista mai mult de una.")
                                    return None, None, None, None, None, None
                            
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
                        return None, None, None, None, None, None
                
                elif current_section == "Symbols":
                    #Verificam daca simbolurile sunt duplicate
                    if line not in symbols:
                        symbols.append(line)
                    else:
                        print(f"Eroare: Simbolul {line} este duplicat.")
                        return None, None, None, None, None, None
                
                elif current_section == "Rules":
                    #Format: state, symbol -> next_state, new_symbol, direction
                    if " -> " in line:
                        left_part, right_part = line.split(" -> ", 1)
                        left_parts = [part.strip() for part in left_part.split(", ")]
                        right_parts = [part.strip() for part in right_part.split(", ")]
                        
                        if len(left_parts) == 2 and len(right_parts) == 3:
                            current_state, symbol = left_parts
                            next_state, new_symbol, direction = right_parts
                            
                            key = (current_state, symbol)
                            
                            # Verificam directia
                            if direction not in ['L', 'R']:
                                print(f"Eroare: Directia '{direction}' este invalida. Folositi 'L' sau 'R'.")
                                return None, None, None, None, None, None
                            
                            # Verificam daca tranzitia a fost deja definita
                            if key in rules:
                                existing_rule = rules[key]
                                new_rule = (new_symbol, direction, next_state)
                                if existing_rule != new_rule:
                                    print(f"Eroare: Tranzitie duplicata cu definitii diferite!")
                                    print(f"  ({current_state}, {symbol}) --> {existing_rule} (prima definire)")
                                    print(f"  ({current_state}, {symbol}) --> {new_rule} (a doua definire)")
                                    return None, None, None, None, None, None
                                else:
                                    print(f"Tranzitia ({current_state}, {symbol}) este deja definita.")
                                    return None, None, None, None, None, None
                            else:
                                rules[key] = (new_symbol, direction, next_state)
                        else:
                            print(f"Eroare: Formatul tranzitiei este invalid: {line}")
                            return None, None, None, None, None, None
                    else:
                        print(f"Eroare: Tranzitia nu contine ' -> ': {line}")
                        return None, None, None, None, None, None
    
    #Eroare la deschiderea fisierului
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{fisier}' nu a fost gasit.")
        return None, None, None, None, None, None
    
    #Eroare neasteptata
    except Exception as e:
        print(f"Eroare la citirea fisierului: {e}")
        return None, None, None, None, None, None
    
    return symbols, rules, states, start_state, final_states, tape


def validate_tm(symbols, rules, states, start_state, final_states, tape):
    if not symbols and not states and not start_state and not final_states:
        return False
    
    #TM invalid daca nu avem cel putin un simbol in alfabet
    if not symbols:
        print("Eroare: Nu este definit niciun simbol.")
        return False
    
    #TM invalid daca nu avem cel putin o stare
    if not states:
        print("Eroare: Nu este definita nicio stare.")
        return False
    
    #TM invalid daca nu avem stare de inceput
    if not start_state:
        print("Eroare: Nu exista definitia unei stari de inceput.")
        return False
    
    #TM invalid daca nu avem cel putin o stare finala
    if not final_states:
        print("Eroare: Nu sunt date definitii ale unor stari finale.")
        return False
    
    #TM invalid daca nu avem banda initiala
    if not tape:
        print("Eroare: Nu este definita banda initiala.")
        return False
    
    #Verificam regulile de tranzitie
    for (current_state, symbol), (new_symbol, direction, next_state) in rules.items():
        #Verificam daca starea curenta exista
        if current_state not in states:
            print(f"Eroare: In tranzitia ({current_state}, {symbol}), starea curenta nu este definita.")
            return False
        
        #Verificam daca starea destinatie exista
        if next_state not in states:
            print(f"Eroare: In tranzitia ({current_state}, {symbol}), starea destinatie {next_state} nu este definita.")
            return False
        
        #Verificam daca simbolul citit exista in alfabet sau este blank
        if symbol not in symbols and symbol != '_':
            print(f"Eroare: In tranzitia ({current_state}, {symbol}), simbolul citit nu este definit in alfabet.")
            return False
        
        #Verificam daca simbolul scris exista in alfabet sau este blank
        if new_symbol not in symbols and new_symbol != '_' and new_symbol != 's':
            print(f"Eroare: In tranzitia ({current_state}, {symbol}), simbolul scris {new_symbol} nu este definit in alfabet.")
            return False
    
    #Verificam daca toate simbolurile de pe banda sunt valide
    for symbol in tape:
        if symbol not in symbols and symbol != '_':
            print(f"Eroare: Simbolul '{symbol}' de pe banda nu este definit in alfabet.")
            return False
    
    return True


def simulate_turing_machine(symbols, rules, states, start_state, final_states, initial_tape, max_steps=1000):
    #Initializare
    tape = initial_tape.copy()
    current_state = start_state
    head_position = 0
    step = 0
    
    print("-------------Simulare Masina Turing------------")
    print(f"Banda initiala: {' '.join(tape)}")
    print()
    
    #Bucla de simulare
    while current_state not in final_states and step < max_steps:
        #Conditie de extindere a benzii, daca este necesar
        if head_position < 0:
            tape.insert(0, '_')
            head_position = 0
        elif head_position >= len(tape):
            tape.append('_')
        
        current_symbol = tape[head_position]
        
        #Verificam daca exista tranzitia
        if (current_state, current_symbol) not in rules:
            print(f"Nu exista tranzitie pentru starea {current_state} si simbolul '{current_symbol}'")
            print("Masina se opreste.")
            return False, tape, step
        
        new_symbol, direction, next_state = rules[(current_state, current_symbol)]
        
        #Scriem noul simbol, daca este diferit de s (spatiu)
        if(new_symbol == 's'):
            tape[head_position] = ' '
        else:
            tape[head_position] = new_symbol
        
        #Mutam capul
        if direction == 'R':
            head_position += 1
        elif direction == 'L':
            head_position -= 1
        
        #Actualizam starea
        current_state = next_state
        step += 1
    
    if current_state in final_states:
        return True, tape, step
    if current_state not in final_states:
        print(f"Masina s-a oprit dupa {max_steps} pasi (posibila bucla infinita)")
        return False, tape, step



def main():
    
    #Parsam fisierul
    symbols, rules, states, start_state, final_states, tape = parse_file("input.tm")
    
    if symbols is None:
        return
    
    #Validam masina Turing
    if not validate_tm(symbols, rules, states, start_state, final_states, tape):
        print("Masina Turing este invalida!")
        return
    
    print("Masina Turing este valida!")
    print(f"Stari: {states}")
    print(f"Simboluri: {symbols}")
    print(f"Starea initiala: {start_state}")
    print(f"Stari finale: {final_states}")
    print(f"Banda initiala: {' '.join(tape)}")
    print()
    
    #Simulam masina Turing
    accepted, final_tape, steps = simulate_turing_machine(symbols, rules, states, start_state, final_states, tape)
    if accepted:
        print("MASINA A ACCEPTAT!")
        print(f"Banda finala: {' '.join(final_tape)}")
        print(f"Total pasi: {steps}")


if __name__ == "__main__":
    main()