from utils.shared.utils import get_neighbors_in_orthogonal_order, is_adjacent, reconstruct_path, manhattan_distance, euclidean_distance


def hill_climbing_search(start, goal, model, heuristic_name):
    heuristic = manhattan_distance if heuristic_name == 'Manhattan' else euclidean_distance
    current_node = start
    visited = set()
    came_from = {start: None}
    step_counter = 1

    while True:
        # If current node is adjacent to the goal, return the path
        if is_adjacent(current_node, goal):
            return reconstruct_path(came_from, current_node)
        
        # Mark the current node as visited
        visited.add(current_node)
        model.place_agent_number(current_node, step_counter)
        print(f"Casilla {current_node} marcada con el número {step_counter}")
        step_counter += 1

        # Get neighbors and find the one with the best heuristic score
        neighbors = get_neighbors_in_orthogonal_order(current_node, model)
        next_node = None
        min_heuristic = float('inf')

        for neighbor in neighbors:
            if neighbor not in visited and model.grid.is_cell_empty(neighbor):
                h = heuristic(neighbor, goal)
                if h < min_heuristic:
                    min_heuristic = h
                    next_node = neighbor

        # If there is no better neighbor, stop (local maximum reached)
        if next_node is None or min_heuristic >= heuristic(current_node, goal):
            return None  # No path found if stuck in a local maximum

        # Move to the next node with the best heuristic
        came_from[next_node] = current_node
        current_node = next_node
