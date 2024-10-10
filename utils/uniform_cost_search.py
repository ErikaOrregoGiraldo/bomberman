from heapq import heappush, heappop

from heapq import heappush, heappop

def uniform_cost_search(start, goal, model):
    # Usamos una cola de prioridad (heap) para manejar los costos
    queue = []
    heappush(queue, (0, 0, start))  # (costo acumulado, prioridad de desempate, nodo)
    visited = set()
    came_from = {start: None}
    
    # Contador para las casillas analizadas
    step_counter = 1
    priority_counter = 0  # Este contador nos ayudará a desempatar cuando los costos sean iguales

    while queue:
        # Atender el nodo con el menor costo acumulado
        current_cost, _, current_node = heappop(queue)
        
        # Si llegamos a la meta, reconstruimos el camino
        if is_adjacent(current_node, goal):
            return reconstruct_path(came_from, current_node)
        
        # Marcar el nodo como visitado
        visited.add(current_node)
        # Mostrar en el mapa el orden de la casilla analizada
        model.place_agent_number(current_node, step_counter)
        print(f"Casilla {current_node} marcada con el número {step_counter}")  # Imprimir en consola
        step_counter += 1
        
        # Obtener vecinos en el orden ortogonal: arriba, derecha, abajo, izquierda
        neighbors = get_neighbors_in_orthogonal_order(current_node, model)
        for neighbor in neighbors:
            if neighbor not in visited and model.grid.is_cell_empty(neighbor):
                new_cost = current_cost + 1  # Asumimos que el costo de moverse es 1
                priority_counter += 1  # Incrementar la prioridad para respetar el orden de inserción
                heappush(queue, (new_cost, priority_counter, neighbor))
                came_from[neighbor] = current_node

    return None  # Si no se encuentra un camino




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
