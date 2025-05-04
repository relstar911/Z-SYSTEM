"""
run_batch_dimacs.py – Batch-Auswertung für alle DIMACS/SATLIB-Instanzen in einem Ordner
======================================================================================
Beispielaufruf:
  python -m runners.run_batch_dimacs --indir data/ai/hoos/Shortcuts/UF250.1065.100 --max-iter 500000 --outfile results_dimacs.csv --plotdir plots/

Optionen:
  --indir DIR       : Verzeichnis mit .cnf-Dateien
  --max-iter K      : Iterationsbudget pro Instanz
  --outfile PATH    : Ergebnis-CSV
  --plotdir DIR     : (optional) speichert für jede Instanz einen Plot (PNG)
"""
import argparse
import csv
import os
from pathlib import Path
from time import perf_counter
from core.valenz_solver import ValenzDriftSolver
from core.valence_resonance import valence_resonance
from core.drift_semantic import semantic_drift

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

def main():
    parser = argparse.ArgumentParser(description="Batch-Run für alle .cnf-Dateien in einem Ordner")
    parser.add_argument('--indir', type=str, required=True, help='Ordner mit .cnf-Dateien')
    parser.add_argument('--max-iter', type=int, default=500_000, help='Iterationsbudget pro Instanz')
    parser.add_argument('--outfile', type=str, required=True, help='Pfad für Ergebnis-CSV')
    parser.add_argument('--plotdir', type=str, default=None, help='Ordner für PNG-Plots')
    args = parser.parse_args()

    indir = Path(args.indir)
    cnf_files = sorted([p for p in indir.glob('*.cnf')])
    if args.plotdir:
        plotdir = Path(args.plotdir)
        plotdir.mkdir(parents=True, exist_ok=True)
    else:
        plotdir = None

    with open(args.outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename','n','m','solved','best_valence','steps','runtime_sec'])
        for cnf_path in cnf_files:
            cnf = read_dimacs(cnf_path)
            n = max((v for cl in cnf for v,_ in cl), default=-1) + 1
            m = len(cnf)
            solver = ValenzDriftSolver(
                cnf=cnf,
                valence_fn=valence_resonance,
                drift_fn=semantic_drift,
                max_iter=args.max_iter
            )
            valence_trace = []
            t0 = perf_counter()
            assignment, best_val, steps, trace = solver.solve(valence_trace=valence_trace)
            runtime = perf_counter() - t0
            solved = best_val == 1.0
            writer.writerow([cnf_path.name, n, m, solved, best_val, steps, runtime])
            f.flush()
            print(f"{cnf_path.name}: solved={solved} valence={best_val:.3f} steps={steps} time={runtime:.2f}s")
            if plotdir is not None:
                try:
                    import matplotlib.pyplot as plt
                    plt.figure(figsize=(8,4))
                    plt.plot(trace)
                    plt.xlabel('Step')
                    plt.ylabel('Best Valence')
                    plt.title(f'{cnf_path.name}')
                    plt.tight_layout()
                    plt.savefig(plotdir / (cnf_path.stem + '.png'))
                    plt.close()
                except ImportError:
                    print("matplotlib nicht installiert: kein Plot für", cnf_path.name)

if __name__ == "__main__":
    main()
