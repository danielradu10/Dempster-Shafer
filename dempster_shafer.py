from itertools import combinations, permutations

class Hypotheses:
    def __init__(self, parties):
        self.parties = parties

    # Functie pentru generarea combinatiei de ipoteze
    def generate_combinations(self):
        all_combinations = []
        for party in self.parties:
            all_combinations.append((party,))
        # for perm in permutations(self.parties, 2):
        #     all_combinations.append(perm)
        print("Generated hypotheses (combinations of size 1 and 2):")
        for comb in all_combinations:
            print(f"Combinatia {comb}")
        return all_combinations

    # Functie pentru generarea tuturor submultimilor cu mase
    def generate_all_subsets_with_masses(self, sources):
        all_combinations = {}  # Dictionar pentru combinatii cu mase
        for source in sources:
            for subset, mass in source.items():
                if len(subset) > 1:  # Luam doar combinatiile de dimensiune 2 sau mai mult
                    combs = combinations(subset, 2)
                    for comb in combs:
                        comb_tuple = tuple(comb)
                        if comb_tuple not in all_combinations:
                            all_combinations[comb_tuple] = 0
                        all_combinations[comb_tuple] += mass  # Adunam masele
        print("Filtered combinations (only size 2 combinations):")
        for comb, mass in all_combinations.items():
            print(f"Combinatia {comb} are masa {mass:.4f}")  # Afisam combinatiile filtrate
        return all_combinations

# Clasa pentru calculul combinat al maselor in Dempster-Shafer
class ComputeDempsterShafer:
    def __init__(self):
        self.combined_masses = {}  # Mase combinate
        self.conflict = 0  # Conflictele dintre ipoteze

    # Functie pentru calculul intersectiei dintre doua ipoteze
    def compute_intersection(self, h1, h2):
        intersection = tuple(sorted(set(h1) & set(h2)))  # Intersectia a doua ipoteze
        return intersection if len(intersection) > 0 else None  # Daca intersectia nu este goala, o returnam

    # Functie pentru actualizarea maselor combinate
    def update_combined_masses(self, m1, m2, hypotheses):
        self.combined_masses = {h: 0 for h in hypotheses}  # Initializam masele combinate
        self.conflict = 0  # Resetam conflictul
        for h1, m1_val in m1.items():
            for h2, m2_val in m2.items():
                intersection = self.compute_intersection(h1, h2)
                if intersection:  # Daca exista intersectie
                    if intersection not in self.combined_masses:
                        self.combined_masses[intersection] = 0
                    self.combined_masses[intersection] += m1_val * m2_val  # Adunam masele pentru intersectie
                else:
                    self.conflict += m1_val * m2_val  # Adunam conflictul daca nu exista intersectie

    # Functie pentru normalizarea maselor combinate
    def normalize_combined_masses(self):
        normalization_factor = 1 - self.conflict  # Factor de normalizare
        if normalization_factor <= 0:
            print("Conflict este prea mare; nu este posibila o combinatie semnificativa.")  # Verificam daca conflictul e prea mare
            return
        for h in self.combined_masses:
            self.combined_masses[h] /= normalization_factor  # Normalizam masele

    # Functie pentru calculul maselor combinate
    def calculate_combined_masses(self, m1, m2, hypotheses):
        self.update_combined_masses(m1, m2, hypotheses)  # Actualizam masele combinate
        self.normalize_combined_masses()  # Normalizam masele
        return self.combined_masses

    # Functie pentru calculul credintei si plauzibilitatii
    def calculate_belief_and_plausibility(self, combined_masses, hypotheses):
        belief = {h: 0 for h in hypotheses}  # Credinta pentru fiecare ipoteza
        plausibility = {h: 0 for h in hypotheses}  # Plauzibilitatea pentru fiecare ipoteza
        for h in hypotheses:
            belief[h] = 0
            for sub_h, mass in combined_masses.items():
                if set(sub_h).issubset(set(h)):  # Verificam daca sub-ipoteza este inclusa in ipoteza
                    belief[h] += mass  # Adunam masa pentru credinta
            plausibility[h] = 0
            for sub_h, mass in combined_masses.items():
                if set(sub_h) & set(h):  # Verificam daca sub-ipoteza se intersecteaza cu ipoteza
                    plausibility[h] += mass  # Adunam masa pentru plauzibilitate
        return belief, plausibility

# Clasa principala pentru executarea algoritmului Dempster-Shafer
class DempsterShaferEngine:
    def __init__(self, parties, source1, source2, hypotheses=None):
        self.parties = parties  # Partile implicate
        if hypotheses is not None:
            self.hypotheses = hypotheses  # Ipotezele sunt date ca parametru
            self.source1 = source1  # Sursele pentru primul set de ipoteze
            self.source2 = source2  # Sursele pentru al doilea set de ipoteze
        else:
            self.hypotheses = Hypotheses(parties).generate_combinations()  # Generam combinatiile de ipoteze
            self.source1 = Hypotheses(parties).generate_all_subsets_with_masses([source1])  # Generam submultimi cu mase pentru sursa 1
            self.source2 = Hypotheses(parties).generate_all_subsets_with_masses([source2])  # Generam submultimi cu mase pentru sursa 2
        self.compute_dempster_shafer = ComputeDempsterShafer()  # Instantiem obiectul care calculeaza Dempster-Shafer

    # Functie pentru rularea procesului
    def run(self):
        combined_masses = self.compute_dempster_shafer.calculate_combined_masses(self.source1, self.source2,
                                                                                 self.hypotheses if isinstance(self.hypotheses, list) else self.hypotheses.keys())
        belief, plausibility = self.compute_dempster_shafer.calculate_belief_and_plausibility(combined_masses,
                                                                                              self.hypotheses if isinstance(self.hypotheses, list) else self.hypotheses.keys())
        self.print_results(combined_masses, belief, plausibility)

    # Functie pentru afisarea rezultatelor
    def print_results(self, combined_masses, belief, plausibility):
        print("\nCombined and normalized masses:")
        for h, mass in combined_masses.items():
            print(f"{h}: {mass:.4f}")
        print("\nBelief and Plausibility:")
        for h in belief:
            print(f"{h}: Belief = {belief[h]:.4f}, Plausibility = {plausibility[h]:.4f}")

# Codul principal
if __name__ == "__main__":
    print("Problema 1-Alegeri\n")
    parties = ["A", "B", "C"]
    source1 = {
        ("A", "B", "C"): 0.5,
        ("B",): 0.3,
        ("A", "C"): 0.3
    }
    source2 = {
        ("C", "A", "B"): 0.2,
        ("B", "A", "C"): 0.1,
        ("C", "A"): 0.1
    }
    engine = DempsterShaferEngine(parties, source1, source2)
    engine.run()

    print("\nProblema 2-Covid vs gripa\n")
    H = ('C', 'G', 'A', 'N')
    m1 = {
        ('C', 'G'): 0.6,
        ('A',): 0.1,
        ('C', 'G', 'A', 'N'): 0.3
    }
    m2 = {
        ('C',): 0.7,
        ('G', 'A'): 0.2,
        ('C', 'G', 'A', 'N'): 0.1
    }
    hypotheses = [
        ('C',),
        ('G',),
        ('A',),
        ('C', 'G'),
        ('C', 'G', 'A', 'N')
    ]
    engine = DempsterShaferEngine(H, m1, m2, hypotheses)
    engine.run()
