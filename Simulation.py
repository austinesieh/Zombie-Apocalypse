import Classes

def initialize_population(population_count, population_type, *args):
    population_table = []

    for i in range(population_count):
        if args:
            population_table.append(population_type(f"{population_type.__name__} {i}", args))
        else:
            population_table.append(population_type(f"{population_type.__name__} {i}"))

    return population_table

def zombie_simulation(susceptible_count, infected_count, removed_count):
    total_participants = susceptible_count + infected_count + removed_count
    alive_population = susceptible_count + infected_count

    susceptible = initialize_population(susceptible_count, Classes.Susceptible)
    infected = initialize_population(infected_count, Classes.Infected)
    removed = initialize_population(removed_count, Classes.Removed, "Was Already Dead", "Unknown")
    print(susceptible)
    print(infected)

zombie_simulation(5,5,0)





