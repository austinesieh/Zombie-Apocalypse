import random
# --// World size 1000,1000
WORLD_SIZE = 1000

def distance(obj1, obj2):
    return ((obj2['x'] - obj1['x'])**2 + (obj2['y'] - obj1['y'])**2) ** 0.5

class Person:
    def __init__(self, name, canvas, object_color):
        self.name = name
        self.health = 100
        self.hunger = 100
        self.position = {"x": random.randint(0, WORLD_SIZE), "y": random.randint(0, WORLD_SIZE)}
        self.causeOfDeath = ""
        self.canvasID = canvas.create_oval(
            self.position['x'],
            self.position['y'],
            self.position['x'] + 5,
            self.position['y'] + 5,
            fill = object_color
        )

    def update_screen_position(self, canvas):
        canvas.coords(
            self.canvasID, self.position['x'], self.position['y'],
            self.position['x'] + 5, self.position['y'] + 5
        )

    def roam(self):
        def world_limit():
            # --// Keep object in the boundaries of the world
            if (self.position["x"] < 0):
                self.position["x"] = 0
            elif (self.position["x"] > WORLD_SIZE):
                self.position["x"] = WORLD_SIZE
            if (self.position["y"] < 0):
                self.position["y"] = 0
            elif (self.position["y"] > WORLD_SIZE):
                self.position["y"] = WORLD_SIZE

        self.position['x'] += random.randint(-10, 10)
        self.position['y'] += random.randint(-10, 10)
        world_limit()

    def feed(self, food):
        if type(food) == Susceptible:
            self.hunger += 10
        else:
            # --// any other food
            self.hunger += 5

    def die(self, death_cause: str):
        self.causeOfDeath = death_cause

    def checkalive(self):
        alive = (self.health > 0 and self.hunger > 0)
        if not alive:
            if self.health <= 0:
                self.die("Was murdered")
            else:
                self.die("Died of hunger")

        return alive

class Susceptible(Person):
    def __init__(self, name, canvas, object_color):
        super().__init__(name, canvas, object_color)

    def check_infected_near(self, infected_list):
        close_threshold = 10
        for infected in infected_list:
            if distance(self.position, infected.position) < close_threshold:
                return True

        return False

    def scavenge(self, food_list):
        find_threshold = 10

        for Food in food_list:
            if distance(self.position, Food) < find_threshold:
                self.feed(Food)
                break

    def act(self, infected_list):
        #food_list
        self.roam()
        if not self.check_infected_near(infected_list):
            pass
            #self.scavenge(food_list)

        self.hunger -= 2

class Infected(Person):
    def __init__(self, name, canvas, object_color):
        super().__init__(name, canvas, object_color)

    def hunt(self, susceptible_list):
        find_threshold = 10
        for susceptible in susceptible_list:
            if distance(self.position, susceptible.position) < find_threshold:
                print('kill')
                susceptible.health = 0
                self.feed(susceptible)
                break

    def act(self, susceptible_list):
        self.roam()
        self.hunt(susceptible_list)
        self.hunger -= 2

class Removed:
    def __init__(self, dead_on_arrival, *args):
        if dead_on_arrival:
            # --// Removed object created in simulation without a previous existance
            name = args[0]
            self.name = name
            self.causeOfDeath = "Was already dead"
            self.classBeforeDeath = "Unknown"
        else:
            # --// Removed object created in simulation from a dead person
            previously_living_object = args[0]
            self.name = previously_living_object.name
            self.causeOfDeath = previously_living_object.causeOfDeath
            self.classBeforeDeath = type(previously_living_object)