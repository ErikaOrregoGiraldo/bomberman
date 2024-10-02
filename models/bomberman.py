from mesa import Agent

class Bomberman(Agent):
    """Un agente que representa al Bomberman en el juego."""
    
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos 

