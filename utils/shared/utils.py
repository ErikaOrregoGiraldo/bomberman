import math

from models.block import Block
from models.metal import Metal

def is_adjacent(pos1, pos2):
    """Verifica si dos posiciones están una al lado de la otra."""
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2) == 1

def reconstruct_path(came_from, current):
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def get_neighbors_in_orthogonal_order(pos, model):
    x, y = pos
    # Orden ortogonal: arriba, derecha, abajo, izquierda
    neighbors = [
        (x - 1, y),   # Izquierda
        (x, y + 1),  # Arriba
        (x + 1, y),  # Derecha
        (x, y - 1),  # Abajo
    ]
    # Filtrar los vecinos válidos que están dentro de los límites del mapa y son caminos
    valid_neighbors = [n for n in neighbors if model.grid.out_of_bounds(n) == False]
    return valid_neighbors


def euclidean_distance(pos1, pos2):
    """Calcula la distancia euclideana entre dos puntos."""
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def manhattan_distance(pos1, pos2):
    """Calcula la distancia Manhattan entre dos puntos."""
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def is_valid_move(pos, model):
    cell_contents = model.grid.get_cell_list_contents(pos)
    for obj in cell_contents:
        if isinstance(obj, Metal):
            return False
    return True  

def is_valid_move_for_globe(pos, model):
    from models.globe import Globe
    cell_contents = model.grid.get_cell_list_contents(pos)
    for obj in cell_contents:
        if isinstance(obj, Metal) or isinstance(obj, Block) or isinstance(obj, Globe):
            return False
    return True  