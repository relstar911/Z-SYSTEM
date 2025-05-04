# Resonanzbasierte Valenzfunktion für das ⦲SYSTEM-Toolkit
from typing import List, Sequence, Tuple

Boolean = bool
Literal = Tuple[int, bool]
Clause = Sequence[Literal]
CNF = List[Clause]
Assignment = List[Boolean]

def valence_resonance(cnf: CNF, assignment: Assignment) -> float:
    """Fraction of clauses satisfied (resonanzbasierte Valenz)."""
    sat = sum(any(assignment[v] if pol else not assignment[v] for v, pol in cl) for cl in cnf)
    return sat / len(cnf) if cnf else 0.0
