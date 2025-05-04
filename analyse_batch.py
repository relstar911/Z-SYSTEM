import pandas as pd
import sys

# Usage: python analyse_batch.py results.csv
# (oder passe den Dateinamen unten an)

def analyse(csv_path):
    df = pd.read_csv(csv_path)
    print("\n===== Batch-Auswertung =====\n")
    print(f"Anzahl Instanzen: {len(df)}")
    if 'solved' in df.columns:
        solved = df['solved'].sum()
        print(f"Erfolgreich gelöst: {solved}/{len(df)} ({100*solved/len(df):.1f}%)")
    if 'best_valence' in df.columns:
        print(f"Durchschnittliche Valenz: {df['best_valence'].mean():.4f}")
        print(f"Min/Max Valenz: {df['best_valence'].min():.4f} / {df['best_valence'].max():.4f}")
    if 'runtime_sec' in df.columns:
        print(f"Durchschnittliche Laufzeit: {df['runtime_sec'].mean()*1000:.3f} ms")
        print(f"Min/Max Laufzeit: {df['runtime_sec'].min()*1000:.3f} / {df['runtime_sec'].max()*1000:.3f} ms")
    if 'steps' in df.columns:
        print(f"Durchschnittliche Iterationen: {df['steps'].mean():.0f}")
        print(f"Min/Max Iterationen: {df['steps'].min()} / {df['steps'].max()}")
    print("\nTop 5 schnellste Lösungen:")
    if 'runtime_sec' in df.columns:
        print(df.sort_values('runtime_sec').head(5)[['n','m','seed','runtime_sec','solved']])
    print("\nTop 5 höchste Valenz:")
    if 'best_valence' in df.columns:
        print(df.sort_values('best_valence', ascending=False).head(5)[['n','m','seed','best_valence','solved']])
    print("\n===== Ende Auswertung =====\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyse_batch.py <results.csv>")
        sys.exit(1)
    analyse(sys.argv[1])
