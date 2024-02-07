from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #  if the state is terminal, return 0
        if(self.mdp.is_terminal(state)):
            return 0
        # if now terminal
        # get the max utility over actions
        max_action_sum = float('-inf')  # Initialize with negative infinity to maximize
        for action in self.mdp.get_actions(state):
            action_sum = 0  # To add in it the sum of utilities of possible successors
            for successor,probability in self.mdp.get_successor(state,action).items():
                action_sum += probability * ( self.mdp.get_reward(state, action, successor) + self.discount_factor * self.utilities[successor])
            # Check if the current action_sum is greater than the current max_action_sum
            if action_sum > max_action_sum:
                max_action_sum = action_sum
        return max_action_sum
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        converge = True
        max_utility_change = 0
        new_utilities: Dict[S, float] = {}# The computed utilities
        for state in self.mdp.get_states():
            new_utilities[state] = self.compute_bellman(state)
            utility_change = new_utilities[state] - self.utilities[state]
            if(utility_change > max_utility_change):
                max_utility_change = utility_change
        self.utilities = new_utilities
        return max_utility_change <= tolerance
        

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        iteration = 0
        while iterations is None or iteration < iterations:
            iteration += 1
            if self.update(tolerance):
                break
        return iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #  if the state is terminal, return 0
        if(self.mdp.is_terminal(state)):
            return None
        # if now terminal
        # get the max utility over actions
        max_action_sum = float('-inf')  # Initialize with negative infinity to maximize
        result = None
        for action in self.mdp.get_actions(state):
            action_sum = 0  # To add in it the sum of utilities of possible successors
            for successor,probability in self.mdp.get_successor(state,action).items():
                action_sum += probability * ( self.mdp.get_reward(state, action, successor) + self.discount_factor * self.utilities[successor])
            # Check if the current action_sum is greater than the current max_action_sum
            if action_sum > max_action_sum:
                max_action_sum = action_sum
                result = action
        return result
     
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
