'''
CMSI 2130 - Homework 1
Author: <Samuel Winter>

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the A* pathfinder that solves the target practice problem.
'''
import queue
from maze_problem import MazeProblem
from dataclasses import *
from typing import *

from typing import List, Tuple, Optional, Dict, Set
import heapq

#>> [NO] The SearchTreeNode class is incredibly helpful for this problem, tracking location, parent, and you should add a cost and targets_left
# allows for all the information you need to be conveniently stored in individual nodes representing maze states.
@dataclass
class SearchTreeNode:
    """
    SearchTreeNodes contain the following attributes to be used in generation of
    the Search tree:

    Attributes:
        player_loc (tuple[int, int]):
            The player's location in this node.
        action (str):
            The action taken to reach this node from its parent (or empty if the root).
        parent (Optional[SearchTreeNode]):
            The parent node from which this node was generated (or None if the root).
    """
    player_loc: tuple[int, int]
    action: str
    parent: Optional["SearchTreeNode"]
    # TODO: Add any other attributes and method overrides as necessary!
    
def pathfind(problem: "MazeProblem") -> Optional[list[str]]:
    """
    The main workhorse method of the package that performs A* graph search to find the optimal
    sequence of actions that takes the agent from its initial state and shoots all targets in
    the given MazeProblem's maze, or determines that the problem is unsolvable.

    Parameters:
        problem (MazeProblem):
            The MazeProblem object constructed on the maze that is to be solved or determined
            unsolvable by this method.

    Returns:
        Optional[list[str]]:
            A solution to the problem: a sequence of actions leading from the 
            initial state to the goal (a maze with all targets destroyed). If no such solution is
            possible, returns None.
    """
    # TODO: Implement A* Graph Search for the Pathfinding Biathlon!
    #----------------------------------------------------------------------------------------------------# - Notes/Todo
    #   - Add Admissible heuristic function - Done
    #   - Goal test on expansion not generation - Done
    #   - Turn frontier into a priority queue - Done
    #----------------------------------------------------------------------------------------------------# - Current Problem
    #   - Root node revisitation --> Not Solved
    #----------------------------------------------------------------------------------------------------# - Helper Functions
    #   - get_inital_loc
    #   - get_inital_targets
    #   - get_transitions_cost --> action, player_loc
    #   - get_visible_targets_from_loc --> player_loc, targets_left
    #   - get_transitions --> player_loc, targets_left
    #----------------------------------------------------------------------------------------------------#
    # h(n) --> Min Distance from Targets + Alignment Bonus

    #>>[NO] Provide docstrings for ALL methods even helpers (-0.25)
    def heuristic(current_node: Tuple[int, int], target_locs: Set[Tuple[int, int]]) -> float: # WORKS 
        min_distance = float('inf')
        aligned_bonus = 0
        for target in target_locs:
            # Calculate Manhattan distance to each target
            distance = abs(current_node[0] - target[0]) + abs(current_node[1] - target[1])
            is_aligned = current_node[0] == target[0] or current_node[1] == target[1]
            # If aligned
            if is_aligned:
                aligned_bonus = 1
            # Update the minimum distance considering alignment
            min_distance = min(min_distance, distance - aligned_bonus)
        return min_distance


    # Retrace optimal path from I.S. to G.S.
    def retrace_path(Total_Nodes: Dict[Tuple[int, int], Tuple[Optional[Tuple[int, int]], Optional[str]]],
    goal_node: Tuple[int, int]) -> List[str]: # WORKS 
        path = []
        current_node = goal_node
        while current_node is not None:
            parent_node, actions = Total_Nodes[current_node]
            if actions:  # Make sure action taken to reach this node are valid
                if isinstance(actions, list):
                    # Add all actions except None
                    path.extend([action for action in actions if action is not None][::-1])
                elif actions is not None:
                    path.append(actions)
            current_node = parent_node
        return path[::-1]  # Reverse the path
    

    def shoot_if_optimal(targets: Set[Tuple[int, int]], visible_targets: Set[Tuple[int, int]]) -> Tuple[bool, Set[Tuple[int, int]]]: # WORKS
        targets_shot = set([])
        # Safety
        if len(visible_targets) > 0:
            # Shooting criteria
            if len(targets) >= 2 or len(targets) == len(visible_targets):
                # Remove the targets hit from the set of targets
                for target in visible_targets:
                    Target_Locs.remove(target)
                    targets_shot.add(target)
                    print("Shot", target, "from node", current_node)
                return True, targets_shot
        #>> [NO] Remove print statements before submission, it really slows down the code (-0.25)
        print("Did not shoot the following targets:", targets)
        return False, targets_shot
    

    root_node: Tuple[int, int] = problem.get_initial_loc()
    Target_Locs: Set[Tuple[int, int]] = problem.get_initial_targets()
    Total_Node_History: Dict[Tuple[int, int], Tuple[Optional[Tuple[int, int]], Union[None, str, List[str]]]] = {root_node: (None, [])}
    Total_Cost: Dict[Tuple[int, int], int] = {root_node: 0}
    frontier: List[Tuple[float, Tuple[int, int]]] = []
    

    heapq.heappush(frontier, (0, root_node))
    

    while frontier:
        print("New Nodes Added to Frontier:", frontier)
        # Pop expanding node
        current_priority, current_node = heapq.heappop(frontier)
        print("\n", "Current Node Location", current_priority, current_node)
        # Check if a shot is possible and optimal before moving
        visible_targets = problem.get_visible_targets_from_loc(current_node, Target_Locs)
        shot_made, targets_shot = shoot_if_optimal(Target_Locs, visible_targets)

        if shot_made and targets_shot:      
            # Get the previous actions for the current node
            previous_actions = Total_Node_History.get(current_node, (None, None))[1]
            # If previous_actions is None
            if previous_actions is None:
                previous_actions = []

            # If previous_actions is a single string
            elif isinstance(previous_actions, str):
                previous_actions = [previous_actions]

            previous_actions.append("S")

            # Append the shooting action
            Total_Node_History[current_node] = (Total_Node_History[current_node][0], previous_actions)
            Total_Cost[current_node] += problem.get_transition_cost("S", current_node)

            # Check Goal State
            if len(Target_Locs) == 0:
                # All targets hit, call retrace path
                actions = retrace_path(Total_Node_History, current_node) # 6/8 tests passed :(
                print("\n", "SHOT ALL TARGETS!", "\n", "Actions that led to goal state:", actions, "\n", "Total Node History:", Total_Node_History, "\n", "Total Cost History:", Total_Cost)
                return actions

        for direction, child in problem.get_transitions(current_node, Target_Locs).items():
            child_location = child['next_loc']
            child_cost = problem.get_transition_cost(direction, child_location)
            # g(child)
            g_child = Total_Cost[current_node] + child_cost
            # h(child)
            h_child = heuristic(child_location, Target_Locs)
            # f(child)
            f_child = g_child + h_child

            print("g(n) + h(n) = f(n)", g_child, "+", h_child, "=", f_child, "Child Location", child_location)
            if child_location not in Total_Cost or g_child <= Total_Cost[child_location] and child_location != current_node:
                heapq.heappush(frontier, (f_child, child_location))
                Total_Cost[child_location] = g_child
                Total_Node_History[child_location] = (current_node, [direction])

        if not frontier: # If every node has been expanded
            print(Total_Node_History)
            return None

# ===================================================
# >>> [NO] Summary
# A solid effort that shows strong command of coding
# fundamentals, but I think deviated too far from the
# prototypical approach to search that was given in
# the CW2 solution (which you could've began with).
# There's a lot to like in what you have above, but
# I think you also ran out of time to test your
# submission adequately and expose its logic problems
# on more general mazes. Not using the SearchTreeNode 
# created a lot of work for yourself, it's good to understand 
# the uses of class objects like the SearchTreeNode.
# Give yourself more time for future submissions and you'll be golden!
# ---------------------------------------------------
# >>> [NO] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
#
# [~] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [~] Proper docstrings provided for ALL methods
# [~] Logic is adequately simplified
# [X] Code repetition is kept to a minimum 
# ---------------------------------------------------
# Correctness:          68 / 100 (-2 / missed unit test)
# Mypy Penalty:        -2 (-2 if mypy wasn't clean)
# Style Penalty:       -0.5
# Total:                65.5 / 100
# ===================================================
