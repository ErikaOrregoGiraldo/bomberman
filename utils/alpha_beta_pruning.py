
from utils.shared.utils import  is_valid_move, manhattan_distance, is_valid_move_for_globe

def alpha_beta_search(position, goal, model, depth, alpha, beta, maximizing_player, bomberman_moves=[], enemy=None):
    from models.globe import Globe
    neighbors = model.grid.get_neighborhood(position, moore=False, include_center=False)
    valid_moves = [
        pos for pos in neighbors if is_valid_move(pos, model)
    ]
    
    if depth == 0 or position == goal:
        return heuristic_evaluation(position, goal, model), bomberman_moves

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
        globes_best_move = None
        for globe in model.schedule.agents:
            if isinstance(globe, Globe):
                globe.use_alpha_beta = True
                globe_neighbors = model.grid.get_neighborhood(globe.pos, moore=False, include_center=False)
                valid_globe_moves = [
                    pos for pos in globe_neighbors if is_valid_move_for_globe(pos, model)
                ]
                for move in valid_globe_moves:
                    #model.grid.move_agent(globe, move)
                    eval, _ = alpha_beta_search(position, goal, model, depth - 1, alpha, beta, True)
                    #model.grid.move_agent(globe, globe.pos)  # Undo move
                    if eval < min_eval:
                        min_eval = eval
                        if globe == enemy:
                            globes_best_move = move
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, globes_best_move

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
