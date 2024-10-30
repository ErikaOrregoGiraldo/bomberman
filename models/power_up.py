from mesa import Agent, Model

class PowerUp(Agent):
    def __init__(self, unique_id: int, model: Model, pos, value) -> None:
        super().__init__(unique_id, model)
        self.pos = pos
        self.value = value