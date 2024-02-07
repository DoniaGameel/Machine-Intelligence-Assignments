from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented
#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # Get the current player's turn
    agent = game.get_turn(state) 

    # Check if the state is terminal
    terminal, values = game.is_terminal(state) 
    if terminal:
        # If the given state is terminal, the returned action should be None.
        return values[agent], None

    # Check if the maximum depth is reached
    if max_depth == 0: 
        if agent == 0: 
            # it should a max node
            return heuristic(game, state, agent), None
        else: 
            # it should a min node (enemies player)
            return -heuristic(game, state, agent), None

    # Generate a list of (action, successor_state) pairs
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)] 

    # Perform Minimax search
    if agent == 0: 
        # Maximize over all states
        # The minimax value of a node is the utility (for MAX) of being in the corresponding state,
        value, _, action = max((minimax(game, state, heuristic, max_depth-1)[0], -index, action) 
                               for index, (action , state) in enumerate(actions_states))
    else: 
        # Minimize over all states
        value, _, action = min((minimax(game, state, heuristic, max_depth-1)[0], -index, action) 
                               for index, (action , state) in enumerate(actions_states))

    return value, action
# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return minmax_alpha_beta(game, state, heuristic, float('-inf') , float('inf'),max_depth)

def minmax_alpha_beta(game: Game[S, A], state: S, heuristic: HeuristicFunction, alpha, beta, max_depth: int = -1):
    # Get the current player's turn
    agent = game.get_turn(state) 

    # Check if the state is terminal
    terminal, values = game.is_terminal(state) 
    if terminal:
        # If the given state is terminal, the returned action should be None. 
        return values[agent], None

    # Check if the maximum depth is reached
    if max_depth == 0: 
        if agent == 0: 
            # it should a max node
            return heuristic(game, state, agent), None
        else: 
            # it should a min node
            return -heuristic(game, state, agent), None

    # Generate a list of (action, successor_state) pairs
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)] 

    # Perform Minimax search
    if agent == 0: 
        # Maximize 
        value = float('-inf')
        optimal_action = None
        # Loop over all (action, successor_state) pairs
        for _, (action, state) in enumerate(actions_states):
            # Recursive call of the function to maximize
            new_value, _ = minmax_alpha_beta(game, state, heuristic, alpha, beta, max_depth-1)
            if new_value > value:
                # Maximize the value
                value = new_value
                # update the optimal action
                optimal_action = action
            # β = the value of the best (i.e., lowest-value) choice we have found
            if value >= beta:
                return value, optimal_action
            # α = the value of the best (i.e., highest-value) choice we have found 
            # so far at any choice point along the path for MAX.
            alpha = max(alpha, value)
    else: 
        # Minimize
        value = float('inf')
        optimal_action = None
        # Loop over all (action, successor_state) pairs
        for _, (action, state) in enumerate(actions_states):
            # Recursive call of the function to minimize
            new_value, _ = minmax_alpha_beta(game, state, heuristic, alpha, beta, max_depth-1)
            if new_value < value:
                # Minimize the value
                value = new_value
                # update the optimal action
                optimal_action = action
            # α = the value of the best (i.e., highest-value) choice we have found 
            if value <= alpha:
                return value, optimal_action
            # β = the value of the best (i.e., lowest-value) choice we have found
            # so far at any choice pointalong the path for MIN.
            beta = min(beta, value)

    return value, optimal_action


# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return minmax_alpha_beta_move_ordering(game, state, heuristic, float('-inf'), float('inf'), max_depth)

def minmax_alpha_beta_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, alpha, beta, max_depth: int):
    # Get the current player's turn
    agent = game.get_turn(state)

    # Check if the state is terminal
    terminal, values = game.is_terminal(state)
    # If the given state is terminal, the returned action should be None. 
    if terminal:
        return values[0], None

    # Check if the maximum depth is reached
    if max_depth == 0:
        if agent == 0:
            # it should a max node
            return heuristic(game, state, agent), None
        else:
            # it should a min node
            return -heuristic(game, state, agent), None

    # Generate a list of (action, successor_state) pairs
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

    if agent == 0:
        # Sort actions based on a heuristic 
        # Order moves based on a heuristic
        actions_states.sort(key=lambda x: heuristic(game, x[1], 0), reverse= True)
        # Maximize 
        value = float('-inf')
        optimal_action = None
        # Loop over all (action, successor_state) pairs
        for _, (action, state) in enumerate(actions_states):
            # Recursive call of the function to mazimize
            new_value, _ = minmax_alpha_beta_move_ordering(game, state, heuristic, alpha, beta, max_depth - 1)
            if new_value > value:
                # Maximize the value
                value = new_value
                # update the optimal action
                optimal_action = action
            # β = the value of the best (i.e., lowest-value) choice we have found
            if value >= beta:
                return value, optimal_action
            # α = the value of the best (i.e., highest-value) choice we have found 
            # so far at any choice point along the path for MAX.
            alpha = max(alpha, value)
    else:
        # Sort actions based on a heuristic 
        # Order moves based on a heuristic
        actions_states.sort(key=lambda x: heuristic(game, x[1], 0))
        # Minimize
        value = float('inf')
        optimal_action = None
        # Loop over all (action, successor_state) pairs
        for _, (action, state) in enumerate(actions_states):
            # Recursive call of the function to minimize
            new_value, _ = minmax_alpha_beta_move_ordering(game, state, heuristic, alpha, beta, max_depth - 1)
            if new_value < value:
                # Minimize the value
                value = new_value
                # update the optimal action
                optimal_action = action
            # α = the value of the best (i.e., highest-value) choice we have found 
            if value <= alpha:
                return value, optimal_action
            # β = the value of the best (i.e., lowest-value) choice we have found
            # so far at any choice pointalong the path for MIN.
            beta = min(beta, value)

    return value, optimal_action

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # Get the current player's turn
    agent = game.get_turn(state)

    # Check if the state is terminal
    terminal, values = game.is_terminal(state)
    # If the given state is terminal, the returned action should be None.
    if terminal: 
        return values[0], None

    # Check if the maximum depth is reached
    if max_depth == 0:
        if agent == 0:
            # it should a max node
            return heuristic(game, state, agent), None
        else:
            # The monsters
            return -heuristic(game, state, agent), None
        
    # Generate a list of (action, successor_state) pairs
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

    if agent == 0:  # Max node
        value, _, action = max((expectimax(game, state, heuristic, max_depth - 1)[0], -index, action)
                               for index, (action, state) in enumerate(actions_states))
    else:  # Chance node
        # For the chance nodes, all the children has the same probability.
        # The probability of a child is 1 / (the number of children).
        num_children = len(actions_states)
        value = sum(expectimax(game, state, heuristic, max_depth - 1)[0] for _, state in actions_states) / num_children
        action = None  # No specific action at chance nodes

    return value, action
