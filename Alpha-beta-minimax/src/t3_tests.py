from t3_state import *
from t3_action import *
from t3_player import *
import unittest
import pytest

class T3GradingTests(unittest.TestCase):
    """
    Unit tests for validating the t3 agent's efficacy. Notes:
    - If this is the set of tests provided in the solution skeleton, it represents an
      incomplete set that you are expected to add to to adequately test your submission!
    - Your correctness score on the assignment will be assessed by a more complete,
      grading set of unit tests.
    - A portion of your style grade will also come from proper type hints; remember to
      validate your submission using `mypy .` and ensure that no issues are found.
    """
    
    # T3State tests for transitions
    # ---------------------------------------------------------------------------
    def test_t3_state_transitions_t0(self) -> None:
        state = [
            [6, 4, 1],
            [1, 1, 4],
            [4, 1, 0]
        ]
        t3state = T3State(False, state)
        transitions = set(t3state.get_transitions())
        result = {
            (T3Action(2, 2, 2),
             T3State(True, [
                 [6, 4, 1],
                 [1, 1, 4],
                 [4, 1, 2]
             ])),
            (T3Action(2, 2, 4),
             T3State(True, [
                 [6, 4, 1],
                 [1, 1, 4],
                 [4, 1, 4]
             ])),
            (T3Action(2, 2, 6),
             T3State(True, [
                 [6, 4, 1],
                 [1, 1, 4],
                 [4, 1, 6]
             ]))
        }
        self.assertEqual(result, transitions)
        
    def test_t3_state_transitions_t1(self) -> None:
        state = [
            [2, 1, 2],
            [1, 1, 0],
            [2, 0, 6]
        ]
        t3state = T3State(True, state)
        transitions = set(t3state.get_transitions())
        result = {
            (T3Action(2, 1, 1),
             T3State(False, [
                 [2, 1, 2],
                 [1, 1, 1],
                 [2, 0, 6]
             ])),
            (T3Action(2, 1, 3),
             T3State(False, [
                 [2, 1, 2],
                 [1, 1, 3],
                 [2, 0, 6]
             ])),
            (T3Action(2, 1, 5),
             T3State(False, [
                 [2, 1, 2],
                 [1, 1, 5],
                 [2, 0, 6]
             ])),
            (T3Action(1, 2, 1),
             T3State(False, [
                 [2, 1, 2],
                 [1, 1, 0],
                 [2, 1, 6]
             ])),
            (T3Action(1, 2, 3),
             T3State(False, [
                 [2, 1, 2],
                 [1, 1, 0],
                 [2, 3, 6]
             ])),
            (T3Action(1, 2, 5),
             T3State(False, [
                 [2, 1, 2],
                 [1, 1, 0],
                 [2, 5, 6]
             ]))
        }
        self.assertEqual(result, transitions)
    
    def test_t3_state_transitions_t2(self) -> None:
        state = [
            [0, 1, 0],
            [0, 1, 0],
            [2, 0, 6]
        ]
        t3state = T3State(True, state)
        transitions = set(t3state.get_transitions())
        self.assertEqual(15, len(transitions))
    
    # Tests with small number of transitions (good for just starting testing)
    # ---------------------------------------------------------------------------
    def test_t3_player_small_t0(self) -> None:
        state = [
            [6, 4, 1],
            [1, 1, 4],
            [4, 1, 0]
        ]
        t3state = T3State(False, state)
        action = choose(t3state)
        self.assertEqual(T3Action(2, 2, 6), action)
        
    def test_t3_player_small_t1(self) -> None:
        state = [
            [6, 4, 1],
            [1, 1, 4],
            [4, 0, 0]
        ]
        t3state = T3State(True, state)
        action = choose(t3state)
        self.assertEqual(T3Action(2, 2, 1), action)
    
    # Terminal states should return None for the action
    def test_t3_player_small_t2(self) -> None:
        state = [
            [6, 4, 0],
            [1, 1, 4],
            [0, 0, 6]
        ]
        t3state = T3State(True, state)
        action = choose(t3state)
        self.assertEqual(None, action)
        
    # Terminal states should return None for the action
    def test_t3_player_small_t3(self) -> None:
        state = [
            [6, 4, 2],
            [1, 1, 4],
            [1, 2, 1]
        ]
        t3state = T3State(True, state)
        action = choose(t3state)
        self.assertEqual(None, action)
    
    # Larger tests with multiple open tiles
    # ---------------------------------------------------------------------------
    def test_t3_player_t0(self) -> None:
        state = [
            [2, 1, 0],
            [0, 0, 0],
            [0, 0, 6]
        ]
        t3state = T3State(True, state)
        action = choose(t3state)
        self.assertEqual(T3Action(1, 1, 5), action)
        
    def test_t3_player_t1(self) -> None:
        state = [
            [2, 1, 0],
            [0, 5, 0],
            [0, 0, 0]
        ]
        t3state = T3State(False, state)

        action = choose(t3state)
        self.assertEqual(T3Action(2, 2, 6), action)
        
    def test_t3_player_t2(self) -> None:
        state = [
            [0, 1, 0],
            [0, 5, 0],
            [0, 0, 6]
        ]
        t3state = T3State(False, state)
        action = choose(t3state)
        self.assertEqual(T3Action(0, 0, 2), action)
        
    def test_t3_player_t3(self) -> None:
        state = [
            [0, 0, 0],
            [0, 5, 0],
            [0, 0, 0]
        ]
        t3state = T3State(False, state)
        action = choose(t3state)
        self.assertEqual(T3Action(0, 0, 2), action)
        
    def test_t3_player_t4(self) -> None:
        state = [
            [3, 0, 0],
            [0, 4, 0],
            [0, 0, 1]
        ]
        t3state = T3State(False, state)
        action = choose(t3state)
        self.assertEqual(T3Action(0, 1, 2), action)
        
    # Depth-tricky Cases
    # ---------------------------------------------------------------------------
    
    # [!] VERY IMPORTANT TODO:
    # Make your own test cases to make sure that the depth tiebreaking works as
    # intended -- invent some edge cases to make sure that depth of terminal is
    # being correctly minimized in your agent's decisions!
        
     # Test Case 1: Immediate Win vs. Delayed Win
    def test_t3_player_depth_tricky_t1(self) -> None:
        state = [
            [0, 0, 0],
            [2, 5, 1],
            [3, 0, 0]
        ]
        t3state = T3State(True, state)
        action = choose(t3state)
        self.assertEqual(T3Action(2, 0, 5), action)

    # Test Case 2: Block and Set Up Future Win
    def test_t3_player_depth_tricky_t2(self) -> None:
        state = [
            [3, 0, 0],
            [6, 0, 0],
            [0, 5, 1]
        ]
        t3state = T3State(False, state)
        action = choose(t3state)
        self.assertIn(action, [T3Action(0, 1, 4), T3Action(0, 2, 4)])

    # Test Case 3: Two-Step Lookahead to Win
    def test_t3_player_depth_tricky_t3(self) -> None:
        state = [
            [0, 0, 0],
            [6, 5, 0],
            [2, 0, 0]
        ]
        t3state = T3State(True, state)
        action = choose(t3state)
        self.assertEqual(T3Action(0, 0, 5), action)
    
if __name__ == '__main__':
    unittest.main()
    