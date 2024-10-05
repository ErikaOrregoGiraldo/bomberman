from mesa import Agent

class Block(Agent):
    def __init__(self, unique_id, pos, model, has_exit=False):
        super().__init__(unique_id, model)
        self.pos = pos
        self.has_exit = has_exit

    def step(self):
        # Las rocas no tienen acciones en este entregable
        pass