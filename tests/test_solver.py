from core.valenz_solver import ValenzDriftSolver

def test_solver_runs():
    solver = ValenzDriftSolver(n_vars=10, n_clauses=5, max_iter=100)
    result = solver.run()
    assert isinstance(result, dict)
