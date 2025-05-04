import streamlit as st
import matplotlib.pyplot as plt
import tempfile
import os
try:
    from core.cnf_utils import parse_dimacs
    from core.valenz_solver import ValenzDriftSolver
    from core.valence_resonance import valence_resonance
    from core.drift_semantic import semantic_drift
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from core.cnf_utils import parse_dimacs
    from core.valenz_solver import ValenzDriftSolver
    from core.valence_resonance import valence_resonance
    from core.drift_semantic import semantic_drift

st.title("Z-System SAT Simulation Tool")

uploaded_file = st.file_uploader("CNF-Datei hochladen (.cnf)", type=["cnf"])
batch_files = st.file_uploader("Batch: Mehrere CNF-Dateien hochladen", type=["cnf"], accept_multiple_files=True)
max_iter = st.number_input("Max Iterationen", 1000, 10000000, 100000)
p_local = st.slider("Lokale Mutationsrate (p_local)", 0.0, 1.0, 0.5)
seed = st.number_input("Seed (optional)", value=42)

# Einzeldatei-Modus
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cnf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    n_vars, n_clauses, clauses = parse_dimacs(tmp_path)
    os.unlink(tmp_path)
    st.write(f"Instanz geladen: **{n_vars} Variablen**, **{n_clauses} Klauseln**")

    if st.button("Simulation starten"):
        solver = ValenzDriftSolver(
            cnf=clauses,
            valence_fn=valence_resonance,
            drift_fn=semantic_drift,
            max_iter=max_iter,
            p_local=p_local,
            seed=seed
        )
        valence_trace = []
        import time
        t0 = time.perf_counter()
        assignment, best_val, steps, trace = solver.solve(valence_trace=valence_trace)
        runtime = time.perf_counter() - t0

        st.success(f"Fertig! Beste Valenz: {best_val:.4f}, Laufzeit: {runtime:.3f}s, Schritte: {steps}")
        st.write("Assignment (gekürzt):", assignment[:min(20, len(assignment))], "...")

        # Plot Valenzverlauf
        fig, ax = plt.subplots()
        ax.plot(valence_trace)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Valenz")
        ax.set_title("Valenzverlauf")
        st.pyplot(fig)

# Batch-Modus
if batch_files:
    st.info(f"{len(batch_files)} Dateien für Batch ausgewählt.")
    batch_name = st.text_input("Testlauf-Name (optional, für Dateinamen und Tabelle)", value="")
    if st.button("Batch-Run starten"):
        import time
        import pandas as pd
        from datetime import datetime
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = batch_name.strip().replace(" ", "_") or "batch"
        result_file = f"results/{safe_name}_{batch_id}.csv"
        for idx, file in enumerate(batch_files):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cnf") as tmp_file:
                tmp_file.write(file.read())
                tmp_path = tmp_file.name
            try:
                n_vars, n_clauses, clauses = parse_dimacs(tmp_path)
            finally:
                os.unlink(tmp_path)
            solver = ValenzDriftSolver(
                cnf=clauses,
                valence_fn=valence_resonance,
                drift_fn=semantic_drift,
                max_iter=max_iter,
                p_local=p_local,
                seed=seed
            )
            valence_trace = []
            t0 = time.perf_counter()
            assignment, best_val, steps, trace = solver.solve(valence_trace=valence_trace)
            runtime = time.perf_counter() - t0
            solved = best_val == 1.0
            results.append({
                "Testlauf": batch_name if batch_name else safe_name,
                "Datei": file.name,
                "Variablen": n_vars,
                "Klauseln": n_clauses,
                "Valenz": best_val,
                "Schritte": steps,
                "Laufzeit [s]": runtime,
                "Gelöst": solved
            })
            progress_bar.progress((idx + 1) / len(batch_files))
            status_text.text(f"{idx+1}/{len(batch_files)} Instanzen abgeschlossen...")
        progress_bar.empty()
        status_text.text(f"Batch abgeschlossen! Ergebnisse gespeichert unter: {result_file}")
        df = pd.DataFrame(results)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        # Automatisches Speichern im Backend
        os.makedirs("results", exist_ok=True)
        with open(result_file, "wb") as f:
            f.write(csv)
        st.success(f"Batch-Ergebnisse wurden automatisch gespeichert: {result_file}")
        st.download_button("Ergebnisse als CSV herunterladen", csv, "batch_results.csv", "text/csv")
