# Verschiedene Heuristiken und Strategien für das Z-System

def random_flip(state, n_vars):
    """Flippt zufällig eine Variable."""
    import numpy as np
    idx = np.random.randint(n_vars)
    state[idx] = 1 - state[idx]
    return state
