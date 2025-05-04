# ⦲SYSTEM Glossar – Neue Begriffe, Methoden und Z-Definitionen

Dieses Glossar fasst alle zentralen Begriffe, Methoden und Konzepte des ⦲SYSTEM-Toolkits zusammen, die klassische „0“-Logik ersetzen oder erweitern.

---

## **Allgemeine Z-Definitionen und Begriffe**

- **⦲SYSTEM / Z-System**  
  Ein Framework für resonanzbasierte, dynamische und heuristische Logik, das klassische boolesche „0/1“-Logik durch flexible, kontextabhängige Strukturen ersetzt.

- **Valenz**  
  Maß für die Qualität einer Belegung (Assignment); typischerweise Anteil erfüllter Klauseln (zwischen 0 und 1). Ersetzt die klassische „0/1“-Bewertung durch ein kontinuierliches Resonanzmaß.

- **Drift**  
  Mutations- oder Suchoperator, der gezielte oder zufällige Änderungen an der aktuellen Belegung vornimmt. Ersetzt deterministische Schrittfolgen durch stochastische, adaptive Exploration.

- **Memory (Gedächtnis)**  
  Speichermechanismus für Plateaus, Blacklists, Drive-States etc., der die Suchdynamik beeinflusst und klassische „Vergessen“-Mechanismen ersetzt.

- **Resonanz**  
  Überlagerung und Wechselwirkung von lokalen und globalen Qualitätsmaßen (Valenz), die das Systemverhalten steuern.

- **Plateau**  
  Zustand, in dem die Valenz über viele Schritte konstant bleibt; wird im ⦲SYSTEM explizit erkannt und für Memory/Drift genutzt.

- **Assignment**  
  Eine Belegung aller Variablen; im ⦲SYSTEM nicht nur als „Wahr/Falsch“, sondern als dynamischer Zustand mit Resonanz und Drift.

- **CNF (Conjunctive Normal Form)**  
  Standardrepräsentation für SAT-Probleme; im ⦲SYSTEM als universelles Inputformat.

---

## **Neue Methoden und Operatoren (statt klassisch 0/1)**

- **valence_resonance(cnf, assignment)**  
  Berechnet die aktuelle Valenz als Resonanzmaß (Anteil erfüllter Klauseln, ggf. erweitert um Gewichtungen, Soft-Constraints etc.).

- **semantic_drift(assignment, cnf, val)**  
  Führt eine Mutation (Flip) an einer oder mehreren Variablen proportional zur „Unzufriedenheit“ (1-Valenz) durch. Ersetzt starre Flip-Strategien durch adaptive Drift.

- **build_var_map(cnf)**  
  Erstellt eine Abbildung von Variablen auf die Klauseln, in denen sie vorkommen – Grundlage für inkrementelle Updates.

- **clause_is_sat(clause, assignment)**  
  Prüft, ob eine Klausel unter der aktuellen Belegung erfüllt ist (Resonanzprüfung).

- **ValenzDriftSolver.solve(valence_trace=None)**  
  Führt die Hauptsimulation mit Valenz-, Drift- und Memory-Operatoren aus. Optionales Tracking des Valenzverlaufs.

- **Plateau-/Memory-Mechanismen**  
  Erweiterbar: Blacklisting, Plateauerkennung, adaptive Driftintensität.

---

## **Erweiterte Z-Definitionen im Kontext des Toolkits**

- **Z-Assignment**  
  Eine Belegung, die nicht nur „gültig“ oder „ungültig“ ist, sondern ein Resonanzspektrum aufweist.

- **Z-Valenz**  
  Ein kontinuierliches Maß für die „Kohärenz“ einer Struktur im ⦲SYSTEM, nicht nur „0/1“.

- **Z-Drift**  
  Jede Mutation, die nicht deterministisch, sondern adaptiv, stochastisch oder memory-gesteuert erfolgt.

- **Z-Memory**  
  Jeglicher Mechanismus, der vergangene Zustände, Plateaus oder Blacklists speichert und die Suche beeinflusst.

---

## **Beispiel für die Ablösung von „0“ durch Z-Operatoren**

| Klassisch (0/1)        | ⦲SYSTEM (Z)                                     |
|------------------------|------------------------------------------------|
| Lösung gefunden (1)    | Valenz = 1.0 (Resonanzmaximum)                 |
| Nicht erfüllbar (0)    | Valenz < 1.0, Drift/Memory suchen weiter       |
| Zufälliger Flip        | Semantic Drift, adaptiv nach Valenz            |
| Keine Änderung         | Plateau, Memory-Mechanismus aktiviert          |
| Statischer Score       | Dynamischer Valenzverlauf (Trace)              |

---

*Letzte Aktualisierung: 2025-05-04*
