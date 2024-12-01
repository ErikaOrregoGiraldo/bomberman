from models.block import Block
from models.metal import Metal
from utils.shared.utils import get_neighbors_in_orthogonal_order

def poda_alpha_beta_search(start, goal, model, depth, alpha, beta, is_maximizing, visited):
    # Caso base: profundidad máxima alcanzada o se llega al objetivo
    if depth == 0 or start == goal:
        return [start]

    # Obtener movimientos válidos evitando ciclos
    posibles_movimientos = model.grid.get_neighborhood(start, moore=False, include_center=False)
    posibles_movimientos = [move for move in posibles_movimientos if model.grid.is_cell_empty(move) and move not in visited]

    # Si no hay movimientos posibles, quedarse en la posición actual
    if not posibles_movimientos:
        return [start]

    visited.add(start)  # Marcar la posición actual como visitada

    if is_maximizing:
        max_eval = float('-inf')
        best_path = []

        for movimiento in posibles_movimientos:
            sub_path = poda_alpha_beta_search(movimiento, goal, model, depth - 1, alpha, beta, False, visited.copy())
            heuristica_value = heuristica_bomberman(movimiento, model)

            eval = heuristica_value + sum(heuristica_bomberman(pos, model) for pos in sub_path)
            if eval > max_eval:
                max_eval = eval
                best_path = [start] + sub_path

            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Poda beta

        return best_path

    else:
        min_eval = float('inf')
        best_path = []

        if(start == model.bomberman.pos):
            print("Globo llegó a bomberman")
            model.finish_game()


        for movimiento in posibles_movimientos:
            sub_path = poda_alpha_beta_search(movimiento, goal, model, depth - 1, alpha, beta, True, visited.copy())
            heuristica_value = heuristica_globe(movimiento, model.bomberman.pos)

            eval = heuristica_value + sum(heuristica_globe(pos, model.bomberman.pos) for pos in sub_path)
            if eval < min_eval:
                min_eval = eval
                best_path = [start] + sub_path

            beta = min(beta, eval)
            if beta <= alpha:
                break  # Poda alpha

        return best_path



def heuristica_bomberman(position, model):
    """
    Calcula el valor heurístico de una posición basada en la distancia al objetivo y otras penalizaciones.
    Args:
        position (tuple): Posición evaluada.
        model (BombermanModel): Instancia del modelo.
        is_maximizing (bool): Si la evaluación es para un jugador maximizador o minimizador.
    Returns:
        int: Valor heurístico de la posición.
    """
    distance_to_goal = abs(position[0] - model.exit_position[0]) + abs(position[1] - model.exit_position[1])
    visited_penalty = 1000 if position in model.visited_numbers else 0  # Penalización fuerte por ciclos
    return -distance_to_goal - visited_penalty

def heuristica_globe(position, bomberman_pos):
    """
    Calcula el valor heurístico de una posición basada en la distancia al objetivo y otras penalizaciones.
    Args:
        position (tuple): Posición evaluada.
        model (BombermanModel): Instancia del modelo.
        is_maximizing (bool): Si la evaluación es para un jugador maximizador o minimizador.
    Returns:
        int: Valor heurístico de la posición.
    """
    return abs(position[0] - bomberman_pos[0]) + abs(position[1] - bomberman_pos[1])


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