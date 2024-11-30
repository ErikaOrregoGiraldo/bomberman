from mesa import Agent
from models.bomberman import Bomberman
from models.number_marker import NumberMarker
from utils.poda_alpha_beta import poda_alpha_beta_search

class Globe(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos

    def move(self):
        if self.pos is None:
            return
        
        # Obtener la posición de Bomberman como objetivo
        bomberman = next(agent for agent in self.model.schedule.agents if isinstance(agent, Bomberman))
        goal = bomberman.pos

        # Calcular el mejor movimiento usando poda alfa-beta
        depth = 3  # Profundidad máxima de búsqueda
        alpha = float('-inf')
        beta = float('inf')

        path = poda_alpha_beta_search(
            start=self.pos, 
            goal=goal, 
            model=self.model, 
            depth=depth, 
            alpha=alpha, 
            beta=beta, 
            maximizer_player=False  # El globo es el jugador minimizador
        )

        if len(path) > 1:
            new_position = path[1]  # El siguiente paso en el camino
            self.model.update_previous_position(self, self.pos)
            self.check_collision(new_position)
            self.model.grid.move_agent(self, new_position)

    def is_valid_step(self, pos):
        cell_contents = self.model.grid.get_cell_list_contents(pos)
        return all(
            isinstance(obj, NumberMarker) or 
            self.model.grid.is_cell_empty(pos) or 
            isinstance(obj, Bomberman) for obj in cell_contents
        )

    def check_collision(self, new_position):
        bomberman = next(agent for agent in self.model.schedule.agents if isinstance(agent, Bomberman))

        # Verificar colisión directa con Bomberman
        if new_position == bomberman.pos:
            print("Colisión directa entre globo y Bomberman.")
            self.model.finish_game()
            return

        # Verificar intercambio de posiciones con Bomberman (colisión alternada)
        for balloon in self.model.schedule.agents:
            if isinstance(balloon, Globe):
                if (self.model.previous_positions.get(bomberman) == new_position and
                    self.model.previous_positions.get(balloon) == bomberman.pos):
                    print("Colisión alternada entre globo y Bomberman.")
                    self.model.finish_game()
                    return

    def step(self):
        self.model.update_previous_position(self, self.pos)
        self.move()
