import random
from mesa import Agent
from models.bomberman import Bomberman
from models.number_marker import NumberMarker
from utils.poda_alpha_beta import poda_alpha_beta_search
from utils.alpha_beta_pruning import alpha_beta_search
class Globe(Agent):
    def __init__(self, pos, model, use_alpha_beta=True):
        super().__init__(pos, model)
        self.pos = pos
        self.use_alpha_beta = use_alpha_beta  # Bandera para usar poda alfa-beta

    def move(self):
        if self.pos is None:
            return

        if self.use_alpha_beta:
            # Usar poda alfa-beta para decidir el movimiento
            bomberman = next(agent for agent in self.model.schedule.agents if isinstance(agent, Bomberman))
            goal = bomberman.pos

            depth = 3  # Profundidad máxima de búsqueda
            alpha = float('-inf')
            beta = float('inf')

            _, next_move = alpha_beta_search(
                position=self.pos,
                goal=goal,
                model=self.model,
                depth=depth,
                alpha=alpha,
                beta=beta,
                maximizing_player=False,  # El globo es el jugador minimizador
                enemy=self
            )

            print(f"Camino encontrado por el globo: {next_move}")

            
            if next_move:
                # Mover a Bomberman al próximo paso calculado
                self.model.grid.move_agent(self, next_move)
                print(f"Globo {self.unique_id} se movió a {next_move} usando poda alfa-beta.")
                return
            else:
                print(f"Poda alfa-beta no encontró un movimiento válido; gloho {self.unique_id} permanece en su lugar.")
        else:
            # Movimiento aleatorio como antes
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            valid_steps = [pos for pos in possible_steps if self.is_valid_step(pos)]
            print("Pasos válidos para el globo", valid_steps)

            if valid_steps:
                new_position = random.choice(valid_steps)
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
