# Z-System Simulations-Toolkit

Ein modulares Python-Toolkit für experimentelle Echtzeit-Simulationen von SAT-Problemen und resonanzbasierter Strukturlogik.

## Projektstruktur

```
zsystem_sim_tool/
│
├── core/                # Kernlogik & Algorithmen
│   ├── __init__.py
│   ├── valenz_solver.py
│   ├── cnf_utils.py
│   ├── heuristics.py
│   └── drift_semantic.py
│
├── runners/             # Kommandozeilen-Skripte & Batch-Runner
│   ├── run_single.py
│   ├── run_batch.py
│   ├── run_batch_parallel.py
│   └── run_batch_dimacs.py
│
├── gui/                 # Interaktive Oberfläche (z.B. Streamlit)
│   └── app.py
│
├── data/                # Beispielinstanzen, Inputdaten
│   └── example.cnf
│
├── plots/               # Automatisch generierte Plots (Batch-Run)
│
├── tests/               # Unit- und Integrationstests
│   └── test_solver.py
│
├── analyse_batch.py     # Automatische Auswertung von Batch-Ergebnissen
├── requirements.txt     # Abhängigkeiten
├── README.md            # Dokumentation & Quickstart
└── .gitignore
```

## Quickstart

```bash
git clone <repo-url>
cd zsystem_sim_tool
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
pip install -r requirements.txt
```

## Einzelinstanz lösen (CLI)

```bash
python -m runners.run_single <pfad/zur/instanz.cnf> --max-iter 1000000 --plot valenz.png --progress
```
- Mit `--progress` wird ein Fortschrittsbalken angezeigt.
- Mit `--plot` wird die Valenzentwicklung als PNG gespeichert.

## Batch-Processing (Parallel)

```bash
python -m runners.run_batch_parallel --indir <ordner_mit_cnf> --max-iter 1000000 --outfile results.csv --plotdir plots
```
- **Alle CNF-Dateien im angegebenen Ordner werden parallel gelöst.**
- Fortschrittsbalken zeigt Gesamtfortschritt.
- Ergebnisse landen in `results.csv` (CSV-Format)
- Optional: Plots für jede Instanz in `plots/`
- `--n-jobs <n>` für parallele Prozesse (Standard: alle Kerne)

## Automatische Auswertung

Nach einem Batch-Run kannst du die Ergebnisse automatisch auswerten:

```bash
python analyse_batch.py results.csv
```
- Gibt Erfolgsrate, durchschnittliche Valenz, Laufzeit, Top-Lösungen usw. im Terminal aus.
- Passt sich automatisch an die Spaltenstruktur der Batch-CSV an.

## Hinweise zur Ergebnisinterpretation
- **Valenz = 1.0** bedeutet: Instanz vollständig gelöst.
- **steps** gibt die Anzahl Iterationen an (bei 0 ggf. sofortige Lösung oder Fehler im Logging).
- **runtime_sec** ist die benötigte Zeit pro Instanz (in Sekunden, meist sehr klein).
- Plots im Ordner `plots/` zeigen die Valenzentwicklung pro Instanz.

## Abhängigkeiten
- numpy
- matplotlib
- streamlit
- python-sat
- tqdm (für Fortschrittsbalken)
- pandas (für Auswertung)

Alle Abhängigkeiten sind in `requirements.txt` gelistet. Für die Auswertung ggf. `pip install pandas tqdm` nachinstallieren.

---

**Fragen, Wünsche oder Erweiterungen? Einfach im Issue-Tracker oder direkt im Code ergänzen!**
