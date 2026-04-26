import matplotlib.pyplot as PLOT_Module

Iterations = []
SusceptiblePopulation = []
InfectedPopulation = []

def SHOW_PLOT_CHART(susceptibles_gone, infecteds_gone):
    PLOT_Module.plot(Iterations, SusceptiblePopulation, color= 'blue', label="Susceptible Population")
    PLOT_Module.plot(Iterations, InfectedPopulation, color = "green",label="Infected Population")
    PLOT_Module.xlabel("Iterations")
    PLOT_Module.ylabel("Population")

    if susceptibles_gone:
        PLOT_Module.axvline(x=susceptibles_gone, color="red", linestyle="--", label="ALL SUSCEPTIBLES DEAD")

    if infecteds_gone:
        PLOT_Module.axvline(x=infecteds_gone, color="red", linestyle="--", label="ALL INFECTEDS DEAD")

    PLOT_Module.legend()
    PLOT_Module.show()
