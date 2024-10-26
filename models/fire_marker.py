from mesa import Agent
from models.block import Block
from models.globe import Globe

class FireMarker(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.life_span = 1  # Duración de la explosión visual

    def step(self):
        # Reducir la duración de vida del FireMarker
        self.life_span -= 1
        if self.life_span <= 0:
            cell_contents = self.model.grid.get_cell_list_contents(self.pos)
            for obj in cell_contents:
                # Eliminar cualquier bloque, incluyendo el que contiene la salida
                if isinstance(obj, Block):
                    self.model.grid.remove_agent(obj)
                    print(f"Bloque destruido en {self.pos}, convirtiéndose en camino")
                elif isinstance(obj, Globe):
                    self.model.grid.remove_agent(obj)
                    print(f"Globo destruido en {self.pos} por la explosión")
                    
            # Eliminar el FireMarker después de que cumpla su función
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

