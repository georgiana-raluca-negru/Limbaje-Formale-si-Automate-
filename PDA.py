def parse_file(fisier):
    input_symbols = []
    stack_symbols = []
    rules = {} 
    states = []
    start_state = None
    final_states = set()
    found = False
    
    #Incercam sa deschidem fisierul, folosim structura de try-catch pentru eventualele erori la deschiderea acestuia
    try:
        with open(fisier, "r") as f:
             #Sectiunea curenta, se refera la una dintre States, InputSymbols, StackSymbols sau Rules
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
                
                elif current_section == "InputSymbols":

                    #Verficam daca simbolurile sunt duplicate
                    if line not in input_symbols:
                        input_symbols.append(line)
                    else:
                        print(f"Eroare: Simbolul {line} este duplicat.")
                        return None, None, None, None, None, None
                
                elif current_section == "StackSymbols":

                    #Verficam daca simbolurile sunt duplicate
                    if line not in stack_symbols:
                        stack_symbols.append(line)
                    else:
                        print(f"Eroare: Simbolul stivei {line} este duplicat.")
                        return None, None, None, None, None, None
                
                #Folosim un dictionar pentru a indentifica mai usor tuplul (current_state, input_symbol, stack_top)
                elif current_section == "Rules":
                    if " -> " in line:
                        left, right = line.split(" -> ", 1)
                        left_parts = [part.strip() for part in left.split(", ")]
                        right_parts = [part.strip() for part in right.split(", ")]
                        
                        if len(left_parts) == 3 and len(right_parts) == 2:
                            current_state, input_symbol, stack_top = left_parts
                            dest_state, stack_push = right_parts
                            key = (current_state, input_symbol, stack_top)
                            transition = (dest_state, stack_push)

                            if key in rules:
                                if rules[key] != transition:
                                   existing_transition = rules[key]
                                   print(f"Eroare: Tranzitie duplicata cu stari destinatii diferite!")
                                   print(f"  ({current_state}, {input_symbol}, {stack_top}) --> ({existing_transition[0]}, {existing_transition[1]}) (prima definire)")
                                   print(f"  ({current_state}, {input_symbol}, {stack_top}) --> ({dest_state}, {stack_push}) (prima definire)")
                                   return None, None, None, None, None, None
                                else:
                                   print(f"Tranzitia ({current_state}, {input_symbol}, {stack_top}) --> {transition} este deja definită.")
                                   return None, None, None, None, None, None
                            else:
                                rules[key] = transition
                        else:
                            print("Eroare: Formatul tranzitiei PDA este invalid. Format: state, input, stack_top -> dest_state, stack_push")
                            return None, None, None, None, None, None
                    else:
                        print("Eroare: Formatul tranzitiei PDA este invalid. Lipsește '->'")
                        return None, None, None, None, None, None
    
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{fisier}' nu a fost gasit.")
        return None, None, None, None, None, None
    except Exception as e:
        print(f"Eroare la citirea fisierului: {e}")
        return None, None, None, None, None, None
    
    return input_symbols, stack_symbols, rules, states, start_state, final_states

def validate_pda(input_symbols, stack_symbols, rules, states, start_state, final_states):
    #PDA invalid daca nu avem cel putin un simbol in alfabetul de input
    if not input_symbols:
        print("Eroare: Nu este definit niciun simbol in alfabetul de input.")
        return False
    
    #PDA invalid daca nu avem cel putin un simbol in alfabetul stivei
    if not stack_symbols:
        print("Eroare: Nu este definit niciun simbol in alfabetul stivei.")
        return False
    
    #PDA invalid daca nu avel cel putin o stare
    if not states:
        print("Eroare: Nu este definita nicio stare.")
        return False

    #PDA invalid daca nu avem stare de inceput
    if not start_state:
        print("Eroare: Nu exista definitia unei stari initiale.")
        return False
    
    #PDA invalid daca nu avem cel putin o stare de final
    if not final_states:
        print("Eroare: Nu sunt date definitii ale unor stari finale.")
        return False
    
    #Necesar sa avem 'Z' in alfabetul stivei, el ne va anunta daca stiva e goala sau nu
    if 'Z' not in stack_symbols:
        print("Eroare: Simbolul de bază al stivei 'Z' nu este definit în alfabetul stivei.")
        return False
    
    for (current_state, input_symbol, stack_top), (dest_state, stack_push) in rules.items():
        #Verificam daca starea curenta exista in definirea starilor
        if current_state not in states:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {input_symbol}, {stack_top}) --> ({dest_state}, {stack_push}), starea curentă nu este definita.")
            return False
        
        #Verificam daca starea destinatie exista in definirea starilor
        if dest_state not in states:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {input_symbol}, {stack_top}) -> ({dest_state}, {stack_push}), starea destinatie nu este definita.")
            return False
        
        #Verificam daca simbolul de input din cadrul tranzitiei exista in definirea alfabetului
        if input_symbol != 'epsilon' and input_symbol not in input_symbols:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {input_symbol}, {stack_top}) --> ({dest_state}, {stack_push}), simbolul de input nu este definit în alfabet.")
            return False
        
        #Verificam daca simbolul stivei (stack_top) din cadrul tranzitiei exista in definirea alfabetului
        if stack_top not in stack_symbols:
            print(f"Eroare: In cadrul tranzitiei ({current_state}, {input_symbol}, {stack_top}) --> ({dest_state}, {stack_push}), simbolul stivei nu este definit în alfabetul stivei.")
            return False
            
        #Verficam daca stack_push este o combinatie de simboluri din alfabetul stivei
        if stack_push != 'epsilon':
            valid_push = True
            remaining = stack_push
                
            while remaining and valid_push:
                found_symbol = False
                    
                for symbol in sorted(stack_symbols, key=len, reverse=True):
                    if remaining.startswith(symbol):
                        remaining = remaining[len(symbol):]
                        found_symbol = True
                        break
                    
                if not found_symbol:
                    print(f"Eroare: În cadrul tranzitiei ({current_state}, {input_symbol}, {stack_top}) -> ({dest_state}, {stack_push}), secvența '{remaining}' din push nu poate fi parsată cu alfabetul stivei.")
                    valid_push = False
                
            if not valid_push:
                return False

    return True

#Afisam detaliile despre PDA, intr-o maniera organizata
def print_pda_details(input_symbols, stack_symbols, rules, states, start_state, final_states):
    print("---------------Definiția PDA-ului (format compact)------------------")
    print(f"Stări: {{{', '.join(states)}}}")
    print(f"Σ (alfabet input): {{{', '.join(input_symbols)}}}")
    print(f"Γ (alfabet stivă): {{{', '.join(stack_symbols)}}}")
    print(f"q₀ (stare inițială): {start_state}")
    print(f"F (stări finale): {{{', '.join(final_states)}}}")
    print("δ (funcția de tranziție):")
    for (current_state, input_symbol, stack_top), (dest_state, stack_push) in rules.items():
        print(f"  ({current_state}, {input_symbol}, {stack_top}) → ({dest_state}, {stack_push})")
    print()


def parse_stack_symbols(stack_string, stack_symbols):
    if stack_string == 'epsilon':
        return []
    
    symbols = []
    remaining = stack_string
    
    while remaining:
        found_symbol = False
        #Le luam in ordine descracsatoare a lungimii simbolurilor
        for symbol in sorted(stack_symbols, key=len, reverse=True):
            if remaining.startswith(symbol):
                symbols.append(symbol)
                remaining = remaining[len(symbol):]
                found_symbol = True
                break
        
        if not found_symbol:
            return []
    
    return symbols

def process_stack_operation(stack, stack_push, stack_symbols):

    #Mereu vom da pop de pe stiva
    new_stack = stack.copy()
    if new_stack:
        new_stack.pop()
    
    #Daca avem cuvantul nul pentru push, nu vom da push la nimic si dam return stivei
    if stack_push == 'epsilon':
        return new_stack
    
    #Parsam simbolurile pentru ca e posibil ca literele sa nu coincida cu simbolurile insisi (a fost necesar pentru Z0)
    symbols_to_push = parse_stack_symbols(stack_push, stack_symbols)
    
    if not symbols_to_push and stack_push != 'epsilon':
        print(f"Error: Could not parse stack operation '{stack_push}'")
        return new_stack
    
    #Dam oush pe stiva simbolurilor, in ordine inversa
    for symbol in reversed(symbols_to_push):
        new_stack.append(symbol)
    
    return new_stack

def process_input(input_string, input_symbols, stack_symbols, rules, start_state, final_states):

    #Validam caracterele din string 
    for char in input_string:
        if char not in input_symbols:
            print(f"Eroare: Caracterul '{char}' nu există în alfabetul de intrare.")
            return False
        
    current_state = start_state
    input_pos = 0
    #Initializam stiva cu 'Z'
    #Nu am mai adaugat in input.pda sectiunea respectiva; am ales sa initializez direct
    stack = ['Z']
    
    while True:
        #Verficam daca am terminat de citit inputul
        if input_pos >= len(input_string):
            #Daca am ajuns intr-un stadiu final, returnam True
            if current_state in final_states:
                return True
            
            #Daca stiva este goala (nu mai este nici simbolul 'Z' de verificare), si nu am ajuns in stare finala, returnam False
            if not stack:
                return False
                
            #Incercam tranzitiile cu epsilon
            stack_top = stack[-1]
            epsilon_key = (current_state, 'epsilon', stack_top)
            if epsilon_key in rules:
                dest_state, stack_push = rules[epsilon_key]
                stack = process_stack_operation(stack, stack_push, stack_symbols)
                current_state = dest_state
                continue
            else:
                return False
        
        #Daca, totusi, nu am terminat de citit intreg inputul si stiva e goala, returnam False
        if not stack:
            return False
            
        stack_top = stack[-1]

        #Continuam cu citirea inputului    
        current_char = input_string[input_pos]
        
        char_key = (current_state, current_char, stack_top)
        if char_key in rules:
            dest_state, stack_push = rules[char_key]
            stack = process_stack_operation(stack, stack_push, stack_symbols)
            current_state = dest_state
            input_pos += 1
            continue
        
        #Incercam tranzitiile cu epsilon
        epsilon_key = (current_state, 'epsilon', stack_top)
        if epsilon_key in rules:
            dest_state, stack_push = rules[epsilon_key]
            stack = process_stack_operation(stack, stack_push, stack_symbols)
            current_state = dest_state
            continue
        
        return False

def main():
    input_symbols, stack_symbols, rules, states, start_state, final_states = parse_file("input.pda")
      
    if not validate_pda(input_symbols, stack_symbols, rules, states, start_state, final_states):
        return
    
    print_pda_details(input_symbols, stack_symbols, rules, states, start_state, final_states)
    
    while True:
        try:
            input_string = input("Introduceti un sir sau 'QUIT' pentru a iesi: ").strip()
            
            if input_string.upper() == 'QUIT':
                break
            
            accepted = process_input(input_string, input_symbols, stack_symbols, rules, start_state, final_states)
            
            print(f"Rezultat: {'INPUT ACCEPTAT' if accepted else 'INPUT RESPINS'}")
            
            print()
            print("-"*100)
            print()
            
        except EOFError:
            break

if __name__ == "__main__":
    main()