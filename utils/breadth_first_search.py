from collections import deque
from utils.shared.utils import get_neighbors_in_orthogonal_order, is_adjacent, reconstruct_path, is_valid_move
from models.block import Block
from models.metal import Metal

def breadth_first_search(start, goal, model):
    queue = deque([start])
    visited = {start}
    came_from = {start: None}
    
    step_counter = 0

    while queue:
        current = queue.popleft()

        # Mostrar en el mapa el orden de la casilla analizada
        model.place_agent_number(current, step_counter)
        print(f"Casilla {current} marcada con el número {step_counter}")
        
        step_counter += 1

        if current == goal:
            return reconstruct_path(came_from, current)

        neighbors = get_neighbors_in_orthogonal_order(current, model)
        for neighbor in neighbors:
            if neighbor not in visited and is_valid_move(neighbor, model):
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current

    return None

def breadth_first_search_without_markers(start, goal, model):
    """
    Algoritmo de búsqueda por anchura (BFS) sin alterar los NumberMarker.
    
    Args:
        start (tuple): La posición inicial de Bomberman.
        goal (tuple): La posición objetivo hacia la que Bomberman debe dirigirse.
        model (BombermanModel): El modelo que contiene el mapa y los agentes.
    
    Returns:
        list: El camino encontrado desde el inicio hasta la meta. Si no hay camino, devuelve None.
    """
    queue = deque([start])
    visited = {start}
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        # Terminar la búsqueda si alcanzamos la meta
        if current == goal:
            return reconstruct_path(came_from, current)

        # Obtener vecinos en orden ortogonal
        neighbors = get_neighbors_in_orthogonal_order(current, model)

        for neighbor in neighbors:
            if neighbor not in visited and is_valid_move_for_escape(neighbor, model):
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current

    return None  # Si no se encuentra un camino

def is_valid_move_for_escape(pos, model):
    """Verifica si Bomberman puede moverse a una posición para escapar, ignorando NumberMarker."""
    cell_contents = model.grid.get_cell_list_contents(pos)
    for obj in cell_contents:
        if isinstance(obj, Block) or isinstance(obj, Metal):
            return False
    return True