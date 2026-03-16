import sys
from grammar_reader import read_grammar
from grammar_parser import parse_grammar, validate_grammar
from first import compute_first
from follow import compute_follow

def display_sets(name: str, sets: dict[str, set[str]], non_terminals: set[str]):
    print(f"\n--- Conjuntos {name} ---")
    for nt in sorted(list(non_terminals)):
        s = sets.get(nt, set())
        # Formatear la salida correctamente
        s_list = sorted(list(s))
        print(f"{name}({nt}) = {{ {', '.join(s_list)} }}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo_gramatica.txt>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    print(f"Leyendo gramática desde: {file_path}")
    
    # 1. Pipeline - Lector
    lines = read_grammar(file_path)
    
    # 2. Pipeline - Parser
    grammar = parse_grammar(lines)
    print("\n[Gramática Parseada Exitosamente]")
    validate_grammar(grammar)
    grammar.display()
    
    # 3. Pipeline - Algoritmo FIRST
    first_sets = compute_first(grammar)
    display_sets("FIRST", first_sets, grammar.non_terminals)
    
    # 4. Pipeline - Algoritmo FOLLOW
    follow_sets = compute_follow(grammar, first_sets)
    display_sets("FOLLOW", follow_sets, grammar.non_terminals)

if __name__ == '__main__':
    main()
