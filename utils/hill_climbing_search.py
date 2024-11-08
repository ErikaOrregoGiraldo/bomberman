from utils.shared.utils import get_neighbors_in_orthogonal_order, reconstruct_path, manhattan_distance, euclidean_distance, is_valid_move

def hill_climbing_search(start, goal, model, heuristic_name):
    """
    Implementación modificada del algoritmo de búsqueda Hill Climbing con retroceso a niveles iniciales.
    
    Args:
        start (tuple): Posición inicial de Bomberman.
        goal (tuple): Posición objetivo (normalmente la salida bajo una roca).
        model (BombermanModel): El modelo de Mesa que contiene el mapa y los agentes.
        heuristic (function): Función heurística para calcular la distancia a la meta.
    
    Returns:
        list: El camino encontrado desde el inicio hasta la meta.
    """
    current_node = start
    came_from = {start: None}
    step_counter = 0
    backtrack_stack = []
    visited = set()  # Conjunto de nodos visitados
    heuristic = manhattan_distance if heuristic_name == 'Manhattan' else euclidean_distance

    while current_node != goal:
        if current_node not in visited:
            model.place_agent_number(current_node, step_counter)
            visited.add(current_node)
            model.record_state(current_node, heuristic(current_node, goal))
            step_counter += 1

        # Obtener vecinos en el orden ortogonal
        neighbors = get_neighbors_in_orthogonal_order(current_node, model)
        
        # Filtrar vecinos válidos y calcular sus valores heurísticos
        valid_neighbors = [
            (neighbor, heuristic(neighbor, goal))
            for neighbor in neighbors
            if is_valid_move(neighbor, model) and neighbor not in visited
        ]

        # Si hay vecinos válidos, elige el vecino con la mejor heurística y almacena el nivel actual
        if valid_neighbors:
            # Select the neighbor with the best heuristic score
            next_node, _ = min(valid_neighbors, key=lambda x: x[1])
            came_from[next_node] = current_node
            backtrack_stack.append(current_node)
            current_node = next_node
        else:
            # Backtrack if no valid neighbors are found
            if backtrack_stack:
                current_node = backtrack_stack.pop(0)
            else:
                # No path found; return None if stack is empty
                return None


    # Reconstruir el camino hacia la salida
    return reconstruct_path(came_from, current_node) if current_node == goal else None
