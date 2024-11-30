from mesa import Agent
from models.metal import Metal
from models.block import Block
from models.power_up import PowerUp

class Bomb(Agent):
    def __init__(self, unique_id, pos, model, power):
        super().__init__(unique_id, model)
        self.pos = pos
        self.timer = power + 2  # Tiempo hasta la explosión
        self.power = power
        self.exploded = False  # Para controlar si la bomba ha explotado
        self.maximizer_player = False

    def step(self):
        # Reducir el temporizador en cada paso
        if not self.exploded:
            self.timer -= 1
            if self.timer <= 0:
                self.explode()

    def explode(self):
        from models.fire_marker import FireMarker
        # Marcar la bomba como explotada
        self.exploded = True
        # Generar las posiciones afectadas por la explosión
        explosion_positions = [self.pos]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for i in range(1, self.power + 1):
                x, y = self.pos[0] + dx * i, self.pos[1] + dy * i
                if not (0 <= x < self.model.grid_width and 0 <= y < self.model.grid_height):
                    break
                explosion_positions.append((x, y))
                
                # Detener la explosión si encuentra un bloque de metal
                cell_contents = self.model.grid.get_cell_list_contents((x, y))
                if any(isinstance(obj, Metal) for obj in cell_contents):
                    break
                
                for obj in cell_contents:
                    if isinstance(obj, Block) and obj.has_power_up and obj.pos in self.model.visited_numbers:
                        power_up = PowerUp(self.model.next_id(), self.model, (x,y), self.model.visited_numbers[obj.pos])
                        #print(f'TIPO {type(obj)}')
                        self.model.grid.remove_agent(obj)
                        self.model.grid.place_agent(power_up, (x,y))
                        self.model.schedule.add(power_up)
                        break
                    

        print(f"Explosión en {self.pos} afectando a {explosion_positions} posiciones")
        # Crear un marcador de explosión para cada posición afectada
        for pos in explosion_positions:
            fire_marker = FireMarker(self.model.next_id(), pos, self.model)
            self.model.grid.place_agent(fire_marker, pos)
            self.model.schedule.add(fire_marker)

        # Eliminar la bomba del modelo después de explotar
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
