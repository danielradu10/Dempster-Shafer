def dempster_shafer(m1, m2):
    K = 0
    for Y in m1:
        for Z in m2:
            if not set(Y).intersection(set(Z)):
                K += m1[Y] * m2[Z]

    if K == 1:
        raise ValueError("Conflict K is 1, combination not possible.")

    combined_masses = {}
    normalization_factor = 1 - K

    for Y in m1:
        for Z in m2:
            intersection = tuple(sorted(set(Y).intersection(set(Z))))
            if intersection:
                if intersection not in combined_masses:
                    combined_masses[intersection] = 0
                combined_masses[intersection] += m1[Y] * m2[Z]

    for subset in combined_masses:
        combined_masses[subset] /= normalization_factor

    return combined_masses

def calculate_belief_and_plausibility(combined_masses, hypotheses):
    belief = {}
    plausibility = {}

    for h in hypotheses:
        h_set = set(h)

        belief[h] = sum(m for subset, m in combined_masses.items() if set(subset).issubset(h_set))

        plausibility[h] = sum(m for subset, m in combined_masses.items() if set(subset).intersection(h_set))

    return belief, plausibility

if __name__ == "__main__":
    H = ('C', 'G', 'A', 'N')  # COVID, Gripa, Alta boala sau Nimic

    m1 = {
        ('C', 'G'): 0.6,
        ('A',): 0.1,
        H: 0.3
    }

    m2 = {
        ('C',): 0.7,
        ('G', 'A'): 0.2,
        H: 0.1
    }

    hypotheses = [
        ('C',),
        ('G',),
        ('A',),
        ('C', 'G'),
        ('C', 'G', 'A', 'N')
    ]

    combined_masses = dempster_shafer(m1, m2)

    belief, plausibility = calculate_belief_and_plausibility(combined_masses, hypotheses)
    intervals = {h: (belief[h], plausibility[h]) for h in hypotheses}

    for subset, mass in combined_masses.items():
        print(f"{subset}: {mass:.4f}")

    print("\nBelief:")
    for h, b in belief.items():
        print(f"{h}: {b:.4f}")

    print("\nPlausibility:")
    for h, p in plausibility.items():
        print(f"{h}: {p:.4f}")

    print("\nConfidence Intervals:")
    for h, (b, p) in intervals.items():
        print(f"{h}: [{b:.4f}, {p:.4f}]")

