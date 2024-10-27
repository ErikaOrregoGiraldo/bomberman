from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Choice, UserParam
from mesa.visualization.ModularVisualization import ModularServer
from bomberman_model import BombermanModel
from models.block import Block
from models.bomb import Bomb
from models.bomberman import Bomberman
from models.fire_marker import FireMarker
from models.globe import Globe
from models.metal import Metal
from models.number_marker import NumberMarker

def bomberman_portrayal(agent):
    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0}

    if isinstance(agent, NumberMarker):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["text"] = str(agent.number)
        portrayal["text_color"] = "black"
        portrayal["Layer"] = 100
        return portrayal  # No necesitamos seguir evaluando otros agentes aquí

    if hasattr(agent, 'model') and agent.pos in agent.model.visited_numbers:
        portrayal["text"] = str(agent.model.visited_numbers[agent.pos])
        portrayal["text_color"] = "red"
    
    if isinstance(agent, Bomberman):  
        portrayal["Shape"] = "images/bomberman.png"  
        portrayal["scale"] = 1  
        portrayal["Layer"] = 2  # Capa para Bomberman

    elif isinstance(agent, Block):
        portrayal["Shape"] = "images/block.png"
        portrayal["scale"] = 1  
        portrayal["Layer"] = 1  # Capa para bloques
        if agent.has_exit:
            portrayal["text"] = "SALIDA"
            portrayal["text_color"] = "white" 

    elif isinstance(agent, Metal):
        portrayal["Shape"] = "images/metal.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 0  # Capa para metal

    elif isinstance(agent, Globe):
        portrayal["Shape"] = "images/globe.png"

    elif isinstance(agent, Bomb):
        portrayal["Shape"] = "images/bomb.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 3

    elif isinstance(agent, FireMarker):
        portrayal["Shape"] = "images/fire.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 4  # Capas superiores para el efecto de fuego

    return portrayal

# Crear la cuadrícula de visualización
def run_interface(width, high, map_file):
    grid = CanvasGrid(bomberman_portrayal, width, high, width * 70, high * 70)

    # Dropdown menu to choose the algorithm
    algorithm_choice = Choice("Algoritmo de búsqueda", value="BFS", choices=["BFS", "DFS", "UCS", "A*", "Beam Search", "Hill Climbing"])
    heuristic_choice = Choice("Heurística", value="Euclidean", choices=["Euclidean", "Manhattan"])

    server = ModularServer(
        BombermanModel,
        [grid],
        "Bomberman", 
        {"width": width, "high": high, "map_file": map_file, "algorithm": algorithm_choice, "heuristic": heuristic_choice}
    )
    server.port = 8521
    server.launch()
