from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from bomberman_model import BombermanModel
from models.block import Block
from models.bomberman import Bomberman
from models.metal import Metal
from models.road import Road

def bomberman_portrayal(agent):
    portrayal = {}
    
    if isinstance(agent, Bomberman):  
        portrayal["Shape"] = "images/bomberman.png"  
        portrayal["scale"] = 1  
        portrayal["Layer"] = 1  

    elif isinstance(agent, Block):  
        portrayal["Shape"] = "images/block.png"  
        portrayal["scale"] = 1
        portrayal["Layer"] = 0  

    elif isinstance(agent, Road):  
        portrayal["Shape"] = "images/path.png"  
        portrayal["scale"] = 1
        portrayal["Layer"] = 0 
    
    elif isinstance(agent, Metal):
        portrayal["Shape"] = "images/metal.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 0

    return portrayal

# Crear la cuadrícula de visualización
def run_interface(width, high, map):
    grid = CanvasGrid(bomberman_portrayal, width, high, 500, 500) 
    server = ModularServer(BombermanModel, [grid], "Bomberman", {"width": width, "high": high, "map": map})
    server.port = 8521
    server.launch()
