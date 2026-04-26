import Classes

def initialize_population(population_count, population_type, *args):
    population_table = []

    for i in range(population_count):
        if population_type == Classes.Removed:
            dead_on_arrival = args[0]
            print(dead_on_arrival)
            if dead_on_arrival:
                # --// We create a removed object with only a name
                population_table.append(population_type(dead_on_arrival, f"{population_type.__name__} #{i}"))
            else:
                # --// We create a removed object with a sus or infected
                pass
        else:
            population_table.append(population_type(f"{population_type.__name__} #{i}"))

    return population_table

def zombie_simulation(susceptible_count, infected_count, removed_count):
    total_participants = susceptible_count + infected_count + removed_count
    alive_population = susceptible_count + infected_count

    #susceptible = initialize_population(susceptible_count, Classes.Susceptible)
    #infected = initialize_population(infected_count, Classes.Infected)
    removed = initialize_population(removed_count, Classes.Removed, True)

    all_susceptibles_dead = False
    all_infected_dead = False

    return
    while alive_population <= 0:

        if not all_susceptibles_dead:
            if susceptible_count <= 0:
                all_susceptibles_dead = True

        if not all_infected_dead:
            if infected_count <= 0:
                all_infected_dead = True





zombie_simulation(0,0,1)





