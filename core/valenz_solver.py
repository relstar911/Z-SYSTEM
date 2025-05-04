import random
from typing import Callable, List, Sequence, Tuple, Set

Boolean = bool
Literal = Tuple[int, bool]  # (var_idx, polarity)
Clause = Sequence[Literal]
CNF = List[Clause]
Assignment = List[Boolean]

def build_var_map(cnf: CNF) -> List[List[int]]:
    """Return mapping var_idx → clause indices that contain the variable."""
    n_vars = 1 + max(v for cl in cnf for v, _ in cl)
    mapping: List[List[int]] = [[] for _ in range(n_vars)]
    for idx, clause in enumerate(cnf):
        for var, _ in clause:
            mapping[var].append(idx)
    return mapping

def clause_is_sat(clause: Clause, assignment: Assignment) -> bool:
    return any(assignment[v] if pol else not assignment[v] for v, pol in clause)

class ValenzDriftSolver:
    """Valenz + Drift heuristic with incremental clause evaluation."""
    def __init__(self,
                 cnf: CNF,
                 valence_fn: Callable[[CNF, Assignment], float],
                 drift_fn: Callable[[Assignment, CNF, float], Assignment],
                 memory_fn: Callable[[dict, Assignment, float], None] = lambda mem, assign, v: None,
                 p_local: float = 0.5,
                 max_iter: int = 100_000,
                 seed: int = None):
        if seed is not None:
            random.seed(seed)
        self.cnf = cnf
        self.valence_fn = valence_fn
        self.drift_fn = drift_fn
        self.memory_fn = memory_fn
        self.p_local = p_local
        self.max_iter = max_iter
        self.var_map = build_var_map(cnf)
        self.n_vars = len(self.var_map)
        self.memory: dict = {"plateaus": [], "blacklist": set()}

    def _init_state(self) -> tuple[Assignment, Set[int]]:
        assignment = [random.choice([False, True]) for _ in range(self.n_vars)]
        unsat: Set[int] = {
            idx for idx, clause in enumerate(self.cnf) if not clause_is_sat(clause, assignment)
        }
        return assignment, unsat

    def solve(self, valence_trace: list = None, progress: bool = False) -> Tuple[Assignment, float, int, list]:
        assignment, unsat = self._init_state()
        best_val = self.valence_fn(self.cnf, assignment)
        best_assign = assignment.copy()
        trace = valence_trace if valence_trace is not None else None
        if trace is not None:
            trace.clear()
            trace.append(best_val)

        rng = range(self.max_iter)
        if progress:
            try:
                from tqdm import tqdm
                rng = tqdm(rng, desc="Solving", unit="step")
            except ImportError:
                pass

        for step in rng:
            if not unsat:
                if trace is not None:
                    trace.append(1.0)
                return assignment, 1.0, step, trace if trace is not None else []
            val = self.valence_fn(self.cnf, assignment)
            if val > best_val:
                best_val = val
                best_assign = assignment.copy()
            if trace is not None:
                trace.append(best_val)

            # Mutation: local drift (unsat clause) oder global/semantic drift
            if random.random() < self.p_local:
                clause_idx = random.choice(list(unsat))
                clause = self.cnf[clause_idx]
                var, _ = random.choice(clause)
                flip_idxs = [var]
            else:
                old_assign = assignment.copy()
                assignment = self.drift_fn(assignment, self.cnf, val)
                flip_idxs = [i for i, (a, b) in enumerate(zip(old_assign, assignment)) if a != b]

            # Inkrementelles Update der unsat-Klauseln
            for var in flip_idxs:
                for ci in self.var_map[var]:
                    was_sat = ci not in unsat
                    now_sat = clause_is_sat(self.cnf[ci], assignment)
                    if was_sat and not now_sat:
                        unsat.add(ci)
                    elif not was_sat and now_sat:
                        unsat.discard(ci)

            self.memory_fn(self.memory, assignment, val)

        if trace is not None:
            trace.append(best_val)
        return best_assign, best_val, self.max_iter, trace if trace is not None else []

