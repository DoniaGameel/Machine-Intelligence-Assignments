from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = []

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # A list of points where state[i] is the position of car 'i'. 
        return list(self.cars)
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # Iterate through the cars tuple
        for i, car_position in enumerate(state):
            # Check if the current car's position matches the expected position in the slots dictionary
            # If the current car position isn't in the slots ==> return false
            # If the current car position match a slot but it isn't the expected slot for this car ==> return false
            if car_position not in self.slots or self.slots[car_position] != i:
                return False
        # If all cars match their expected positions ==> return True
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        actions = []
        # Iterate through the cars tuple
        for i in range(len(state)):
            # Iterate through the directions
            for direction in Direction:
                # Add the position vector to the position of the car to get the new position of the car
                new_position =  state[i] + direction.to_vector()
                # Check if the car can go this direction
                
                # first check it is a passage
                # second check it isn't another car position now
                # third check it isn't out of borders
                if (new_position in self.passages 
                    and 
                    new_position not in state 
                    and 
                    new_position != self.width and new_position != self.height and new_position != -1):
                    actions.append((i,direction.__str__()))

        return actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # Get the indes of the car that will take the action and get the direction it will go
        car_index,action_direction = action
        # Update the position of the car after applying the action in the direction specified in it
        state[car_index] += action_direction.to_vector()
        return state
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        car_index,action_direction = action
        # This car position
        current_position = state[car_index] 
        # the index of the car in the cars tuple depend on the rank of the employee
        # rank A ==> position 0 ==> cost 26
        # rank z ==> position 26 ==> cost 0
        # primary cost = 26 - index
        action_cost = 26 - car_index
        # check if the next position is slot and it isn't this car slot ==> add 100 to the primary cost
        next_position = current_position + action_direction.to_vector()
        if (next_position in self.slots and self.slots[next_position] != car_index):
            action_cost+=100
        return action_cost
        
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
