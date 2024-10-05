from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from bomberman_model import BombermanModel, NumberMarker
from models.block import Block
from models.bomberman import Bomberman
from models.metal import Metal
from models.road import Road

def bomberman_portrayal(agent):
    portrayal = {}

    if isinstance(agent, NumberMarker):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "white"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["text"] = str(agent.number)
        portrayal["text_color"] = "black"
        portrayal["Layer"] = 3
        return portrayal  # No necesitamos seguir evaluando otros agentes aquí

    if hasattr(agent, 'model') and agent.pos in agent.model.visited_numbers:
        portrayal["text"] = str(agent.model.visited_numbers[agent.pos])
        portrayal["text_color"] = "red"
    
    if isinstance(agent, Bomberman):  
        portrayal["Shape"] = "images/bomberman.png"  
        portrayal["scale"] = 1  
        portrayal["Layer"] = 2

    elif isinstance(agent, Block):
        portrayal["Shape"] = "images/block.png"
        portrayal["scale"] = 1  
        portrayal["Layer"] = 1  
        if agent.has_exit:
            portrayal["text"] = "SALIDA"
            portrayal["text_color"] = "white" 

    elif isinstance(agent, Road):  
        portrayal["Shape"] = "images/path.png"  
        portrayal["scale"] = 1
        portrayal["Layer"] = 0 
        
        # Si la celda está marcada con un número de búsqueda, lo mostramos
        if hasattr(agent, 'step_counter'):
            portrayal["text"] = str(agent.step_counter)
            portrayal["text_color"] = "Black"  # Elige un color adecuado

    elif isinstance(agent, Metal):
        portrayal["Shape"] = "images/metal.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 0

    return portrayal


# Crear la cuadrícula de visualización
def run_interface(width, high, map):
    grid = CanvasGrid(bomberman_portrayal, width, high, width * 70, high * 70) 
    server = ModularServer(BombermanModel, [grid], "Bomberman", {"width": width, "high": high, "map": map})
    server.port = 8521
    server.launch()
