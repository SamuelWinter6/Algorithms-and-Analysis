"""
Artificial Intelligence responsible for playing the game of T3!
Implements the alpha-beta-pruning mini-max search algorithm
"""
from dataclasses import *
from typing import *
from t3_state import *
    
def choose(state: "T3State") -> Optional["T3Action"]:
    """
    Main workhorse of the T3Player that makes the optimal decision from the max node
    state given by the parameter to play the game of Tic-Tac-Total.
    
    [!] Remember the tie-breaking criteria! Moves should be selected in order of:
    1. Best utility
    2. Smallest depth of terminal
    3. Earliest move (i.e., lowest col, then row, then move number)
    
    You can view tiebreaking as something of an if-ladder: i.e., only continue to
    evaluate the depth if two candidates have the same utility, only continue to
    evaluate the earliest move if two candidates have the same utility and depth.
    
    Parameters:
        state (T3State):
            The board state from which the agent is making a choice. The board
            state will be either the odds or evens player's turn, and the agent
            should use the T3State methods to simplify its logic to work in
            either case.
    
    Returns:
        Optional[T3Action]:
            If the given state is a terminal (i.e., a win or tie), returns None.
            Otherwise, returns the best T3Action the current player could take
            from the given state by the criteria stated above.
    """
    # [!] TODO! Implement alpha-beta-pruning minimax search!
    def utility(state: T3State, is_maximizing_player: bool, depth: int) -> float:
        '''
        Calculates the utility of a given state for the minimax algorithm.
        
        Parameters:
            state (T3State):
                The current state of the game.
            is_maximizing_player (bool):
                A boolean indicating if the current player is maximizing or minimizing.
            depth (int):
                The current depth in the game tree.
            
        Returns:
            float:
                A float representing the utility score of the state. Negative values favor the minimizing player, 
                positive values favor the maximizing player, and 0 represents a neutral state.
                Closer wins or losses are weighted by depth to prefer faster victories or delayed defeats.
        '''
        if is_maximizing_player:
            if state.is_win():
                return -1 - depth # weighted utility score, pefering closer solutions in the game tree
            else:
                return 0
        else:
            if state.is_win():
                return 1 + depth
            else:
                return 0

    def minimax(state: T3State, depth: int, alpha: float, beta: float, is_maximizing_player: bool) -> Tuple[float, Optional[T3Action]]:
        '''
        Implements the minimax algorithm with alpha-beta pruning to find the best move.
        
        Parameters:
            state (T3State):
                The current state of the game.
            depth (int):
                The maximum depth to search in the game tree.
            alpha (float):
                The current alpha value for alpha-beta pruning, representing the best already explored option along the path to the root for the maximizer.
            beta (float):
                The current beta value for alpha-beta pruning, representing the best already explored option along the path to the root for the minimizer.
            is_maximizing_player (bool):
                A boolean indicating if the current player is maximizing or minimizing.
            
        Returns:
            tuple(float, Optional[T3Action]):
                A tuple containing the best evaluated score and the corresponding best action that leads to that outcome.
                If no action is available (e.g., in terminal states), the action will be None.
        '''
        if depth == 0 or state.is_win() or state.is_tie():
            return utility(state, is_maximizing_player, depth), None
        if is_maximizing_player:
            max_eval = float("-inf")
            best_action = None
            for action, next_state in state.get_transitions():
                eval, _ = minimax(next_state, depth-1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_action = action
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_action
        else:
            min_eval = float("inf")
            best_action = None
            for action, next_state in state.get_transitions():
                eval, _ = minimax(next_state, depth-1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_action = action
                beta = min(beta, eval)
                if alpha >= beta:
                    break
            return min_eval, best_action

    # Choose the action with the best outcome
    _, best_action = minimax(state, 5, float("-inf"), float("inf"), True)

    # If solution, return
    if best_action:
        print("\n Best Action:", best_action)
        return best_action
    
    print("\n Best Action was None")
    return None