import re

class Grammar:
    def __init__(self):
        self.start_symbol = None
        self.terminals = set()
        self.non_terminals = set()
        self.productions = {} # dict: No-Terminal -> list[list[str]]
        # Representación de epsilon
        self.epsilon = 'e'

    def display(self):
        print(f"Símbolo Inicial: {self.start_symbol}")
        print(f"No-Terminales: {sorted(list(self.non_terminals))}")
        print(f"Terminales: {sorted(list(self.terminals))}")
        print("Producciones:")
        for nt, prods in self.productions.items():
            for prod in prods:
                print(f"  {nt} -> {' '.join(prod)}")

def validate_grammar(grammar: Grammar):
    """
    Verifica posibles errores comunes en la gramática, como falta de espacios.
    """
    for term in grammar.terminals:
        # Heurística: Si un terminal tiene paréntesis/corchetes pegados a letras (ej: '(E')
        # Probablemente sea un error de espaciado.
        if len(term) > 1 and not term.isalnum():
            if re.search(r'[(){}\[\]].*[a-zA-Z0-9]', term) or re.search(r'[a-zA-Z0-9].*[(){}\[\]]', term):
                print(f"ADVERTENCIA: El terminal '{term}' parece sospechoso. Asegúrate de separar los símbolos con espacios (ej: '( E )' en lugar de '(E)').")

def parse_grammar(lines: list[str]) -> Grammar:
    """
    Construye un objeto Grammar a partir de líneas de texto limpio generadas por el lector.
    """
    grammar = Grammar()
    
    # Primera pasada: identificar No-Terminales y Símbolo Inicial
    for line in lines:
        if '->' not in line:
            continue
            
        left_side, right_side = line.split('->', 1)
        left_side = left_side.strip()
        
        if not grammar.start_symbol:
            grammar.start_symbol = left_side
            
        grammar.non_terminals.add(left_side)
        if left_side not in grammar.productions:
            grammar.productions[left_side] = []
            
    # Segunda pasada: procesar las producciones y descubrir los Terminales
    for line in lines:
        if '->' not in line:
            continue
            
        left_side, right_side = line.split('->', 1)
        left_side = left_side.strip()
        
        # Las diferentes producciones pueden estar separadas por |
        right_productions = right_side.split('|')
        
        for prod_str in right_productions:
            prod_str = prod_str.strip()
            # Si el lado derecho está vacío, lo trataremos como epsilon
            if not prod_str:
                symbols = [grammar.epsilon]
            else:
                symbols = prod_str.split()
            
            grammar.productions[left_side].append(symbols)
            
            # Identificar terminales
            for symbol in symbols:
                if symbol not in grammar.non_terminals and symbol != grammar.epsilon:
                    grammar.terminals.add(symbol)
                    
    return grammar
