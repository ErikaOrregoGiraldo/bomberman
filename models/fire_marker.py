from mesa import Agent

from models.block import Block
from models.globe import Globe
class FireMarker(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.life_span = 1  # Duración de la explosión visual

    def step(self):
        # Reducir la duración y eliminar después de un paso
        self.life_span -= 1
        if self.life_span <= 0:
            # Eliminar cualquier bloque o globo en la posición del FireMarker
            cell_contents = self.model.grid.get_cell_list_contents(self.pos)
            for obj in cell_contents:
                if isinstance(obj, Block) and not obj.has_exit:  # Solo eliminar bloques sin salida
                    self.model.grid.remove_agent(obj)
                    print(f"Bloque destruido en {self.pos}, convirtiéndose en camino")
                elif isinstance(obj, Globe):  # Eliminar globos afectados por la explosión
                    self.model.grid.remove_agent(obj)
                    print(f"Globo destruido en {self.pos} por la explosión")
                    
            # Convertir la posición en camino libre y eliminar el FireMarker
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)