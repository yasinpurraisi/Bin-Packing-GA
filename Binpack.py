import random

# -------------------------------
# Problem Setup
# -------------------------------
ITEM_SIZES = [4, 8, 1, 4, 2, 1, 7, 3, 6, 5, 2, 9, 3, 2]
BIN_CAPACITY = 10
POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.05

# -------------------------------
# Fitness Function
# -------------------------------
def fitness(chromosome, item_sizes, bin_capacity):
    bins = {}
    overflow_penalty = 1000

    for i, bin_idx in enumerate(chromosome):
        bins.setdefault(bin_idx, []).append(item_sizes[i])

    total_bins_used = len([b for b in bins.values() if sum(b) > 0])
    overflow = sum(max(0, sum(items) - bin_capacity) for items in bins.values())
    
    return - (total_bins_used + overflow * overflow_penalty)

# -------------------------------
# Initialization
# -------------------------------
def create_chromosome(num_items, max_bins):
    return [random.randint(0, max_bins - 1) for _ in range(num_items)]

def initial_population(pop_size, num_items, max_bins):
    return [create_chromosome(num_items, max_bins) for _ in range(pop_size)]

# -------------------------------
# Selection
# -------------------------------
def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1], reverse=True)
    return selected[0][0]

# -------------------------------
# Crossover
# -------------------------------
def crossover(parent1, parent2):
    return [parent1[i] if random.random() < 0.5 else parent2[i] for i in range(len(parent1))]

# -------------------------------
# Mutation
# -------------------------------
def mutate(chromosome, mutation_rate, max_bins):
    return [
        random.randint(0, max_bins - 1) if random.random() < mutation_rate else gene
        for gene in chromosome
    ]

# -------------------------------
# GA Main Loop
# -------------------------------
def genetic_algorithm(item_sizes, bin_capacity, population_size, generations):
    num_items = len(item_sizes)
    max_bins = num_items  # worst case: each item in its own bin
    population = initial_population(population_size, num_items, max_bins)

    for gen in range(generations):
        fitnesses = [fitness(ch, item_sizes, bin_capacity) for ch in population]
        next_gen = []

        # Elitism: keep the best
        best = population[fitnesses.index(max(fitnesses))]
        next_gen.append(best)

        while len(next_gen) < population_size:
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, MUTATION_RATE, max_bins)
            next_gen.append(child)

        population = next_gen

        if gen % 50 == 0:
            print(f"Generation {gen} - Best fitness: {max(fitnesses)}")

    # Final result
    final_fitnesses = [fitness(ch, item_sizes, bin_capacity) for ch in population]
    best_solution = population[final_fitnesses.index(max(final_fitnesses))]

    return best_solution

# -------------------------------
# Run and Display Result
# -------------------------------
if __name__ == "__main__":
    best = genetic_algorithm(ITEM_SIZES, BIN_CAPACITY, POPULATION_SIZE, GENERATIONS)

    # Group items by bin
    packed_bins = {}
    for i, bin_idx in enumerate(best):
        packed_bins.setdefault(bin_idx, []).append(ITEM_SIZES[i])

    # Clean empty bins and sort by bin index
    final_bins = {k: v for k, v in sorted(packed_bins.items()) if sum(v) > 0}

    print("\n Final Bin Packing Solution:")
    for bin_id, items in final_bins.items():
        print(f"Bin {bin_id}: {items} (Total: {sum(items)}/{BIN_CAPACITY})")

    print(f"\nTotal bins used: {len(final_bins)}")
