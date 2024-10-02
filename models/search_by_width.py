from collections import deque

from models.road import Road

def breadth_first_search(start_pos, goal_pos, grid):
    queue = deque([[start_pos]])
    visited = set()

    print(f"Iniciando BFS desde {start_pos} hasta {goal_pos}")

    while queue:
        path = queue.popleft()
        current_pos = path[-1]

        # Imprimir el estado actual de la búsqueda
        print(f"Explorando posición {current_pos}, camino actual: {path}")

        if current_pos == goal_pos:
            print(f"Meta alcanzada en {current_pos}")
            return path

        if current_pos in visited:
            continue

        visited.add(current_pos)

        neighbors = get_neighbors(current_pos, grid)
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    print("No se encontró un camino.")
    return None


def get_neighbors(pos, grid):
    neighbors = []
    x, y = pos
    possible_moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    
    for move in possible_moves:
        if grid.out_of_bounds(move) is False:  # Verificar si está dentro de los límites
            cell_content = grid.get_cell_list_contents([move])
            if all(isinstance(agent, Road) for agent in cell_content):  # Solo se mueve en caminos
                neighbors.append(move)
                print(f"Vecino válido encontrado: {move}")

    return neighbors
