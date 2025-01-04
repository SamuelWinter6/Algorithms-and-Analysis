from constants import *
import copy

class MazeProblem:
    """
    MazeProblem class used to store all relevant information about the maze being solved
    by the Pathfinder, including the starting location of the player and the position of
    all other maze entities like mud tiles, targets, and walls.

    [!] Warning / Reminder: if an attribute or method begins with an underscore (_), it
    should not be accessed outside of this class. There are thus NO publicly accessible
    *attributes* to this class, but a variety of methods available for use.
    """
    
    # Constructor
    # ---------------------------------------------------------------------------
    def __init__(self, maze: list[str]) -> None:
        """
        Constructs a new pathfinding problem (finding the locations of any
        relevant maze entities) from a maze specified as a list of string rows.
        
        Parameters:
            maze (list[str]):
                A list of string rows of a rectangular maze consisting of the
                following traits:
                - A border of walls ("X"), with possibly others in the maze
                - Exactly 1 player starting position ("@")
                - Some number [0-infinity] of targets to shoot ("T")
                - Some number [0-infinity] of mud tiles
        """
        self._maze: list[list[str]] = [[r for r in row] for row in maze]
        self._targets: set[tuple[int, int]] = set()
        self._walls: set[tuple[int, int]] = set()
        self._mud: set[tuple[int, int]] = set()
        
        for (row_num, row) in enumerate(maze):
            for (col_num, cell) in enumerate(row):
                loc = (col_num, row_num)
                if cell == Constants.TARG_BLOCK:
                    self._targets.add(loc)
                if cell == Constants.WALL_BLOCK:
                    self._walls.add(loc)
                if cell == Constants.MUD_BLOCK:
                    self._mud.add(loc)
                if cell == Constants.PLR_BLOCK:
                    self._player_loc: tuple[int, int] = loc
        
    
    # Methods
    # ---------------------------------------------------------------------------
    def get_initial_loc (self) -> tuple[int, int]:
        """
        Returns the player's starting position in the maze ("@").
    
        Returns:
            tuple[int, int]:
                The player's starting location in the maze: (col, row) = (x, y).
        """
        return self._player_loc
    
    def get_initial_targets (self) -> set[tuple[int, int]]:
        """
        Returns the (possibly empty) set of targets that the player must shoot to
        reach a goal state.
        
        [!] Note: this method ALWAYS returns the starting set of target locations;
        you must record-keep separately any *remaining* targets of those unshot
        during the course of search.
        
        Returns:
            set[tuple[int, int]]:
                A set of each target's location in the maze: (col, row) = (x, y).
        """
        return copy.deepcopy(self._targets)
    
    def get_transition_cost(self, action: str, player_loc: tuple[int, int]) -> int:
        """
        Returns the cost of the given transition, which would normally be parameterized
        by the current state, action, and next state, except that all costs in the
        current maze problem are a function of only the action and next state, and so only
        those are required.
        
        Parameters:
            action (str):
                The action being taken in the current transition.
            player_loc (tuple[int, int]):
                The next-state's location of the player in the maze, i.e., having already
                taken the given action.
        
        Returns:
            int:
                The cost associated with this transition, which will be:
                    - 3 if moving ONTO a mud tile for the first time
                    - 2 if shooting (whether or not you're shooting from a mud tile)
                    - 1 otherwise
        """
        if action == "S": return Constants.SHOOTING_COST
        if player_loc in self._mud: return Constants.MUD_TILE_COST
        return 1
    
    def get_visible_targets_from_loc(self, player_loc: tuple[int, int], targets_left: set[tuple[int, int]]) -> set[tuple[int, int]]:
        """
        Returns the set of targets that would be hit by a player taking the shoot action from
        the given player_loc from amongst those targets remaining in the targets_left parameter.
        
        [!] Note: a target may only be shot if there are no walls between the player and the
        target in any of the 4 cardinal directions: Up, Down, Left, or Right (and in any number
        of tiles in those directions). Shots will also penetrate targets, possibly destroying
        multiple targets in the same direction.
        
        Parameters:
            player_loc (tuple[int, int]):
                The current location of the player / the location from which they are shooting.
            targets_left (set[tuple[int, int]])
                A set of location tuples indicating the positions of remaining targets to shoot.
        
        Returns:
            set[tuple[int, int]]:
                The set of target locations that would be hit by taking the shoot action from the
                given player_loc.
        """
        p_loc = player_loc
        targets_hit = set()
        for target in targets_left:
            if ((p_loc[0] == target[0] and not {(p_loc[0], row) for row in range(p_loc[1], target[1], 1 if p_loc[1] < target[1] else -1)}.intersection(self._walls)) or
                (p_loc[1] == target[1] and not {(col, p_loc[1]) for col in range(p_loc[0], target[0], 1 if p_loc[0] < target[0] else -1)}.intersection(self._walls))):
                targets_hit.add(target)
        return targets_hit
                
    def get_transitions(self, player_loc: tuple[int, int], targets_left: set[tuple[int, int]]) -> dict:
        """
        Returns a dictionary describing all possible transitions that a player may take from their
        given position. 
        
        Parameters:
            player_loc (tuple[int, int]):
                The current location of the player / the location from which they are shooting.
            targets_left (set[tuple[int, int]])
                A set of location tuples indicating the positions of remaining targets to shoot.
        
        Returns:
            dict:
                A dictionary whose keys are the possible actions from the given player_loc, with mapped
                values that describe the transition associated with that action, including:
                    - next_loc (tuple[int, int]): the location of the player after taking that action
                    - cost (int): the cost of this particular transition
                    - targets_hit (set[tuple[int, int]]): the set of targets hit in this transition
        
        Example:
            For example, if only the actions "S" and "U" were possible from the current player_loc of (3,3),
            we might see an output of:
            {
                "S": {next_loc: (3,3), cost: 2, targets_hit: {(3, 1)}},
                "U": {next_loc: (3,2), cost: 1, targets_hit: {}},
            }
        """
        new_player_locs = {action: (player_loc[0] + offset[0], player_loc[1] + offset[1]) for action, offset in Constants.MOVE_DIRS.items()}
        transitions = {
            action: {
                "next_loc": loc,
                "cost": self.get_transition_cost(action, loc),
                "targets_hit": self.get_visible_targets_from_loc(loc, targets_left) if action == "S" else set()
            } for action, loc in new_player_locs.items() if loc not in self._walls and loc not in targets_left
        }
        return transitions
    
    def test_solution(self, solution: Optional[list[str]]) -> dict:
        """
        Given a solution (a sequence of actions), tests to ensure that the provided series of steps
        does indeed solve the problem. It is assumed that the current MazeProblem *is* solvable in
        order to use this method.
        
        [!] IMPORTANT NOTES:
            - You will never call this method in your implementation of pathfinder -- it is for test
              purposes only and does nothing for you during the actual solution
            - See the unit tests module for how this method is used
        
        Parameters:
            solution (Optional[list[str]]):
                A sequence of actions that possibly solves the maze, e.g., ["S", "U", "S"]
        
        Returns:
            dict:
                A dictionary with 2 keys used by the test suite to validate the solution:
                    - is_solution (bool): whether or not the solution successfully hits all targets
                      in the maze
                    - cost (int): the total cost of all actions taken, or -1 if is_solution is False
        """
        remaining_targets = copy.deepcopy(self._targets)
        player_loc = self.get_initial_loc()
        cost = 0
        err_result = {"is_solution": False, "cost": -1}
        
        if solution is None:
            return err_result
        
        for action in solution:
            offset = Constants.MOVE_DIRS[action]
            player_loc = (player_loc[0] + offset[0], player_loc[1] + offset[1])
            if player_loc in self._walls or player_loc in remaining_targets:
                return err_result
            targets_hit = self.get_visible_targets_from_loc(player_loc, remaining_targets) if action == "S" else set()
            remaining_targets -= targets_hit
            cost += self.get_transition_cost(action, player_loc)
        
        return {"is_solution": len(remaining_targets) == 0, "cost": cost}
    
