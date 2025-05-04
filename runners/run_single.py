import argparse
import json
import random
import sys
from pathlib import Path
from time import perf_counter
from core.valenz_solver import ValenzDriftSolver
from core.valence_resonance import valence_resonance
from core.drift_semantic import semantic_drift

Boolean = bool
Literal = tuple[int, bool]
Clause = list[Literal]
CNF = list[Clause]
Assignment = list[Boolean]

def read_dimacs(path: Path) -> CNF:
    cnf: CNF = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            # Ignore comments and non-clause lines (c, p, %, etc.)
            if not line or not any(ch.isdigit() or ch == '-' for ch in line):
                continue
            if line[0] in ("c", "p", "%"):
                continue
            try:
                lits = [int(x) for x in line.split() if x != "0"]
            except ValueError:
                continue  # skip any malformed line
            clause: Clause = []
            for lit in lits:
                var_idx = abs(lit) - 1
                polarity = lit > 0
                clause.append((var_idx, polarity))
            if clause:
                cnf.append(clause)
    return cnf

def gen_random_cnf(n_vars: int, m_clauses: int | None = None) -> CNF:
    if m_clauses is None:
        m_clauses = int(4.3 * n_vars)
    hidden = [random.choice([False, True]) for _ in range(n_vars)]
    cnf: CNF = []
    for _ in range(m_clauses):
        triple = random.sample(range(n_vars), 3)
        clause: Clause = []
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

def parse_args(argv: list[str]):
    p = argparse.ArgumentParser(description="Solve CNF with Valenz‑Drift heuristic")
    p.add_argument("file", nargs="?", help="DIMACS CNF file")
    p.add_argument("--random", type=int, dest="rnd_n", metavar="N", help="generate random satisfiable 3‑SAT with N variables")
    p.add_argument("--clauses", type=int, metavar="M", help="override clause count when using --random")
    p.add_argument("--max-iter", type=int, default=100_000, help="max iterations (default: 100k)")
    p.add_argument("--json-out", metavar="PATH", help="write JSON result file")
    p.add_argument("--trace-out", metavar="PATH", help="write valence trace as JSON")
    p.add_argument("--plot", metavar="PATH", help="save valence trace plot as PNG")
    p.add_argument("--progress", action='store_true', help='Show progress bar during solving')
    return p.parse_args(argv)

def main(argv: list[str] | None = None):
    args = parse_args(argv or sys.argv[1:])
    if args.rnd_n:
        cnf = gen_random_cnf(args.rnd_n, args.clauses)
        instance_info = {"type": "random", "n": args.rnd_n, "m": len(cnf)}
    elif args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: file {path} not found", file=sys.stderr)
            sys.exit(1)
        cnf = read_dimacs(path)
        instance_info = {"type": "dimacs", "path": str(path), "m": len(cnf)}
    else:
        print("Error: must supply --random N or CNF FILE", file=sys.stderr)
        sys.exit(1)
    solver = ValenzDriftSolver(
        cnf=cnf,
        valence_fn=valence_resonance,
        drift_fn=semantic_drift,
        max_iter=args.max_iter,
    )
    valence_trace = []
    t0 = perf_counter()
    assignment, best_val, steps, trace = solver.solve(valence_trace=valence_trace, progress=args.progress)
    runtime = perf_counter() - t0
    result = {
        "instance": instance_info,
        "best_valence": best_val,
        "steps": steps,
        "runtime_sec": runtime,
        "solved": best_val == 1.0,
    }
    out_json = json.dumps(result, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(out_json)
    else:
        print(out_json)
    if args.trace_out:
        Path(args.trace_out).write_text(json.dumps(trace))
    if args.plot:
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8,4))
            plt.plot(trace)
            plt.xlabel('Step')
            plt.ylabel('Best Valence')
            plt.title('Valence Trace')
            plt.tight_layout()
            plt.savefig(args.plot)
            plt.close()
            print(f"Valence trace plot saved to {args.plot}")
        except ImportError:
            print("matplotlib not installed: cannot plot valence trace.")

if __name__ == "__main__":
    main()
