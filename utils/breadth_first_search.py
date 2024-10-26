from collections import deque
from utils.shared.utils import get_neighbors_in_orthogonal_order, is_adjacent, reconstruct_path, is_valid_move

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

        if is_adjacent(current, goal):
            return reconstruct_path(came_from, current)

        neighbors = get_neighbors_in_orthogonal_order(current, model)
        for neighbor in neighbors:
            if neighbor not in visited and is_valid_move(neighbor, model):
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current

    return None