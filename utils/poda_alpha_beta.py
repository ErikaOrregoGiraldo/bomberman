from models.block import Block
from models.metal import Metal
from utils.shared.utils import get_neighbors_in_orthogonal_order, manhattan_distance, is_valid_move

def poda_alpha_beta_search(start, goal, model, depth, alpha, beta, maximizer_player):
    """Implementación del algoritmo de poda alfa-beta para el juego Bomberman."""
    
    # Agregar depuración
    print(f"Evaluando posición: {start}, Profundidad: {depth}")
    
    if depth == 0 or start == goal:
        print(f"Start: {[start]}")
        print(f"Goal: {[goal]}")

        print(f"Camino final: {[start]}")
        return [start]
    
    # Generar los posibles movimientos (acciones)
    posibles_movimientos = generar_posibles_movimientos(start, model)
    
    if maximizer_player:  # Si es Bomberman (jugador maximizador)
        max_eval = float('-inf')
        best_move = None  # Para guardar el mejor movimiento
        for movimiento in posibles_movimientos:
            path = poda_alpha_beta_search(movimiento, goal, model, depth - 1, alpha, beta, False)
            eval = heuristica(movimiento, model, maximizer_player)  # Usar heurística para evaluar el movimiento
            if eval > max_eval:
                max_eval = eval
                best_move = path  # Guardar el camino correspondiente
            alpha = max(alpha, eval)
            if beta <= alpha:  # Poda
                break
        return [start] + best_move if best_move else []  # Retorna el camino que lleva a la mejor jugada
    
    else:  # Si es un globo (jugador minimizador)
        min_eval = float('inf')
        best_move = None  # Para guardar el mejor movimiento
        for movimiento in posibles_movimientos:
            path = poda_alpha_beta_search(movimiento, goal, model, depth - 1, alpha, beta, True)
            eval = heuristica(movimiento, model, maximizer_player)  # Usar heurística para evaluar el movimiento
            if eval < min_eval:
                min_eval = eval
                best_move = path  # Guardar el camino correspondiente
            beta = min(beta, eval)
            if beta <= alpha:  # Poda
                break
        return [start] + best_move if best_move else []  # Retorna el camino que lleva a la mejor jugada


def heuristica(position, model, maximizer_player):
    """Calcula la heurística de la posición actual."""
    # Ejemplo de heurística: la distancia de Manhattan a la meta (y la prioridad de seguridad si es maximizador)
    if maximizer_player:
        print(f"Posición: {position}: Heuristica: {[ manhattan_distance(position, model.exit_position)]}" )
        return manhattan_distance(position, model.exit_position)  # Para Bomberman, la distancia a la salida
    else:
        return manhattan_distance(position, model.bomberman.pos)  # Para los globos, la distancia a Bomberman

def generar_posibles_movimientos(position, model):
    """Genera una lista de posibles movimientos (acciones) a partir de la posición actual."""
    # Considera todas las posiciones vecinas que no estén bloqueadas
    vecinos = get_neighbors_in_orthogonal_order(position, model)
    movimientos_validos = []
    
    for vecino in vecinos:
        cell_contents = model.grid.get_cell_list_contents(vecino)
        
        # Verificar que la lista no esté vacía antes de intentar acceder a su primer elemento
        if cell_contents:  # Si hay algo en la celda
            if not (isinstance(cell_contents[0], Block) or 
                    isinstance(cell_contents[0], Metal)):  # Bloques o metales no son válidos
                movimientos_validos.append(vecino)
        else:  # Si la celda está vacía
            movimientos_validos.append(vecino)
    
    print(f"Posibles movimientos desde {position}: {movimientos_validos}")
    return movimientos_validos

def heuristic_evaluation(position, goal, model):
    """
    Evaluate the desirability of the given game state.
    """
    from models.globe import Globe
    # Calculate Manhattan distance between Bomberman and the goal
    distance_to_goal = manhattan_distance(position, goal)
    
    # Penalize if Bomberman is surrounded or has fewer moves available
    bomberman_neighbors = model.grid.get_neighborhood(position, moore=False, include_center=False)
    valid_bomberman_moves = [
        pos for pos in bomberman_neighbors if is_valid_move(pos, model)
    ]
    mobility_penalty = -len(valid_bomberman_moves)
    
    # Calculate the impact of Globe agents
    globe_penalty = 0
    for globe in model.schedule.agents:
        if isinstance(globe, Globe):
            distance_to_bomberman = manhattan_distance(globe.pos, position)
            globe_penalty += max(0, 5 - distance_to_bomberman)  # Closer globes increase penalty
    
    # Combine heuristic components
    score = -distance_to_goal + mobility_penalty - globe_penalty
    
    return score