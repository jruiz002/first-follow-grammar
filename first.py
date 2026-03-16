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
                # Calcular FIRST(rhs) usando la función utilitaria
                rhs_first = compute_first_of_string(production, first_sets, grammar.epsilon)
                
                # Actualizar FIRST(nt)
                before_size = len(first_sets[nt])
                first_sets[nt].update(rhs_first)
                
                if len(first_sets[nt]) > before_size:
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
