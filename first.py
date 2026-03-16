from grammar_parser import Grammar

def compute_first(grammar: Grammar) -> dict[str, set[str]]:
    """
    Calcula dinámicamente el conjunto FIRST para todos los símbolos (terminales y no terminales)
    y para epsilon.
    """
    first_sets = {}
    
    # 1. Inicializar FIRST para terminales y epsilon
    for terminal in grammar.terminals:
        first_sets[terminal] = {terminal}
    
    # epsilon también deriva en su propio conjunto
    first_sets[grammar.epsilon] = {grammar.epsilon}
    
    # Inicializar FIRST para no-terminales con conjunto vacío
    for nt in grammar.non_terminals:
        first_sets[nt] = set()

    changed = True
    while changed:
        changed = False
        
        for nt in grammar.non_terminals:
            for production in grammar.productions[nt]:
                # Para cada producción A -> X1 X2 ... Xk
                
                # Llevar la pista de si todos los símbolos hasta Xi pueden derivar epsilon
                all_can_derive_epsilon = True
                
                for symbol in production:
                    if symbol == grammar.epsilon:
                        if grammar.epsilon not in first_sets[nt]:
                            first_sets[nt].add(grammar.epsilon)
                            changed = True
                        break # Si hay un epsilon directo en una cadena, detenemos el consumo
                    
                    # Agregar FIRST(symbol) - {e} a FIRST(nt)
                    original_size = len(first_sets[nt])
                    
                    symbol_first = first_sets[symbol]
                    first_sets[nt].update(symbol_first - {grammar.epsilon})
                    
                    if len(first_sets[nt]) > original_size:
                        changed = True
                        
                    # Si el símbolo actual no puede derivar epsilon, detenemos el avance en esta regla de producción
                    if grammar.epsilon not in symbol_first:
                        all_can_derive_epsilon = False
                        break
                        
                # Si todos los X1...Xk en la parte derecha pueden derivar a epsilon,
                # entonces A =>* e
                if all_can_derive_epsilon and production != [grammar.epsilon]:
                    if grammar.epsilon not in first_sets[nt]:
                        first_sets[nt].add(grammar.epsilon)
                        changed = True

    return first_sets

def compute_first_of_string(symbols: list[str], first_sets: dict[str, set[str]], epsilon: str) -> set[str]:
    """
    Función utilitaria matemática que calcula el FIRST de una secuencia de símbolos (y1, y2, ... yn),
    utilizado luego extensamente en el cálculo de los conjuntos FOLLOW.
    """
    result = set()
    if not symbols:
        return {epsilon}
        
    for symbol in symbols:
        if symbol == epsilon:
            result.add(epsilon)
            break
            
        # Obtener first del simbolo. Si es desconocido, se trata como sí mismo.
        sym_first = first_sets.get(symbol, {symbol} if symbol != epsilon else {epsilon})
        result.update(sym_first - {epsilon})
        
        # Si un símbolo en la cadena no puede derivar epsilon, cortamos evaluación.
        if epsilon not in sym_first:
            break
    else:
        # Si no se interrumpió el loop y todos derivaron epsilon en cascada, entonces toda
        # la cadena genera epsilon 
        result.add(epsilon)
        
    return result
