from dataclasses import *
from typing import *

@dataclass
class T3Action:
    """
    T3Actions are agent-specified manipulations on the game
    board such that they indicate which column, row, (both 0
    indexed), and number / move they would like to make.
    T3Actions implement Comparable and are ordered in ascending
    column, row, then move number.
    """
    
    _col: int
    _row: int
    _move: int
    
    def col(self) -> int:
        """
        Returns:
            int:
                The column in which this action is placed
        """
        return self._col
    
    def row(self) -> int:
        """
        Returns:
            int:
                The row in which this action is placed
        """
        return self._row
    
    def move(self) -> int:
        """
        Returns:
            int:
                The number that is being placed on the board at this
                action's location; will be different for the odds vs.
                evens player
        """
        return self._move
    
    def __str__(self) -> str:
        return "(" + str(self._col) + "," + str(self._row) + ") = " + str(self._move)
    
    def __lt__(self, other: "T3Action") -> bool:
        """
        [!] Ordering for T3Actions that abides by the spec's action tiebreaking rule
        """
        col_diff = self._col - other._col
        row_diff = self._row - other._row
        mov_diff = self._move - other._move
        if not col_diff == 0: return col_diff < 0
        if not row_diff == 0: return row_diff < 0
        return mov_diff < 0
    
    def __eq__(self, other: Any) -> bool:
        if other is None: return False
        if not isinstance(other, T3Action): return False
        return self._col == other._col and self._row == other._row and self._move == other._move
    
    def __hash__(self) -> int:
        return hash((self._col, self._row, self._move))
