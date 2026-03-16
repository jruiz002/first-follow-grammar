from grammar_parser import Grammar
from first import compute_first_of_string

def compute_follow(grammar: Grammar, first_sets: dict[str, set[str]]) -> dict[str, set[str]]:
    """
    Calcula el conjunto FOLLOW para todos los no-terminales de la gramática.
    """
    follow_sets = {nt: set() for nt in grammar.non_terminals}
    
    # Regla 1: Colocar $ en FOLLOW del símbolo inicial
    end_symbol = '$'
    
    if grammar.start_symbol in follow_sets:
        follow_sets[grammar.start_symbol].add(end_symbol)
    
    changed = True
    while changed:
        changed = False
        
        for nt in grammar.non_terminals:
            for production in grammar.productions[nt]:
                # Para cada producción A -> X1 X2 ... Xk
                for i, symbol_B in enumerate(production):
                    if symbol_B in grammar.non_terminals:
                        # B es el símbolo actual (Xi)
                        beta = production[i+1:] # Lo que sigue de B
                        
                        original_size = len(follow_sets[symbol_B])
                        
                        # Calculamos FIRST de beta
                        first_beta = compute_first_of_string(beta, first_sets, grammar.epsilon)
                        
                        # Regla 2: Todo en FIRST(beta) excepto epsilon se agrega a FOLLOW(B)
                        follow_sets[symbol_B].update(first_beta - {grammar.epsilon})
                        
                        # Regla 3: Si beta =>* epsilon, o si beta está vacío, se agrega FOLLOW(A) a FOLLOW(B)
                        if grammar.epsilon in first_beta or not beta:
                            follow_sets[symbol_B].update(follow_sets[nt])
                            
                        if len(follow_sets[symbol_B]) > original_size:
                            changed = True
                            
    return follow_sets
