from mesa import Agent

class ExitMarker(Agent):
    """Representa la salida visible después de que la roca se destruye."""
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
