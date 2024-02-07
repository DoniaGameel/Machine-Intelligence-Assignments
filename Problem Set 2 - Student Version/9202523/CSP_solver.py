from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    # Loop over all constraints
    for constraint in problem.constraints:
        # Get the binary constraints
        if isinstance(constraint, BinaryConstraint):
            # Check the assigned_variable is a variable in this constraint
            if assigned_variable in constraint.variables:
                # Get the other variable in the constraint
                the_other_variable = constraint.get_other(assigned_variable)
                # Check if the_other_variable has a domain
                # If the other variable has no domain (in other words, it is already assigned), skip this constraint
                if the_other_variable in domains:
                    # Update the other variable's domain 
                    # to only include the values that satisfy the binary constraint with the assigned variable.
                    
                    # 1- Get the values of the other variable
                    values = domains[the_other_variable]
                    new_values= set()
                    # 2- Loop over values
                    for value in values:
                        # 3- Assign the value to the other variable
                        assignment: Dict[str, Any] = {}
                        assignment[the_other_variable] = value
                        # 4- Add the assigned_value and the assigned_variable to the Assignment dictionary
                        assignment[assigned_variable] = assigned_value
                        # 5- Check this assignment satisfy the binary constraint
                        if constraint.is_satisfied(assignment):
                            # The value satisfy the binary constraint
                            new_values.add(value)
                    # Update the values of the variable
                    domains[the_other_variable] = new_values
                    # Check if the new domain became empty ==> return false
                    if not new_values:
                        return False
    return True
                    




# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    # List all domains that can result fro the different values
    new_domains: List[Dict[str,Dict[str, set]]] =[]
    # Get all values of the variable_to_assign
    values = domains[variable_to_assign]
    # Loop over alll values of the variable_to_assign
    for value_to_assign in values:
        # the domains result from the current value
        value_domains: Dict[str, set] = {}
        # Loop over all constraints
        for constraint in problem.constraints:
            # Get the binary constraints
            if isinstance(constraint, BinaryConstraint):
                # Check the assigned_variable is a variable in this constraint
                if variable_to_assign in constraint.variables:
                    # Get the other variable in the constraint
                    the_other_variable = constraint.get_other(variable_to_assign)
                    # Check if the_other_variable has a domain
                    # If the other variable has no domain (in other words, it is already assigned), skip this constraint
                    if the_other_variable in domains:
                        # Update the other variable's domain 
                        # to only include the values that satisfy the binary constraint with the assigned variable.
                        
                        # 1- Get the values of the other variable
                        values = domains[the_other_variable]
                        new_values= set()
                        # 2- Loop over values
                        for value in values:
                            # 3- Assign the value to the other variable
                            assignment: Dict[str, Any] = {}
                            assignment[the_other_variable] = value
                            # 4- Add the assigned_value and the assigned_variable to the Assignment dictionary
                            assignment[variable_to_assign] = value_to_assign
                            # 5- Check this assignment satisfy the binary constraint
                            if constraint.is_satisfied(assignment):
                                # The value satisfy the binary constraint
                                new_values.add(value)
                        # Update the values of the variable
                        value_domains[the_other_variable] = new_values
        # Add the domain resulting from this value to the domains list
        new_domains.append({value_to_assign: value_domains})
    # Get the domain that has most available values   
                   
    # 1- Calculate the sum of lengths of all sets in each dictionary
    # To get the number of remaining values
    sum_values = [
        (key, sum(len(s) for s in inner_dict.values()))
        for d in new_domains
        for key, inner_dict in d.items()
    ]
    # 2- Sort the values based on the maximum sum and the minimum value_to_assign
    sorted_values = sorted(sum_values, key=lambda x: (-x[1], x[0]))

    # 3- Extract the value_to_assign from the sorted list
    result_list = [key for key, _ in sorted_values]

    return result_list


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    # Unary constraints handling using 1-Consistency before starting the backtracking search.
    if not one_consistency(problem):
        # If Unary constraints aren't satidfied ==> No solution ==> Null
        return None
    # If Unary constraints are satidfied ==> Call BackTrack to get the solution if exists
    return BackTrack(problem=problem,assignment={},domains=problem.domains) 
  
# BackTrack algorithm
def BackTrack(problem: Problem, assignment: Assignment,domains: Dict[str, set]) -> Optional[Assignment]:  
    # Check if the assignment we reached is complete   
    if problem.is_complete(assignment):
        return assignment
    # Select unassigned variable to start assigning it using minimum_remaining_values heuristic
    variable = minimum_remaining_values(problem=problem, domains=domains)
    # Sort the variables that the variable can take based on least_restraining_values heurisitic
    values = least_restraining_values(problem=problem,variable_to_assign=variable,domains=domains)
    # Loop over all values
    for value in values:
        # Get copy of domins to avoid modifying the original domains
        domains_copy = domains.copy()
        # Get copy of assignment to avoid modifying the original assignment
        assignment_copy = assignment.copy()
        # Assign this value to the variable
        assignment_copy[variable] = value
        # Delete the assigned variable from the domain ==> the domain has only the variables that weren't assigned
        domains_copy.pop(variable)

        # This function return False if it is impossible to solve the problem after the given assignment, and True otherwise.
        # It checks the constraints of the variables with the other variables after assigning it the current value
        if (forward_checking(problem=problem,assigned_variable=variable,assigned_value=value,domains=domains_copy)):
            # Recursive call the function to get possible assignments for the remaining values or return no solution
            result = BackTrack(problem,assignment_copy,domains_copy)
            # If there is a solution ==> return it (the first solution)
            if result is not None:
                return result
    # No solution ==> return None
    return None
    