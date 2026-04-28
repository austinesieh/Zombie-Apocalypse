import matplotlib.pyplot as PLOT_Module

Iterations = []

SusceptiblePopulation = []
InfectedPopulation = []
RemovedPopulation = []

def SHOW_PLOT_CHART(ALL_SUSCEPTIBLES_DIED, ALL_INFECTEDS_DIED):
    PLOT_Module.plot(Iterations, SusceptiblePopulation, color= 'blue', label="Susceptible Population")
    PLOT_Module.plot(Iterations, InfectedPopulation, color = "green",label="Infected Population")
    PLOT_Module.plot(Iterations, RemovedPopulation, color = "red",label="Removed Population")

    PLOT_Module.xlabel("Iterations")
    PLOT_Module.ylabel("Population")

    if ALL_SUSCEPTIBLES_DIED:
        PLOT_Module.axvline(x=ALL_SUSCEPTIBLES_DIED, color="blue", linestyle="--", label="ALL SUSCEPTIBLES DEAD")

    if ALL_INFECTEDS_DIED:
        PLOT_Module.axvline(x=ALL_INFECTEDS_DIED, color="green", linestyle="--", label="ALL INFECTEDS DEAD")

    PLOT_Module.legend()
    PLOT_Module.show()
