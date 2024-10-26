from utils.shared.utils import get_neighbors_in_orthogonal_order, is_adjacent, reconstruct_path, is_valid_move

def depth_first_search(start, goal, model):
    stack = [start]
    visited = {start}
    came_from = {start: None}
    
    # Contador para las casillas analizadas
    step_counter = 0

    while stack:
        current = stack.pop()

        # Mostrar en el mapa el orden de la casilla analizada
        model.place_agent_number(current, step_counter)
        print(f"Casilla {current} marcada con el número {step_counter}")  # Imprimir en consola
        
        step_counter += 1

        # Si estamos en una casilla adyacente a la roca con la salida, terminamos la búsqueda
        if is_adjacent(current, goal):
            return reconstruct_path(came_from, current)
        
        # Obtener vecinos en el orden ortogonal: arriba, derecha, abajo, izquierda
        neighbors = get_neighbors_in_orthogonal_order(current, model)
        for neighbor in reversed(neighbors):
            if neighbor not in visited and is_valid_move(neighbor, model):
                visited.add(neighbor)
                stack.append(neighbor)
                came_from[neighbor] = current

    return None  # No se encontró la meta