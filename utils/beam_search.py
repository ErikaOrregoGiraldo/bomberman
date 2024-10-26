from utils.shared.utils import get_neighbors_in_orthogonal_order, is_adjacent, reconstruct_path, manhattan_distance, euclidean_distance, is_valid_move

def recursive_beam_search(current_level, goal, model, heuristic, beam_width, visited, came_from, step_counter):
    # Base case: if any node in the current level is adjacent to the goal
    for _, node in current_level:
        if is_adjacent(node, goal):
            return reconstruct_path(came_from, node)

    next_level = []
    priority_counter = 0  # To maintain insertion order for nodes with equal heuristic

    for _, current_node in current_level:
        visited.add(current_node)
        model.place_agent_number(current_node, step_counter)
        print(f"Casilla {current_node} marcada con el número {step_counter}")  # For console output visualization
        step_counter += 1

        # Expand neighbors and calculate their heuristic
        neighbors = get_neighbors_in_orthogonal_order(current_node, model)
        for neighbor in neighbors:
            if neighbor not in visited and is_valid_move(neighbor, model):
                priority_counter += 1
                priority = heuristic(neighbor, goal)
                next_level.append((priority, neighbor))
                came_from[neighbor] = current_node

    # Keep only the top `beam_width` nodes for the next recursion level
    next_level = sorted(next_level)[:beam_width]

    if not next_level:
        return None  # No path found if there are no valid nodes in the next level

    # Recursive call to continue the search on the next level
    return recursive_beam_search(next_level, goal, model, heuristic, beam_width, visited, came_from, step_counter)


def beam_search(start, goal, model, heuristic_name, beam_width):
    heuristic = manhattan_distance if heuristic_name == 'Manhattan' else euclidean_distance
    initial_priority = heuristic(start, goal)
    visited = set()
    came_from = {start: None}

    # Initial call to recursive Beam Search
    return recursive_beam_search([(initial_priority, start)], goal, model, heuristic, beam_width, visited, came_from, step_counter=1)