def epsilon_closure(states_set, rules):
    #Verificam starile in care putem ajunge, incepand dintr-o anumita stare, consumand cuvantul nul ε
    closure = set(states_set)
    #Lista pentru starile pe care le avem de verificat in continuare
    stack = list(states_set)
    
    #Trecem prin toate starile pe care le avem de verificat
    while stack:
        current_state = stack.pop()
        
        #Verficiam daca putem consuma caracterul ε din starea curenta la care ne aflam
        if (current_state, "epsilon") in rules:
            #Adaugam starile in care putem ajunge in closure
            for dest_state in rules[(current_state, "epsilon")]:
                if dest_state not in closure:
                    closure.add(dest_state)
                    #Vom da append starii destinatie in lista starilor ce urmeaza a fi verificate pentru a vedea daca acestea, 
                    # la randul lor, au tranzitii cu ε
                    stack.append(dest_state)
    
    return closure


def move_nfa(states_set, symbol, rules):
    #Luam toate starile in care putem ajunge daca consumam un anumit simbol
    result = set()
    for state in states_set:
        if (state, symbol) in rules:
            result.update(rules[(state, symbol)])
    return result


def nfa_to_dfa(symbols, rules, states, start_state, final_states):
    
    dfa_symbols = [s for s in symbols if s != "epsilon"]
    
    #Initializam componentele DFA-ului
    dfa_states = []
    dfa_rules = {}
    dfa_final_states = set()
    
    #Starea de start a DFA-ului este cea data de epsilon_closure la inceput
    start_closure = epsilon_closure({start_state}, rules)
    dfa_start_state = frozenset(start_closure)
    
    #Unrpocessed retine starile DFA-ului neprocesate
    unprocessed = [dfa_start_state]
    processed = set()
    
    state_names = {}
    state_counter = 0
    
    def get_state_name(state_set):
        nonlocal state_counter
        if state_set not in state_names:
            state_names[state_set] = f"q{state_counter}"
            state_counter += 1
        return state_names[state_set]
    
    #Procesam starile DFA-ului
    while unprocessed:
        current_dfa_state = unprocessed.pop(0)
        
        if current_dfa_state in processed:
            continue
            
        processed.add(current_dfa_state)
        current_name = get_state_name(current_dfa_state)
        dfa_states.append(current_name)
        
        #Verificam daca starea este stare finala in NFA
        if any(nfa_state in final_states for nfa_state in current_dfa_state):
            dfa_final_states.add(current_name)
        
        #Procesam fiecare simbol
        for symbol in dfa_symbols:
            #CAlculam starile in care putem ajunge cu un anumit simbol cu functia move_nfa
            moved_states = move_nfa(current_dfa_state, symbol, rules)
            
            if moved_states:
                #Calculam epsilon_closure
                next_dfa_state = frozenset(epsilon_closure(moved_states, rules))
                next_name = get_state_name(next_dfa_state)
                
                #Adaugam tranzitia 
                dfa_rules[(current_name, symbol)] = next_name
                
                #Daca utmatoarea stare nu a fost procesata, o adaugam in lista
                if next_dfa_state not in processed:
                    unprocessed.append(next_dfa_state)
    
    start_name = get_state_name(dfa_start_state)
    
    return dfa_states, dfa_rules, start_name, dfa_final_states, state_names


def print_dfa(dfa_states, dfa_rules, dfa_start_state, dfa_final_states, symbols, state_names):
    dfa_symbols = [s for s in symbols if s != "epsilon"]
    
    print("----------DFA-UL converttit--------- ")
    
    print("Stari: ", end ="")
    print(*dfa_states)
    print("Alfabetul: ", end = "")
    print(*dfa_symbols)
    print("Starea initiala: ", end = "")
    print(*dfa_start_state)
    print("Stari finale: ", end = "")
    print(*dfa_final_states)
    
    print("Functia de tranzitie:")
    for (state, symbol), dest_state in sorted(dfa_rules.items()):
        print(f"  δ({state}, {symbol}) = {dest_state}")
    


def convert_nfa_to_dfa(nfa_file="input.nfa"):
    #Importam functiile deja existente in fisierul NFA.py
    from NFA import parse_file, validate_nfa
    
    #Parsam fisierul de input (tot input.nfa)
    symbols, rules, states, start_state, final_states = parse_file(nfa_file)
    
    if not validate_nfa(symbols, rules, states, start_state, final_states):
        print("Invalid NFA. Cannot proceed with conversion.")
        return None
    
    #Convertim NFA la DFA
    dfa_states, dfa_rules, dfa_start_state, dfa_final_states, state_names = nfa_to_dfa(
        symbols, rules, states, start_state, final_states
    )
    
    print_dfa(dfa_states, dfa_rules, dfa_start_state, dfa_final_states, symbols, state_names)
    
    #Returnam componenteke DFA-ului ca un dictionar
    return {
        'states': dfa_states,
        'rules': dfa_rules,
        'start_state': dfa_start_state,
        'final_states': dfa_final_states,
        'symbols': [s for s in symbols if s != "epsilon"],
        'state_mapping': state_names
    }

if __name__ == "__main__":
    dfa = convert_nfa_to_dfa()
    if dfa:
        print(f"\nDFA-ul memorat cuprinde {len(dfa['states'])} stari")