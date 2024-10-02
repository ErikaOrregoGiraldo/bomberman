from mesa import Agent

class Metal(Agent):
    """Un agente que representa un metal en el juego."""
    
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos  
