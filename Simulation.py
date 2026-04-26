from asyncio import wait
import time
import Classes
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
            population_table.append(population_type(f"{population_type.__name__} #{i}", canvas))

    return population_table

print('ji')
def zombie_simulation(susceptible_count, infected_count, removed_count):
    total_participants = susceptible_count + infected_count + removed_count
    alive_population = susceptible_count + infected_count

    susceptible = initialize_population(susceptible_count, Classes.Susceptible)
    infected = initialize_population(infected_count, Classes.Infected)
    removed = initialize_population(removed_count, Classes.Removed, True)

    all_susceptibles_dead = False
    all_infected_dead = False

    while alive_population > 0:
        if not all_susceptibles_dead:
            if susceptible_count <= 0:
                # --// Show on chart when all susceptibles are dead
                all_susceptibles_dead = True

        if not all_infected_dead:
            if infected_count <= 0:
                # --// Show on chart when all infected are dead
                all_infected_dead = True

        # --// Make all susceptible objects act
        for susceptible_obj in susceptible:
            susceptible_obj.act(infected)
            print('do')
            susceptible_obj.update_screen_position(canvas)

            object_is_alive = susceptible_obj.checkalive()
            if not object_is_alive:
                alive_population -= 1

                dead_susceptible = Classes.Removed(False, susceptible_obj)
                susceptible.remove(susceptible_obj)
                removed.append(dead_susceptible)

        for infected_obj in infected:
            infected_obj.act(susceptible)
            object_is_alive = infected_obj.checkalive()

            if not object_is_alive:
                alive_population -= 1

                dead_susceptible = Classes.Removed(False, infected_obj)
                infected.remove(infected_obj)
                removed.append(infected_obj)
        time.sleep(.1)
        window.update()
    print(len(removed))

zombie_simulation(15,30,0)





