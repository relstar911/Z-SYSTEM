# Semantische Driftfunktion für das ⦲SYSTEM-Toolkit
import random
from typing import List, Sequence, Tuple

Boolean = bool
Literal = Tuple[int, bool]
Clause = Sequence[Literal]
CNF = List[Clause]
Assignment = List[Boolean]

def semantic_drift(assignment: Assignment, cnf: CNF, val: float) -> Assignment:
    """Flip k variables proportional to (1 - val)."""
    k = max(1, int(len(assignment) * (1.0 - val) * 0.1))
    idxs = random.sample(range(len(assignment)), k)
    for idx in idxs:
        assignment[idx] = not assignment[idx]
    return assignment
