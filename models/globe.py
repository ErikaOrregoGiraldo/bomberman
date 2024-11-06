from mesa import Agent
import random

from models.bomberman import Bomberman
from models.number_marker import NumberMarker

class Globe(Agent):
    def __init__(self, post, model) :
        super().__init__(post, model)
        self.post = post

    def move(self):
        if self.pos is None:
            return
        
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        valid_steps = [pos for pos in possible_steps if self.is_valid_estep(pos)]     
        print("Pasos válidos para el globo" , valid_steps)

        if valid_steps:
            new_position = random.choice(valid_steps)
            self.model.update_previous_position(self, self.pos)
            self.check_collision(new_position)
            self.model.grid.move_agent(self, new_position)


    def is_valid_estep(self, pos):
        cell_contents = self.model.grid.get_cell_list_contents(pos)
        return all(isinstance(obj, NumberMarker) or self.model.grid.is_cell_empty(pos) or isinstance(obj, Bomberman) for obj in cell_contents)
    
    
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
        
        