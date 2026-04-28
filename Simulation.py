import time
import Classes
import Plot_Module
import UI_Module as UI
from Classes import WORLD_SIZE

WORLD_SIZE = {'WIDTH': 1000, 'HEIGHT': 1000}
canvas, window = UI.SETUP_WORLD(WORLD_SIZE['WIDTH'], WORLD_SIZE['HEIGHT'])

def initialize_population(population_count, population_type, *args):
    population_table = []

    for i in range(population_count):
        if population_type == Classes.Removed:
            # --// Because removed objects can be instantiated two ways we use *args
            dead_on_arrival = args[0]
            if dead_on_arrival:
                # --// We create a removed object with only a name
                population_table.append(population_type(dead_on_arrival, f"{population_type.__name__} #{i}"))
            else:
                # --// We create a removed object with a sus or infected
                pass
        else:
            population_table.append(population_type(f"{population_type.__name__} #{i}", canvas,
            population_type == Classes.Susceptible and "white" or "green"))

    return population_table

def zombie_simulation(susceptible_count, infected_count, removed_count):
    total_participants = susceptible_count + infected_count + removed_count
    alive_population = susceptible_count + infected_count

    susceptible = initialize_population(susceptible_count, Classes.Susceptible)
    infected = initialize_population(infected_count, Classes.Infected)
    removed = initialize_population(removed_count, Classes.Removed, True)

    all_susceptibles_dead = False
    all_infected_dead = False

    iteration = 0
    # --// Both get the iteration when a whole population is wiped out
    SUSCPETIBLES_WIPED_OUT = None
    INFECTEDS_WIPED_OUT = None

    while alive_population > 0:
        iteration += 1

        UI.CLEAR_LABELS(canvas, Classes.text_labels)
        interaction_occured = False

        if not all_susceptibles_dead:
            if susceptible_count <= 0:
                # --// Show on chart a line when all susceptibles are dead
                SUSCPETIBLES_WIPED_OUT = iteration
                all_susceptibles_dead = True

        if not all_infected_dead:
            if infected_count <= 0:
                INFECTEDS_WIPED_OUT = iteration
                # --// Show on chart a line when all infected are dead
                all_infected_dead = True

        # --// Make all susceptible objects act
        for susceptible_obj in susceptible:
            susceptible_obj.act(infected, canvas)

            object_is_alive = susceptible_obj.checkalive(canvas)
            if not object_is_alive:
                alive_population -= 1
                susceptible_count -= 1
                removed_count += 1

                dead_susceptible = Classes.Removed(False, susceptible_obj)
                susceptible.remove(susceptible_obj)
                removed.append(dead_susceptible)

        for infected_obj in infected:
            # --// When a zombie fights / interacts with a susceptible
            interaction = infected_obj.act(susceptible, canvas)
            if interaction:
                interaction_occured = True

            object_is_alive = infected_obj.checkalive(canvas)
            if not object_is_alive:
                alive_population -= 1
                infected_count -= 1
                removed_count += 1

                dead_susceptible = Classes.Removed(False, infected_obj)
                infected.remove(infected_obj)
                removed.append(infected_obj)

        # --// Update & add to plot tables each iteration
        Plot_Module.Iterations.append(iteration)
        Plot_Module.SusceptiblePopulation.append(susceptible_count)
        Plot_Module.InfectedPopulation.append(infected_count)
        Plot_Module.RemovedPopulation.append(removed_count)

        # --// Slow down the simulation slightly if an interation occured
        time.sleep(interaction_occured and .05 or .02)
        window.update()
    return SUSCPETIBLES_WIPED_OUT, INFECTEDS_WIPED_OUT

ALL_SUSCEPTIBLES_DIED, ALL_INFECTEDS_DIED = zombie_simulation(200,10,0)
Plot_Module.SHOW_PLOT_CHART(ALL_SUSCEPTIBLES_DIED, ALL_INFECTEDS_DIED)