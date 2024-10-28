from utils.shared.utils import get_neighbors_in_orthogonal_order, is_adjacent, reconstruct_path, manhattan_distance, euclidean_distance, is_valid_move
from heapq import heappush, heappop, nsmallest

def beam_search(start, goal, model, heuristic_name, beam_width):
    # Use a priority queue (heap) to manage nodes, focusing on the top `k` most promising nodes at each depth
    queue = []
    heappush(queue, (0, 0, start))  # (heuristic value, priority tie-breaker, node)
    visited = set()
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    heuristic = manhattan_distance if heuristic_name == 'Manhattan' else euclidean_distance

    step_counter = 0
    priority_counter = 0  # Tie-breaker to maintain insertion order for nodes with the same heuristic value

    while queue:
        # Select only the top `beam_width` nodes to expand in this level
        current_level = nsmallest(beam_width, queue)
        queue = []  # Reset queue for the next level

        for _, _, current_node in current_level:
            # If we reach the goal, reconstruct and return the path
            if is_adjacent(current_node, goal):
                return reconstruct_path(came_from, current_node)
            
            # Mark the node as visited
            visited.add(current_node)
            model.place_agent_number(current_node, step_counter)
            print(f"Casilla {current_node} marcada con el número {step_counter}")  # Console output for visualization
            step_counter += 1

            # Get neighbors in orthogonal order (up, right, down, left)
            neighbors = get_neighbors_in_orthogonal_order(current_node, model)
            for neighbor in neighbors:
                if neighbor not in visited and is_valid_move(neighbor, model):
                    new_cost = cost_so_far[current_node] + 1  # Assume movement cost is 1
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority_counter += 1  # Increment to keep insertion order consistent
                        priority = heuristic(neighbor, goal)  # Use heuristic only (no accumulated cost in Beam Search)
                        heappush(queue, (priority, priority_counter, neighbor))
                        came_from[neighbor] = current_node

    return None  # Return None if no path is found