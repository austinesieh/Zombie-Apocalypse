import random
import time
import UI_Module as UI

WORLD_SIZE = 1000 # --// World size 1000,1000
text_labels = [] # --// for dynamically getting rid of all textlabels

def distance(obj1, obj2):
    return ((obj2['x'] - obj1['x'])**2 + (obj2['y'] - obj1['y'])**2) ** 0.5

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

class Person:
    def __init__(self, name, canvas, object_color):
        self.name = name
        self.health = 100
        self.hunger = 100
        self.position = {"x": random.randint(0 + 50, WORLD_SIZE - 50), "y": random.randint(0 + 50, WORLD_SIZE - 250)}
        self.causeOfDeath = ""
        self.canvasID = canvas.create_oval(
            self.position['x'],
            self.position['y'],
            self.position['x'] + 10,
            self.position['y'] + 10,
            fill = object_color
        )

    def update_screen_position(self, canvas):
        canvas.coords(
            self.canvasID, self.position['x'], self.position['y'],
            self.position['x'] + 10, self.position['y'] + 10
        )

    def world_limit(self):
        # --// Keep object in the boundaries of the world
        if (self.position["x"] < 0 + 50):
            self.position["x"] = 0 + 50
        if (self.position["x"] > WORLD_SIZE - 50):
            self.position["x"] = WORLD_SIZE - 50

        if (self.position["y"] < 0 + 50):
            self.position["y"] = 0 + 50
        if (self.position["y"] > WORLD_SIZE - 250):
            self.position["y"] = WORLD_SIZE - 250

    def roam(self, canvas):
        self.position['x'] += random.randint(-10, 10)
        self.position['y'] += random.randint(-10, 10)
        self.world_limit()
        self.update_screen_position(canvas)

    def feed(self, food):
        if type(food) == Susceptible:
            self.hunger += clamp(self.hunger + 10,0, 100)
        else:
            # --// any other food
            self.hunger += clamp(self.hunger + 5,0, 100)

    def die(self, death_cause: str, canvas):
        canvas.delete(self.canvasID)
        self.causeOfDeath = death_cause

    def checkalive(self, canvas):
        alive = (self.health > 0 and self.hunger > 0)
        if not alive:
            if self.health <= 0:
                self.die("Was murdered", canvas)
            else:
                death_label = UI.CREATE_LABEL(canvas, self, "DIED OF HUNGER", isinstance(self, Infected) and "green" or "white")
                self.die("Died of hunger", canvas)
                text_labels.append(death_label)

        return alive

class Susceptible(Person):
    def __init__(self, name, canvas, object_color):
        super().__init__(name, canvas, object_color)

    def act(self, infected_list, canvas):
        self.roam(canvas)
        # --// Slowly lose hunger
        if random.randint(1,2) == 1:
            self.hunger -= float(random.randint(0, 2)) / 10

class Infected(Person):
    def __init__(self, name, canvas, object_color):
        super().__init__(name, canvas, object_color)

    def roam(self, canvas):
        self.position['x'] += random.randint(-20, 20)
        self.position['y'] += random.randint(-20, 20)
        self.world_limit()
        self.update_screen_position(canvas)

    def fight(self, susceptible, canvas):
        if self.hunger >= random.randint(20, 100):
            # --// Create text label where susceptible died
            x1, y1, x2, y2 = canvas.coords(susceptible.canvasID)
            x = (x1 + x2) / 2
            y = y1 - 20

            text_label = UI.CREATE_LABEL(canvas, susceptible, "KILLED BY ZOMBIE", "red")
            text_labels.append(text_label)

            # --// Make object bigger and have red outline
            x1, y1, x2, y2 = canvas.coords(susceptible.canvasID)
            canvas.coords(susceptible.canvasID, x1-6, y1-6, x2+6, y2+6)
            canvas.itemconfig(susceptible.canvasID, outline="red", width=7)

            susceptible.health = 0
            self.feed(susceptible)
        else:
            # --// Create text label where susceptible died
            x1, y1, x2, y2 = canvas.coords(susceptible.canvasID)
            x = (x1 + x2) / 2
            y = y1 - 20

            text_label = UI.CREATE_LABEL(canvas, susceptible, "SUSCEPTIBLE SURVIVED ZOMBIE", "white")
            text_labels.append(text_label)

    def hunt(self, susceptible_list, canvas):
        find_threshold = 20
        interacted = False
        for susceptible in susceptible_list:
            if distance(self.position, susceptible.position) < find_threshold:
                self.fight(susceptible, canvas)
                interacted = True
                break
        return interacted

    def act(self, susceptible_list, canvas):
        self.roam(canvas)
        interaction = self.hunt(susceptible_list, canvas)
        self.hunger -= 1.25
        return interaction

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