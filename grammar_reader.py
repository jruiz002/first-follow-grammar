def read_grammar(file_path: str) -> list[str]:
    """
    Lee un archivo de gramática y devuelve una lista de líneas limpias,
    eliminando comentarios y líneas en blanco.
    """
    cleaned_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Eliminar espacios en blanco alrededor
            line = line.strip()
            
            # Ignorar líneas vacías y comentarios (líneas que empiezan con #)
            if line and not line.startswith('#'):
                cleaned_lines.append(line)
                
    return cleaned_lines
