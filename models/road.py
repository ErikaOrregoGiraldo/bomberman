from mesa import Agent

class Road(Agent):
    """Un agente que representa un camino en el juego."""
    
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos  