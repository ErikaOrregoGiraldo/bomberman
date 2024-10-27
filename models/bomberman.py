from collections import deque
from mesa import Agent
from utils.breadth_first_search import breadth_first_search, breadth_first_search_without_markers
from utils.depth_first_search import depth_first_search
from utils.uniform_cost_search import uniform_cost_search
from utils.a_star_search import a_star_search
from utils.beam_search import beam_search
from utils.hill_climbing_search import hill_climbing_search
from utils.shared.utils import get_neighbors_in_orthogonal_order
from models.block import Block
from models.metal import Metal
from models.bomb import Bomb
from models.fire_marker import FireMarker

class Bomberman(Agent):
    """Un agente que representa al Bomberman en el juego."""

    def __init__(self, unique_id, pos, model, algorithm, heuristic):
        super().__init__(unique_id, model)
        self.pos = pos
        self.path = []  # Aquí guardaremos el camino hacia la salida
        self.algorithm = algorithm
        self.heuristic = heuristic
        self.safe_path = []  # Camino hacia una posición segura
        self.return_path = []  # Camino de regreso al camino original
        self.power = 1  # Poder de destrucción inicial de la bomba
        self.exit_found = False  # Bandera para rastrear si Bomberman encontró la salida
        self.placed_bomb = False  # Rastrea si ya se ha colocado una bomba
        self.waiting_for_explosion = False  # Indica si Bomberman está esperando que la bomba y el fuego desaparezcan
        self.safe_position = None  # Posición segura donde Bomberman esperará
        self.exit_position = self.find_exit_position() 

    def move(self):
        """Controla los movimientos de Bomberman y gestiona la lógica de colocación de bombas y movimiento seguro."""
        
        # Si está esperando en la posición segura, verifica si la explosión ha terminado
        if self.waiting_for_explosion:
            if self.is_explosion_over():
                print("La explosión ha terminado, Bomberman retoma su camino.")
                self.waiting_for_explosion = False
                self.placed_bomb = False
                self.calculate_return_path()  # Calcula el camino de regreso al camino original
            else:
                self.follow_safe_path()  # Moverse en el camino seguro paso a paso
            return

        # Si Bomberman está en el proceso de regresar al camino original
        if self.return_path:
            self.follow_return_path()  # Seguir el camino de regreso paso por paso
            return

        exit_position = self.find_exit_position()

        # Si la salida está libre, moverse directamente hacia allí
        if self.exit_found and exit_position and not self.is_block_present(exit_position):
            self.model.grid.move_agent(self, exit_position)
            print("¡Bomberman ha alcanzado la salida!")
            self.model.finish_game()
            return

        # Colocar una bomba si Bomberman está adyacente a la roca con la salida
        if exit_position and self.is_adjacent(exit_position) and not self.exit_found:
            self.place_bomb()
            self.exit_found = True
            self.calculate_safe_path()
            return

        # Calcular un nuevo camino si es necesario
        if exit_position and not self.path:
            self.calculate_path(self.exit_position)
            print(f"Camino encontrado: {self.path}")

        # Colocar bomba si un bloque está en el camino
        if self.is_block_in_the_way() and not self.placed_bomb:
            self.place_bomb()
            self.calculate_safe_path()
        else:
            self.follow_path()  # Moverse si no hay bloque en el camino

    def is_explosion_over(self):
        """Verifica si todos los agentes bomba y fuego han sido eliminados del modelo."""
        for agent in self.model.schedule.agents:
            if isinstance(agent, Bomb) or isinstance(agent, FireMarker):
                return False
        return True
    
    def calculate_return_path(self):
        """Calcula el camino de regreso al último punto explorado antes de ir a la posición segura."""
        if self.path:
            self.return_path = breadth_first_search_without_markers(self.pos, self.path[0], self.model)
            if self.return_path:
                self.return_path = self.return_path[1:]  # Evitar incluir la posición actual en el retorno
            print(f"Camino de regreso al camino original calculado: {self.return_path}")
            
    def follow_safe_path(self):
        """Mueve a Bomberman paso a paso hacia la posición segura."""
        if self.safe_path:
            next_safe_step = self.safe_path.pop(0)
            self.model.grid.move_agent(self, next_safe_step)
            print(f"Bomberman se movió a {next_safe_step} buscando seguridad")
            
    def follow_return_path(self):
        """Mueve a Bomberman paso a paso de regreso al camino original."""
        if self.return_path:
            next_return_step = self.return_path.pop(0)
            self.model.grid.move_agent(self, next_return_step)
            print(f"Bomberman regresando al camino original, movido a {next_return_step}")

    def find_exit_position(self):
        """Busca la posición de la roca que contiene la salida (R_s)."""
        for agent in self.model.schedule.agents:
            if isinstance(agent, Block) and agent.has_exit:
                return agent.pos
        return None

    def follow_path(self):
        """Sigue el camino calculado hacia la salida o la siguiente posición."""
        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_agent(self, next_position)
    
    
    def calculate_safe_path(self):
        """Calcula el camino paso a paso hacia una posición segura usando un BFS sin marcar casillas."""
        queue = deque([(self.pos, 0)])
        visited = set([self.pos])

        while queue:
            current_pos, _ = queue.popleft()
            if self.is_safe_position(current_pos):
                self.safe_position = current_pos
                self.safe_path = breadth_first_search_without_markers(self.pos, current_pos, self.model)
                print(f"Camino hacia posición segura calculado: {self.safe_path}")
                self.waiting_for_explosion = True
                return

            # Expande vecinos ortogonales
            for neighbor in get_neighbors_in_orthogonal_order(current_pos, self.model):
                if neighbor not in visited and self.is_valid_move_for_escape(neighbor):
                    visited.add(neighbor)
                    queue.append((neighbor, 1))
    
    
    def is_valid_move_for_escape(self, pos):
        """Determina si Bomberman puede moverse a una posición para escapar de la explosión."""
        cell_contents = self.model.grid.get_cell_list_contents(pos)
        for obj in cell_contents:
            if isinstance(obj, Block) or isinstance(obj, Metal):
                return False
        return True
    
    def is_adjacent(self, position):
        """Comprueba si Bomberman está en una posición adyacente a la dada."""
        x, y = self.pos
        px, py = position
        return abs(px - x) + abs(py - y) == 1

    def is_block_present(self, position):
        """Verifica si hay un bloque en la posición dada."""
        cell_contents = self.model.grid.get_cell_list_contents(position)
        return any(isinstance(obj, Block) for obj in cell_contents)

    def is_block_in_the_way(self):
        """Verifica si el siguiente paso está bloqueado por un bloque."""
        if self.path:
            next_pos = self.path[0]
            cell_contents = self.model.grid.get_cell_list_contents(next_pos)
            return any(isinstance(obj, Block) for obj in cell_contents)
        return False

    def place_bomb(self):
        """Coloca una bomba en la posición actual."""
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

    def step(self):
        self.move()