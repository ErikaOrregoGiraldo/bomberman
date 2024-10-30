from mesa import Agent

class Block(Agent):
    def __init__(self, unique_id, pos, model, has_exit=False, has_power_up=False):
        super().__init__(unique_id, model)
        self.pos = pos
        self.has_exit = has_exit
        self.has_power_up = has_power_up

    def step(self):
        # Las rocas no tienen acciones en este entregable
        pass