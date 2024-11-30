from models.globe import Globe
from utils.shared.utils import get_neighbors_in_orthogonal_order, is_adjacent, reconstruct_path, is_valid_move

def alpha_beta_search(position, goal, model, depth, alpha, beta, maximizing_player, bomberman_moves=[]):
    neighbors = model.grid.get_neighborhood(position, moore=False, include_center=False)
    valid_moves = [
        pos for pos in neighbors if is_valid_move(pos, model)
    ]
    
    if depth == 0 or position == goal:
        return heuristic_evaluation(position, goal), move_history

    if maximizing_player:
        max_eval = float("-inf")
        best_move = None
        for move in valid_moves:
            #model.grid.move_agent(model.bomberman, move)
            eval, _ = alpha_beta_search(move, goal, model, depth - 1, alpha, beta, False, bomberman_moves)
            #model.grid.move_agent(model.bomberman, position)  # Undo move
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            if best_move is not None:
                bomberman_moves.append(best_move)
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for globe in model.schedule.agents:
            if isinstance(globe, Globe):
                globe_neighbors = model.grid.get_neighborhood(globe.pos, moore=False, include_center=False)
                valid_globe_moves = [
                    pos for pos in globe_neighbors if is_valid_move(pos, model)
                ]
                for move in valid_globe_moves:
                    #model.grid.move_agent(globe, move)
                    eval, _ = alpha_beta_search(position, goal, model, depth - 1, alpha, beta, True)
                    #model.grid.move_agent(globe, globe.pos)  # Undo move
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, None