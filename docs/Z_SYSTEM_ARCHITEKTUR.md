# ⦲SYSTEM Toolkit – Komponentenübersicht

Dieses Dokument beschreibt alle Kernkomponenten des Z-System Simulations-Toolkits für experimentelle SAT/Resonanz-Logik.

---

## 1. **core/** – Zentrale Algorithmen & Heuristiken

### **valenz_solver.py**
- Enthält den generischen, hochperformanten ValenzDriftSolver.
- Unterstützt:
  - Beliebige CNF-Instanzen (DIMACS-kompatibel oder generiert)
  - Frei wählbare Valenz-, Drift- und Memory-Funktionen (Plug-and-Play)
  - Inkrementelles Tracking unzufriedener Klauseln
  - Optionales Tracking des Valenzverlaufs
- API: `ValenzDriftSolver(cnf, valence_fn, drift_fn, memory_fn, ...)`

### **valence_resonance.py**
- Implementiert die Standard-Valenzfunktion (Resonanz, Anteil erfüllter Klauseln).
- Kann durch eigene Qualitätsfunktionen ersetzt werden.

### **drift_semantic.py**
- Implementiert die Standard-Driftfunktion (semantischer Flip proportional zu 1-Valenz).
- Kann durch beliebige Mutations-/Suchoperatoren ersetzt werden.

### **heuristics.py**
- (Optional) Weitere Heuristiken, z.B. Random Flip, Plateau-Strategien, Blacklisting.

---

## 2. **runners/** – Ausführungs- und Experimentier-Skripte

### **run_single.py**
- CLI-Tool zum Lösen einzelner CNF-Instanzen (Datei oder generiert).
- Optionen:
  - Maximale Iterationen
  - Valenzverlauf als Plot/JSON
  - Ergebnis-Export als JSON

### **run_batch.py**
- Batch-Runner für systematische Experimente mit generierten Instanzen (verschiedene n/m/Seeds).
- Exportiert Ergebnisse als CSV.

### **run_batch_dimacs.py**
- Batch-Runner für echte DIMACS/SATLIB-Instanzen in einem Ordner.
- Für jede Instanz: Ergebnis-CSV, optional Plots.
- Ermöglicht systematische Benchmark-Experimente.

---

## 3. **data/** – Instanzen & Inputdaten
- Beispiel-CNF-Dateien (DIMACS, SATLIB, eigene Generierung)
- Struktur: frei, empfohlen z.B. `data/example.cnf`, `data/ai/hoos/Shortcuts/UF250.1065.100/`

---

## 4. **tests/** – Unit-Tests
- Automatisierte Tests für Solver, Parser, Heuristiken.
- Beispiel: `test_solver.py` prüft, ob der Solver grundsätzlich läuft.

---

## 5. **gui/** – (optional) Interaktive Visualisierung
- Streamlit-App für Live-Experimente und Präsentation.
- Noch in Vorbereitung/Prototyp.

---

## 6. **requirements.txt & README.md**
- Abhängigkeiten (numpy, matplotlib, streamlit, python-sat, ...)
- Dokumentation, Quickstart, Beispiele

---

## **Kernprinzipien des ⦲SYSTEM-Toolkits**
- **Modularität:** Jede Komponente kann unabhängig erweitert/ersetzt werden.
- **Forschungstauglichkeit:** Batch- und Einzel-Experimente, CSV/Plot-Export, echte Benchmarks.
- **Plug-and-Play-Heuristiken:** Valenz, Drift, Memory als freie Parameter.
- **Reproduzierbarkeit:** Seed-Handling, vollständige Ergebnisprotokollierung.
- **Visualisierung:** Valenzverlauf, Plots, GUI (optional).

---

## **Erweiterungsideen**
- Heuristik-Plugin-System (CLI-Auswahl)
- Memory-Mechanismen, Plateau-Analyse
- Statistische Auswertung (Erfolgsrate, Mittelwertplots)
- Streamlit-GUI für interaktive Forschung

---

*Letzte Aktualisierung: 2025-05-04*
