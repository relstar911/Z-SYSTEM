"""
run_batch.py – Systematische Experimente mit dem ValenzDriftSolver
==================================================================
Starte viele Instanzen mit unterschiedlichen Parametern (n, m, Seed) und speichere die Ergebnisse als CSV.

Usage:
  python -m runners.run_batch --n-range 50 100 10 --runs 5 --max-iter 50000 --outfile results.csv

Optionen:
  --n-range START STOP STEP : Variablenzahl von START bis STOP (exkl.) in STEP-Schritten
  --runs N                 : Anzahl Wiederholungen pro Setting (verschiedene Seeds)
  --max-iter K             : Iterationsbudget pro Lauf
  --outfile PATH           : Ergebnis-CSV
  --clauses-per-var R      : Klausel/Variablen-Verhältnis (default: 4.3)
"""
import argparse
import csv
import random
from pathlib import Path
from time import perf_counter
from core.valenz_solver import ValenzDriftSolver
from core.valence_resonance import valence_resonance
from core.drift_semantic import semantic_drift

def gen_random_cnf(n_vars, m_clauses, seed=None):
    if seed is not None:
        random.seed(seed)
    hidden = [random.choice([False, True]) for _ in range(n_vars)]
    cnf = []
    for _ in range(m_clauses):
        triple = random.sample(range(n_vars), 3)
        clause = []
        satisfied = False
        for v in triple:
            pol = random.choice([False, True])
            clause.append((v, pol))
            satisfied |= (hidden[v] and pol) or (not hidden[v] and not pol)
        if not satisfied:
            v0, pol0 = clause[0]
            clause[0] = (v0, not pol0)
        cnf.append(clause)
    return cnf

def parse_args():
    p = argparse.ArgumentParser(description="Batch-Experimente mit dem ValenzDriftSolver")
    p.add_argument('--n-range', nargs=3, type=int, metavar=('START','STOP','STEP'), required=True)
    p.add_argument('--runs', type=int, default=3, help='Wiederholungen pro Setting (verschiedene Seeds)')
    p.add_argument('--max-iter', type=int, default=50000, help='Iterationsbudget pro Lauf')
    p.add_argument('--outfile', type=str, required=True, help='Pfad für Ergebnis-CSV')
    p.add_argument('--clauses-per-var', type=float, default=4.3, help='Klausel/Variablen-Verhältnis')
    return p.parse_args()

def main():
    args = parse_args()
    n_start, n_stop, n_step = args.n_range
    with open(args.outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['n','m','seed','solved','best_valence','steps','runtime_sec'])
        for n in range(n_start, n_stop, n_step):
            m = int(args.clauses_per_var * n)
            for run in range(args.runs):
                seed = random.randint(1, 1_000_000_000)
                cnf = gen_random_cnf(n, m, seed=seed)
                solver = ValenzDriftSolver(
                    cnf=cnf,
                    valence_fn=valence_resonance,
                    drift_fn=semantic_drift,
                    max_iter=args.max_iter,
                    seed=seed
                )
                t0 = perf_counter()
                assignment, best_val, steps, _ = solver.solve()
                runtime = perf_counter() - t0
                solved = best_val == 1.0
                writer.writerow([n, m, seed, solved, best_val, steps, runtime])
                f.flush()
                print(f"n={n} m={m} seed={seed} solved={solved} valence={best_val:.3f} steps={steps} time={runtime:.2f}s")

if __name__ == "__main__":
    main()
