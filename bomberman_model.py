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
    def __init__(self, width, high, map_file, algorithm, heuristic, power_ups):
        super().__init__()
        self.grid_width = width
        self.grid_height = high
        self.grid = MultiGrid(width, high, torus=False)
        self.schedule = RandomActivation(self)
        self.algorithm = algorithm
        unique_id_counter = 0
        self.visited_numbers = {}
        self.previous_positions = {}
        self.map_file = map_file
        self.running = True
        self.power_ups = power_ups
        self.export_file = "game_states.txt"
        self.bomberman = None
        self.exit_position = None  # Atributo de posición de salida

        with open(self.export_file, "w") as f:
            f.write("Estados de juego en pre-orden:\n")

        globe_positions = []
        rock_positions = []

        for y, row in enumerate(reversed(map_file)):
            for x, cell in enumerate(row):
                if cell == 'C_b':
                    bomberman = Bomberman(unique_id_counter, (x, y), self, self.algorithm, heuristic)
                    unique_id_counter += 1
                    self.grid.place_agent(bomberman, (x, y))
                    self.schedule.add(bomberman)
                    self.bomberman = bomberman

                elif cell == 'R':
                    rock_positions.append((x, y))

                elif cell == "R_s":
                    rock = Block(unique_id_counter, (x, y), self, has_exit=True)
                    unique_id_counter += 1
                    self.grid.place_agent(rock, (x, y))
                    self.schedule.add(rock)
                    self.exit_position = (x, y)  # Asignar la posición de salida

                elif cell == 'M':
                    metal = Metal(unique_id_counter, (x, y), self)
                    unique_id_counter += 1
                    self.grid.place_agent(metal, (x, y))
                    self.schedule.add(metal)

                elif cell == "C_g":
                    globe_positions.append((x, y))

        power_up_positions = random.sample(rock_positions, min(self.power_ups, len(rock_positions)))

        for rock_position in rock_positions:
            has_power_item = rock_position in power_up_positions
            bloque = Block(unique_id_counter, rock_position, self, has_power_up=has_power_item)
            unique_id_counter += 1
            self.grid.place_agent(bloque, rock_position)
            self.schedule.add(bloque)

        for globe_position in globe_positions:
            globe = Globe(globe_position, self)
            print(f"globe{globe.unique_id}")
            self.grid.place_agent(globe, globe_position)
            self.schedule.add(globe)

        if not globe_positions:
            self.add_globes(1)

    def step(self):
        if self.running:
            self.update_previous_position(self.bomberman, self.bomberman.pos)
            self.schedule.step()
    
    def place_agent_number(self, pos, number):
        """
            Marca una casilla en el mapa con un número que representa el orden en que fue visitada.

            Args:
                pos (tuple): La posición en la grilla.
                number (int): El número que representa el orden de la visita.
        """
        self.visited_numbers[pos] = number
        self.grid.place_agent(NumberMarker(pos, self, number), pos)

    def finish_game(self):
        self.running = False

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
        """
        Actualiza la última posición registrada del agente solo si ha cambiado.

        Args:
            agent: El agente cuya posición se actualiza.
            new_position: La nueva posición del agente.
        """
        if agent not in self.previous_positions or self.previous_positions[agent] != new_position:
            self.previous_positions[agent] = new_position


    def record_state(self, position, heuristic_value=None):
        """
        Registra el estado en un archivo de texto en preorden.
        
        Args:
            position (tuple): La posición actual de Bomberman.
            heuristic_value (float, optional): Valor de la heurística (solo para algoritmos informados).
        """
        with open(self.export_file, "a", encoding="utf-8") as f:
            if heuristic_value is not None:
                f.write(f"Posición: {position}, Heurística: {heuristic_value}\n")
            else:
                f.write(f"Posición: {position}\n")

