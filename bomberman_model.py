from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from models.block import Block
from models.bomberman import Bomberman
from models.metal import Metal
from models.road import Road

class BombermanModel(Model):
    def __init__(self, width, high, map):
        super().__init__()
        self.grid = MultiGrid(width, high, True)
        self.schedule = SimultaneousActivation(self)
        unique_id_counter = 0  

        # Crear el mapa y colocar los agentes correspondientes
        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                if cell == 'C_b':
                    bomberman = Bomberman(unique_id_counter, (x, y), self)
                    unique_id_counter += 1
                    self.grid.place_agent(bomberman, (x, y))
                    self.schedule.add(bomberman)

                elif cell == 'R':
                    bloque = Block(unique_id_counter, (x, y), self)
                    unique_id_counter += 1
                    self.grid.place_agent(bloque, (x, y))
                    self.schedule.add(bloque)

                elif cell == 'C':
                    road = Road(unique_id_counter, (x, y), self)
                    unique_id_counter += 1
                    self.grid.place_agent(road, (x, y))
                    self.schedule.add(road)

                elif cell == 'M':
                    metal = Metal(unique_id_counter, (x, y), self)
                    unique_id_counter += 1
                    self.grid.place_agent(metal, (x, y))
                    self.schedule.add(metal)
    
    def setp(self):
        self.schedule.step()
