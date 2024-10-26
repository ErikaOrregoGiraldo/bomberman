from mesa import Agent
from models.block import Block
from utils.breadth_first_search import breadth_first_search
from utils.depth_first_search import depth_first_search
from utils.uniform_cost_search import uniform_cost_search
from utils.a_star_search import a_star_search
from utils.beam_search import beam_search
from utils.hill_climbing_search import hill_climbing_search

class Bomberman(Agent):
    """Un agente que representa al Bomberman en el juego."""

    def __init__(self, unique_id, pos, model, algorithm, heuristic):
        super().__init__(unique_id, model)
        self.pos = pos
        self.path = []  # Aquí guardaremos el camino hacia la salida
        self.algorithm = algorithm
        self.heuristic = heuristic
        self.power = 1  # Poder de destrucción inicial de la bomba
        self.exit_found = False  # Bandera para rastrear si Bomberman encontró la salida
        self.exit_position = self.find_initial_exit_position()  # Guardar la posición de la salida al inicio

    def move(self):
        # Verificar si la salida está libre y moverse a ella
        if self.exit_found and self.exit_position and self.is_path_clear(self.exit_position):
            self.model.grid.move_agent(self, self.exit_position)
            print("¡Bomberman ha alcanzado la salida!")
            self.model.finish_game()
            return

        # Si Bomberman está adyacente a la roca de la salida y aún no ha colocado una bomba
        if self.exit_position and self.is_adjacent(self.exit_position) and not self.exit_found:
            self.place_bomb()
            self.exit_found = True  # Marcar que Bomberman ha encontrado la salida y colocado la bomba
            self.move_to_safe_position()
            return

        # Si aún no se ha encontrado la salida, seguir el camino normalmente
        if self.exit_position and not self.path:
            self.calculate_path(self.exit_position)

        # Si el siguiente paso está bloqueado por un bloque, coloca una bomba
        if self.is_block_in_the_way():
            self.place_bomb()
            self.move_to_safe_position()
        else:
            self.follow_path()

    def find_initial_exit_position(self):
        """Encuentra y guarda la posición inicial de la roca con la salida."""
        for agent in self.model.schedule.agents:
            if isinstance(agent, Block) and agent.has_exit:
                return agent.pos
        return None

    def is_adjacent(self, position):
        """Comprueba si Bomberman está en una posición adyacente a la dada."""
        x, y = self.pos
        px, py = position
        return abs(px - x) + abs(py - y) == 1

    def is_path_clear(self, position):
        """Verifica si la posición está libre para moverse a la salida."""
        cell_contents = self.model.grid.get_cell_list_contents(position)
        return not any(isinstance(obj, Block) for obj in cell_contents)

    def is_block_in_the_way(self):
        """Verifica si el siguiente paso está bloqueado por un bloque."""
        if self.path:
            next_pos = self.path[0]
            cell_contents = self.model.grid.get_cell_list_contents(next_pos)
            return any(isinstance(obj, Block) for obj in cell_contents)
        return False

    def place_bomb(self):
        """Coloca una bomba en la posición actual."""
        from models.bomb import Bomb
        bomb = Bomb(self.model.next_id(), self.pos, self.model, self.power)
        self.model.grid.place_agent(bomb, self.pos)
        self.model.schedule.add(bomb)
        print("¡Bomba colocada!")

    def move_to_safe_position(self):
        """Busca una posición segura fuera del rango de la explosión y se mueve hacia ella."""
        safe_positions = [
            pos for pos in self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            if self.is_safe_position(pos)
        ]
        if safe_positions:
            safe_pos = safe_positions[0]
            self.model.grid.move_agent(self, safe_pos)
            print(f"Bomberman se movió a una posición segura: {safe_pos}")
        else:
            print("No hay posiciones seguras alrededor; Bomberman puede quedar en peligro.")

    def is_safe_position(self, pos):
        """Determina si una posición está fuera del alcance de la explosión."""
        x, y = self.pos
        px, py = pos
        return abs(px - x) > self.power or abs(py - y) > self.power

    def calculate_path(self, exit_position):
        # Cálculo del camino según el algoritmo seleccionado
        if self.algorithm == "BFS":
            self.path = breadth_first_search(self.pos, exit_position, self.model)
        elif self.algorithm == "DFS":
            self.path = depth_first_search(self.pos, exit_position, self.model)
        elif self.algorithm == "UCS":
            self.path = uniform_cost_search(self.pos, exit_position, self.model)
        elif self.algorithm == "A*":
            self.path = a_star_search(self.pos, exit_position, self.model, self.heuristic)
        elif self.algorithm == "Beam Search":
            self.path = beam_search(self.pos, exit_position, self.model, self.heuristic, 2)
        elif self.algorithm == "Hill Climbing":
            self.path = hill_climbing_search(self.pos, exit_position, self.model, self.heuristic)
        print(f"Camino encontrado: {self.path}")

    def follow_path(self):
        """Sigue el camino calculado."""
        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_agent(self, next_position)

    def step(self):
        self.move()