from dataclasses import *
from typing import *
from t3_action import *
import copy
import itertools

@dataclass
class T3State:
    """
    Representation of the T3 grid board-state, which player's turn (odds / evens),
    and ability to obtain the actions and transitions possible (among other state
    utility methods).
    """
    
    # The maximum numerical move available to either player, though odds will get
    # all odds from 1 to MAX_MOVE (inclusive), and evens all even numbers
    MAX_MOVE = 6
    # The sum along any row, column, or diagonal that constitutes a win condition
    WIN_TARGET = 13
    # The default size of the game board, though can be arbitrarily larger
    DEFAULT_SIZE = 3
    
    def __init__(self, odd_turn: bool, state: Optional[list[list[int]]]):
        """
        Constructs a new T3 Board State from either the one provided,
        or the default, which will be a 3x3 empty grid. Which players turn
        is also specified.
        
        Parameters:
            odd_turn (bool):
                Whether or not this is the odd player's turn (and if False,
                therefore, it is the even player's)
            state (Optional[list[list[int]]]):
                The board state, which must be a square N x N grid
        """
        if state:
            self._state: list[list[int]] = state 
        else:
            self._state = [[0]*T3State.DEFAULT_SIZE for x in range(T3State.DEFAULT_SIZE)]
        self._rows: int = len(self._state)
        self._cols: int = len(self._state[0])
        self._odd_turn: bool = odd_turn
    
    def is_valid_action(self, act: "T3Action") -> bool:
        """
        Determines if the provided action is legal within this state, as decided by
        whether or not the col and row are in range of the board, that spot is not
        occupied, and whether the move number is within the set of allowable player
        actions on the given turn.
        
        Parameters:
            act (T3Action):
                The action being judged for legality
                
        Returns:
            Whether or not the given act is legal in this board state
        """
        return act.col() >= 0 and act.col() < self._rows and \
               act.row() >= 0 and act.row() < self._cols and \
               act.move() >= 0 and act.move() <= T3State.MAX_MOVE and \
               act.move() % 2 == 1 if self._odd_turn else act.move() % 2 == 0 and \
               self._state[act.row()][act.col()] == 0
    
    def get_next_state(self, act: Optional["T3Action"]) -> "T3State":
        """
        Returns the next state representing the transition from the current state (self)
        having taken the given action. E.g., if the player is at location (1,1) and
        moves Right (assuming there's no wall blocking them), then the returned state is
        that which has them in the position (2,1).
        
        Parameters:
            act (Optional[T3Action]):
                The T3Action representing the move chosen by the agent in the current state.
                [!] If None or an invalid action (e.g., runs into a wall), raises an error.
        
        Returns:
            T3State:
                The next state that would be reached from taking the given act in the
                current state.
        """
        if act is None or not self.is_valid_action(act):
            raise ValueError("[X] Chosen action " + str(act) + " is invalid!")
        
        next_state = copy.deepcopy(self)
        next_state._state[act.row()][act.col()] = act.move()
        next_state._odd_turn = not next_state._odd_turn
        return next_state
    
    def get_open_tiles(self) -> list[tuple[int, int]]:
        """
        Returns a list of (x,y) = (c,r) tuples indicating the open tiles into which
        players may place numbers in the current board state (i.e., returns the
        locations of all 0s on the board).
        
        Returns:
            list[tuple[int, int]]:
                The list of (c,r) tuples of all 0s / open tiles on the board.
        """
        tile_pos = itertools.product(range(self._cols), range(self._rows))
        return [(c, r) for (c, r) in tile_pos if self._state[r][c] == 0]
    
    def get_moves(self) -> list[int]:
        """
        Returns the list of "move" options for any open tile available to the 
        player whose turn it is in the current state.
        
        Examples:
            Odd player's turn in self:     [1, 3, 5]
            Even player's turn in self:    [2, 4, 6]
        
        Returns:
            list[int]:
                The list of int moves available to the player in any open tile.
        """
        return [move for move in range(1, T3State.MAX_MOVE+1) if \
                (self._odd_turn and move % 2 == 1) or \
                (not self._odd_turn and move % 2 == 0)]
    
    def is_win(self) -> bool:
        """
        Returns whether or not the current state is in a win condition, i.e.,
        at least one row, col, or diagonal has numbers that sum to WIN_TARGET.
        
        [!] Note: does not necessarily tell you *which* player won, as this state
        will represent the terminal *following* the player who made the winning move.
        
        Returns:
            bool:
                Whether or not the current state is a terminal win state.
        """
        rows = [sum([self._state[i][j] for i in range(self._rows)]) for j in range(self._cols)]
        cols = [sum([self._state[j][i] for i in range(self._cols)]) for j in range(self._rows)]
        diag1 = [sum([self._state[x][x] for x in range(self._rows)])]
        diag2 = [sum([self._state[x][self._cols - 1 - x] for x in range(self._rows)])]
        return T3State.WIN_TARGET in (rows + cols + diag1 + diag2)
    
    def is_tie(self) -> bool:
        """
        Returns whether or not the current state is a tie condition, i.e., the
        state is not a win for any player, and there are no more possible moves.
        
        Returns:
            bool:
                Whether or not the state is a tie.
        """
        return not self.is_win() and not self.get_open_tiles()
    
    def __str__(self) -> str:
        return "\n".join([str(r) for r in self._state])
    
    def __eq__(self, other: Any) -> bool:
        if other is None: return False
        if not isinstance(other, T3State): return False
        return self._state == other._state and self._odd_turn == other._odd_turn
    
    def __hash__(self) -> int:
        return hash((str(self._state), self._odd_turn))
    
    # DO NOT TOUCH ABOVE THIS LINE! Your work is below!
    # ---------------------------------------------------------------------------
    
    def get_transitions(self) -> Iterator[tuple["T3Action", "T3State"]]:
        """
        Returns a Generator of the transitions from this state, viz., tuples of
        T3Actions mapped to the next T3States they lead to from the current state.
        
        [!] Note: for convenience in the T3Player, should generate tuples in order
        of the T3Action tiebreaking order!
        
        Example:
            [6, 4, 1]
            [1, 1, 4]
            [4, 1, 0]
        
            If even's turn, there is 1 open tiles in which to move, with the
            following combos that would be generated (note each item is a tuple of
            the format (T3Action, T3State)):
            
            (T3Action(2, 2, 2),
             T3State(True, [
                 [6, 4, 1],
                 [1, 1, 4],
                 [4, 1, 2]
             ]))
            (T3Action(2, 2, 4),
             T3State(True, [
                 [6, 4, 1],
                 [1, 1, 4],
                 [4, 1, 4]
             ]))
            (T3Action(2, 2, 6),
             T3State(True, [
                 [6, 4, 1],
                 [1, 1, 4],
                 [4, 1, 6]
             ]))
        
        Returns:
            Iterator[tuple["T3Action", "T3State"]]:
                A Generator of transition tuples of the format (T3Action, T3State)
        """
        # [!] TODO! (delete these next 2 lines to start)
        open_tiles = self.get_open_tiles()  # Get all open tiles where a move can be made
        moves = self.get_moves()  # Get the set of valid moves for the current player

        for tile in open_tiles:
            for move in moves:
                action = T3Action(tile[0], tile[1], move)  # Create an action for each move
                if self.is_valid_action(action):  # Ensure the action is valid
                    next_state = self.get_next_state(action)  # Generate the next state from that action
                    yield (action, next_state)  # Yield the tuple of action and resulting state

        # return
        # yield
        