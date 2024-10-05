from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from models.block import Block
from models.bomberman import Bomberman
from models.metal import Metal

class BombermanModel(Model):
    def __init__(self, width, high, map_file, algorithm="BFS"):
        super().__init__()
        self.grid = MultiGrid(width, high, True)
        self.schedule = RandomActivation(self)
        self.algorithm = algorithm
        unique_id_counter = 0  
        self.visited_numbers = {}

        # Crear el mapa y colocar los agentes correspondientes
        for y, row in enumerate(reversed(map_file)):
            for x, cell in enumerate(row):
                if cell == 'C_b':
                    bomberman = Bomberman(unique_id_counter, (x, y), self, self.algorithm)
                    unique_id_counter += 1
                    self.grid.place_agent(bomberman, (x, y))
                    self.schedule.add(bomberman)

                elif cell == 'R':
                    bloque = Block(unique_id_counter, (x, y), self)
                    unique_id_counter += 1
                    self.grid.place_agent(bloque, (x, y))
                    self.schedule.add(bloque)

                elif cell == "R_s":
                        rock = Block(unique_id_counter, (x, y), self, has_exit=True)
                        unique_id_counter += 1
                        self.grid.place_agent(rock, (x, y))
                        self.schedule.add(rock)

                elif cell == 'M':
                    metal = Metal(unique_id_counter, (x, y), self)
                    unique_id_counter += 1
                    self.grid.place_agent(metal, (x, y))
                    self.schedule.add(metal)
    
    def place_agent_number(self, pos, number):
        print(f"Colocando número {number} en la casilla {pos}")
        print(f"self.visited_numbers: {self.visited_numbers}")
        # Registrar el número de la casilla en self.visited_numbers
        self.visited_numbers[pos] = number
        # Asegurar que el número se queda en la celda aunque Bomberman no esté
        self.grid.place_agent(NumberMarker(pos, self, number), pos)

    def step(self):
        # Avanzar en el tiempo
        self.schedule.step()

class NumberMarker(Agent):
    def __init__(self, pos, model, number):
        super().__init__(pos, model)
        self.number = number

    def step(self):
        pass  # Los números no hacen nada, son solo decorativos