# Hilfsfunktionen zum Parsen und Erzeugen von CNF/SAT-Instanzen

def parse_dimacs(path):
    """Liest eine DIMACS-CNF-Datei ein und gibt Variablen- und Klauselanzahl sowie Klauseln (als Liste von Tupeln (var_idx, polarity)) zurück."""
    with open(path, 'r') as f:
        clauses = []
        n_vars = n_clauses = None
        for line in f:
            line = line.strip()
            if line == '' or line.startswith('c') or line.startswith('%'):
                continue
            if line.startswith('p'):
                _, _, n_vars, n_clauses = line.split()
                n_vars, n_clauses = int(n_vars), int(n_clauses)
            else:
                try:
                    ints = [int(x) for x in line.split() if x != '0']
                    if ints:
                        clause = []
                        for lit in ints:
                            var_idx = abs(lit) - 1
                            polarity = lit > 0
                            clause.append((var_idx, polarity))
                        clauses.append(clause)
                except ValueError:
                    continue  # Zeilen mit ungültigen Literalen überspringen
    return n_vars, n_clauses, clauses
