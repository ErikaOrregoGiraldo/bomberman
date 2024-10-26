import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from models.block import Block
from models.bomberman import Bomberman
from models.globe import Globe
from models.metal import Metal
from models.number_marker import NumberMarker

class BombermanModel(Model):    
    def __init__(self, width, high, map_file, algorithm="BFS"):
        super().__init__()
        self.grid_width = width
        self.grid_height = high
        self.grid = MultiGrid(width, high, torus=False)
        self.schedule = RandomActivation(self)
        self.algorithm = algorithm
        unique_id_counter = 0  
        self.visited_numbers = {}
        globe_positions = []
        self.previous_positions = {}
        self.map_file = map_file
        self.running = True  # Bandera para controlar la ejecución del juego

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
                
                elif cell == "C_g":
                    globe_positions.append((x, y))
    
        for globe_position in globe_positions:
                globe = Globe(globe_position, self)
                self.grid.place_agent(globe, globe_position)
                self.schedule.add(globe)

        if not globe_positions:
                self.add_globes(1)

    def finish_game(self):
        """Detiene la ejecución del juego."""
        self.running = False
        print("Juego terminado debido a colisión.")

    def place_agent_number(self, pos, number):
        print(f"Colocando número {number} en la casilla {pos}")
        print(f"self.visited_numbers: {self.visited_numbers}")
        # Registrar el número de la casilla en self.visited_numbers
        self.visited_numbers[pos] = number
        # Asegurar que el número se queda en la celda aunque Bomberman no esté
        self.grid.place_agent(NumberMarker(pos, self, number), pos)

    def step(self):
        # Avanzar en el tiempo solo si el juego está activo
        if self.running:
            self.schedule.step()

    def add_globes(self, count):
        for _ in range(count):
            # Buscar una posición válida aleatoria (C)
            while True:
                x = random.randrange(self.grid_width)
                y = random.randrange(self.grid_height)
                if self.grid.is_cell_empty((x, y)):  # Verificar si es un camino libre
                    globe = Globe((x, y), self)
                    self.grid.place_agent(globe, (x, y))
                    self.schedule.add(globe)
                    break

    def update_previous_position(self, agent, new_position):
        self.previous_positions[agent] = new_position
