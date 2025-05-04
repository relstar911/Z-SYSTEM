"""
run_batch_parallel.py – Batch-Runner mit Multi-Core-Parallelisierung für DIMACS/SATLIB-Instanzen
===============================================================================================
Beispielaufruf:
  python -m runners.run_batch_parallel --indir data/ai/hoos/Shortcuts/UF250.1065.100 --max-iter 1000000 --outfile results_parallel.csv --plotdir plots/ --n-jobs 8

Optionen:
  --indir DIR       : Verzeichnis mit .cnf-Dateien
  --max-iter K      : Iterationsbudget pro Instanz
  --outfile PATH    : Ergebnis-CSV
  --plotdir DIR     : (optional) speichert für jede Instanz einen Plot (PNG)
  --n-jobs N        : Anzahl paralleler Prozesse
"""
import argparse
import csv
import os
from pathlib import Path
from time import perf_counter
from core.valenz_solver import ValenzDriftSolver
from core.valence_resonance import valence_resonance
from core.drift_semantic import semantic_drift
import multiprocessing as mp

def read_dimacs(path: Path):
    cnf = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or not any(ch.isdigit() or ch == '-' for ch in line):
                continue
            if line[0] in ("c", "p", "%"):
                continue
            try:
                lits = [int(x) for x in line.split() if x != "0"]
            except ValueError:
                continue
            clause = []
            for lit in lits:
                var_idx = abs(lit) - 1
                polarity = lit > 0
                clause.append((var_idx, polarity))
            if clause:
                cnf.append(clause)
    return cnf

def run_instance(args):
    cnf_path, max_iter, plotdir = args
    cnf = read_dimacs(cnf_path)
    n = max((v for cl in cnf for v,_ in cl), default=-1) + 1
    m = len(cnf)
    solver = ValenzDriftSolver(
        cnf=cnf,
        valence_fn=valence_resonance,
        drift_fn=semantic_drift,
        max_iter=max_iter
    )
    t0 = perf_counter()
    assignment, best_val, steps, trace = solver.solve(valence_trace=[])
    runtime = perf_counter() - t0
    solved = best_val == 1.0
    # Plot speichern
    if plotdir is not None:
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')
            plt.figure(figsize=(8,4))
            plt.plot(trace)
            plt.xlabel('Step')
            plt.ylabel('Best Valence')
            plt.title(f'{cnf_path.name}')
            plt.tight_layout()
            plot_path = Path(plotdir) / (cnf_path.stem + '.png')
            plt.savefig(plot_path)
            plt.close()
        except ImportError:
            pass
    return (cnf_path.name, n, m, solved, best_val, steps, runtime)

def main():
    parser = argparse.ArgumentParser(description="Batch-Run mit Parallelisierung für .cnf-Dateien")
    parser.add_argument('--indir', type=str, required=True, help='Ordner mit .cnf-Dateien')
    parser.add_argument('--max-iter', type=int, default=500_000, help='Iterationsbudget pro Instanz')
    parser.add_argument('--outfile', type=str, required=True, help='Pfad für Ergebnis-CSV')
    parser.add_argument('--plotdir', type=str, default=None, help='Ordner für PNG-Plots')
    parser.add_argument('--n-jobs', type=int, default=4, help='Anzahl paralleler Prozesse')
    args = parser.parse_args()

    indir = Path(args.indir)
    cnf_files = sorted([p for p in indir.glob('*.cnf')])
    if args.plotdir:
        plotdir = Path(args.plotdir)
        plotdir.mkdir(parents=True, exist_ok=True)
    else:
        plotdir = None

    pool_args = [(p, args.max_iter, plotdir) for p in cnf_files]
    try:
        from tqdm import tqdm
    except ImportError:
        tqdm = None

    with mp.Pool(processes=args.n_jobs) as pool:
        if tqdm is not None:
            results = list(tqdm(pool.imap_unordered(run_instance, pool_args), total=len(pool_args), desc="Batch Progress"))
        else:
            results = list(pool.imap_unordered(run_instance, pool_args))

    with open(args.outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename','n','m','solved','best_valence','steps','runtime_sec'])
        for row in results:
            writer.writerow(row)
    print(f"Batch abgeschlossen. Ergebnisse in {args.outfile}")

if __name__ == "__main__":
    main()
