from mesa import Agent
from models.block import Block
from models.road import Road  # Asegúrate de importar la clase Road
from utils.breadth_first_search import breadth_first_search

class Bomberman(Agent):
    """Un agente que representa al Bomberman en el juego."""
    
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos 
        self.path = []  # Aquí guardaremos el camino hacia la salida

    def move(self):
        # Encontrar la posición de la salida
        exit_position = self.find_exit_position()

        # Verificar si se ha encontrado la salida
        if exit_position is not None:
            # Si no hay un camino calculado o ya llegamos al final, calculamos un nuevo camino
            if not self.path:
                self.path = breadth_first_search(self.pos, exit_position, self.model)
                # Eliminar la posición actual de Bomberman del camino si es la primera
                if self.path and self.path[0] == self.pos:
                    self.path.pop(0)  # Eliminar la posición inicial

                print(f"Camino encontrado: {self.path}")

            # Mientras haya posiciones en el camino, intentamos mover
            while self.path:
                next_position = self.path[0]  # Tomamos la primera posición del camino

                # Verificamos si la celda es de tipo 'Road'
                if self.is_road(next_position, self.model):
                    self.model.grid.move_agent(self, next_position)
                    self.pos = next_position  # Actualiza la posición de Bomberman aquí
                    self.path.pop(0)  # Eliminamos la posición del camino
                    print(f"Bomberman se movió a: {self.pos}")
                else:
                    print(f"Posición {next_position} no es de tipo 'Road'. No se puede mover.")
                    break  # Si no se puede mover, salimos del bucle

        else:
            print("No se ha encontrado la salida.")

    def is_road(self, position, model):
        """Verifica si la celda en la posición dada es un camino (Road)."""
        cell_contents = model.grid.get_cell_list_contents(position)
        return any(isinstance(agent, Road) for agent in cell_contents)

    def find_exit_position(self):
        # Encontrar la roca con la salida
        for agent in self.model.schedule.agents:
            if isinstance(agent, Block) and agent.has_exit:
                return agent.pos
        return None  # Debería siempre encontrar una roca con salida

    def step(self):
        self.move()
