from heapq import heappush, heappop

from utils.shared.utils import get_neighbors_in_orthogonal_order, reconstruct_path, manhattan_distance, euclidean_distance, is_valid_move


def a_star_search(start, goal, model, heuristic_name):
    # Usamos una cola de prioridad (heap) para manejar los costos y la heurística
    queue = []
    heappush(queue, (0, 0, start))  # (costo acumulado + heurística, prioridad de desempate, nodo)
    visited = set()
    came_from = {start: None}
    cost_so_far = {start: 0}
    cost_of_nodes = {}

    # Contador para las casillas analizadas
    step_counter = 0
    priority_counter = 0  # Para desempatar cuando las prioridades sean iguales
    
    heuristic = manhattan_distance if heuristic_name == 'Manhattan' else euclidean_distance
    
    while queue:
        # Atender el nodo con la menor prioridad (costo acumulado + heurística)
        _, _, current_node = heappop(queue)
        
        model.record_state(current_node, heuristic(current_node, goal))
        
        # Si llegamos a la meta, reconstruimos el camino
        if current_node == goal:
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
            if neighbor not in visited and is_valid_move(neighbor, model):
                new_cost = cost_so_far[current_node] + 1  # Asumimos que el costo de moverse es 1
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority_counter += 1  # Desempatar
                    priority = new_cost + heuristic(neighbor, goal)  # f(n) = g(n) + h(n)
                    if priority not in cost_of_nodes.keys():
                        cost_of_nodes[priority] = [neighbor]
                    else:
                        cost_of_nodes[priority].append(neighbor)
                    heappush(queue, (priority, priority_counter, neighbor))
                    came_from[neighbor] = current_node
        for key, value in cost_of_nodes.items():
            print(f'Costo {key}, Nodos: {value}, Total: {len(value)}')
    return None  # Si no se encuentra un camino
   