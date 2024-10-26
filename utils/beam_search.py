import math

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
            if neighbor not in visited and model.grid.is_cell_empty(neighbor):
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

# Auxiliary functions (euclidean_distance, manhattan_distance, is_adjacent, reconstruct_path, get_neighbors_in_orthogonal_order)
def euclidean_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def manhattan_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def is_adjacent(pos1, pos2):
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
    neighbors = [
        (x - 1, y),   # Left
        (x, y + 1),   # Up
        (x + 1, y),   # Right
        (x, y - 1),   # Down
    ]
    return [n for n in neighbors if not model.grid.out_of_bounds(n)]
