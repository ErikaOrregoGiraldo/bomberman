from mesa import Agent


class Block(Agent):
    """Un agente que representa un bloque en el juego."""

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos  
