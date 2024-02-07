from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq
import queue

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # Define a queue for the frontier
    frontier = deque()
    # Define a forntier set to check if a node is in the forntier
    # Use it for the check search to speed up the problem
    frontier_set = set()
    # Add the initial state to the frontier with an empty path
    frontier.append((initial_state, []))
    # Add the initial state to the fast frontier (the set)
    frontier_set.add(initial_state)
    # Define the explored set as an empty set
    explored = set()
    # Loop until the frontier is empty or a solution is found
    while(frontier):
        # Choose the shallowest node and its path in the frontier 
        state, actionList = frontier.popleft()
        # Add the selected node to the explored set
        explored.add(state)

        # Loop over all actions (children) of the current node
        for action in problem.get_actions(state):
            # get the state resulting from applying the current action
            successor = problem.get_successor(state,action)
            # Check the goal before inserting it in the frontier to speed up the search
            if problem.is_goal(successor):
                    return actionList + [action]
            # check it isn't in the explored ==> search graph
            # check it isn't in the frontier to get the shallowest path
            if (successor not in explored) and (successor not in frontier_set):
                frontier.append((successor, actionList + [action]))
                # Add the successor to the fast frontier
                frontier_set.add(successor)
    #If no solution is found return None
    return None

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # Define a queue for the frontier
    frontier = deque()
    # Add the initial state to the frontier with an empty path
    frontier.append((initial_state, []))
    # Define the explored set as an empty set
    explored = set()

    # Loop until the frontier is empty or a solution is found
    while(frontier):
        # Choose the last inserted node
        state, actionList = frontier.pop()
        # Check the node hasn't been explored before ==> graph searc
        if state not in explored:
            # If the node is a goal ==> return the solution
            if problem.is_goal(state):
                return actionList
            # Add the selected node to the explored set
            explored.add(state)
            # get all children of the current node
            for action in problem.get_actions(state):
                successor = problem.get_successor(state,action)
                # Add the childs to the frontier stack
                frontier.append((successor, actionList + [action]))
    #If no solution is found return None
    return None
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # Define a priority queue as a list of tuples (cost, state, actionList)
    # Add the initial state to the frontier
    frontier = [(0, initial_state, [])]
    # Define the explored set as an empty set
    explored = set()
    # Loop until the frontier is empty or a solution is found
    while frontier:
        # Get the node with least cost value
        state_index = min(range(len(frontier)), key=lambda i: frontier[i][0])
        # Get the actionlist and cost related to this node
        old_cost, state, actionList = frontier.pop(state_index)
        # Check the node hasn't been explored before
        if state not in explored:
            # If the node is a goal ==> return the solution
            if problem.is_goal(state):
                return actionList
            # Add the selected node to the explored set
            explored.add(state)

            # Get all children of the current node
            for action in problem.get_actions(state):
                # Get the action of accessing this successor from this path
                action_cost= old_cost + problem.get_cost(state, action)
                successor = problem.get_successor(state,action)
                # Check if the node isn't in the explored ==> graph search
                if successor not in explored:
                    # If the node is in the frontier with higher cost ==> The node with least cost will be explored first
                    # If the node is not in the frontier ==> add it to the frontier
                    frontier.append((action_cost, successor, actionList + [action]))

    return None
'''
# This is old version of the function which causes time out in one test case
def UniformCostSearch2(problem: Problem[S, A], initial_state: S) -> Solution:
    # Define a priority queue as dictionary for the frontier
    frontier = {}
    # Add the initial state to the frontier with an empty path and 0 cost
    frontier[initial_state] = [[],0]
    # Define the explored set as an empty set
    explored = set()
    # Loop until the frontier is empty or a solution is found
    while(frontier):
        # Get the node with least cost value
        state = min(frontier, key=lambda key: frontier[key][1])
        # Get the actionlist and cost related to this node
        actionList,old_cost = frontier[state]
        # Remove it to get the queue effect
        del frontier[state]
        # Check the node hasn't been explored before
        if state not in explored:
            # If the node is a goal ==> return the solution
            if problem.is_goal(state):
                return actionList
            # Add the selected node to the explored set
            explored.add(state)
            # get all children of the current node
            for action in problem.get_actions(state):
                # Get the action of accessing this successor from this path
                action_cost= old_cost + problem.get_cost(state, action)
                successor = problem.get_successor(state,action)
                # Check the node isn't in the frontier or the explored
                if (((successor not in explored) and (successor not in frontier))
                    #If the node in the frontier ==> Check if the new cost is less than the old cost
                or (successor in frontier and (action_cost < frontier[successor][1]))):
                    frontier[successor]= [actionList + [action],action_cost]

    return None
'''
def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # Define a priority queue as a list of tuples (g(n)+h(n), state, actionList)
    # Add the initial state to the frontier
    frontier = [(0 + heuristic(problem,initial_state), initial_state, [])]
    # Define the explored set as an empty set
    explored = set()

    # Loop until the frontier is empty or a solution is found
    while frontier:
        # Get the node with least g(n)+h(n) value
        state_index = min(range(len(frontier)), key=lambda i: frontier[i][0])
        # Get the actionlist and cost related to this node
        old_cost, state, actionList = frontier.pop(state_index)
        # Check the node hasn't been explored before ==> graph search
        if state not in explored:
            # If the node is a goal ==> return the solution
            if problem.is_goal(state):
                return actionList
            # Add the selected node to the explored set
            explored.add(state)

            # Get all children of the current node
            for action in problem.get_actions(state):
                # Get the action of accessing this successor from this path
                # heuristic isn't accumulated ==> subtract the last heuristic from the cost 
                action_cost= old_cost - heuristic(problem, state) + problem.get_cost(state, action) 
                successor = problem.get_successor(state,action)

                # Check if the node isn't in the explored ==> graph searc
                if successor not in explored:
                    # If the node is in the frontier with higher cost ==> The node with least cost will be explored first
                    # If the node is not in the frontier ==> add it to the frontier
                    frontier.append((action_cost + heuristic(problem,successor), successor, actionList + [action]))

    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # Define a priority queue as a list of tuples (cost, state, actionList)
    frontier = [(heuristic(problem,initial_state), initial_state, [])]
    # Define the explored set as an empty set
    explored = set()

    # Loop until the frontier is empty or a solution is found
    while frontier:
        # Get the node with least cost value
        state_index = min(range(len(frontier)), key=lambda i: frontier[i][0])
        # Get the actionlist and cost related to this node
        _, state, actionList = frontier.pop(state_index)
        # Check the node hasn't been explored before ==> graph search
        if state not in explored:
            # If the node is a goal ==> return the solution
            if problem.is_goal(state):
                return actionList
            # Add the selected node to the explored set
            explored.add(state)

            # Get all children of the current node
            for action in reversed(problem.get_actions(state)):
                successor = problem.get_successor(state,action)
                # Check if the node isn't in the explored
                if successor not in explored:
                    # If the node is in the frontier with higher cost ==> The node with least cost will be explored first
                    # If the node is not in the frontier ==> add it to the frontier
                    frontier.append((heuristic(problem,successor), successor, actionList + [action]))

    return None