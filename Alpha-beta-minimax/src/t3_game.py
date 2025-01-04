from t3_state import *
from t3_action import *
from t3_player import *
import unittest
import pytest

# The beginning board state; can be customized for debugging or
# playing on non-standard boards like a 4x4 battlefied extreme
# (though beware that the AI will take a long time to think on
# larger board states)
START_STATE = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# Whether or not odds places the first number on the board
ODDS_STARTS = True
# Whether or not the human player plays as odds
PLAYER_ODDS = True

if __name__ == '__main__':
    """
    Interactive game for T3 that provides UI, IO, and prompts both
    player and agent for their action choices at each state.
    """
    
    print("================================")
    print("=              T3              =")
    print("================================")
    
    state = T3State(ODDS_STARTS, START_STATE)
    players_turn = not (ODDS_STARTS ^ PLAYER_ODDS)
    act = None
    
    # Main game loop: keep placing tiles until a terminal
    while not state.is_tie() and not state.is_win():
        print("\n" + str(state))
        
        if players_turn:
            print("Enter three space-separated numbers in format: COL ROW NUMBER ")
            print("[Player's Turn] - Move Options: " + str(state.get_moves()) + " > ")
            choice = input()
            parsed_act = choice.split(" ")
            err = "[X] Invalid or improperly formatted action, l2p. Try again."
            if not len(parsed_act) == 3:
                print(err)
                continue
            col, row, num = parsed_act
            act = T3Action(int(col), int(row), int(num))
            if not state.is_valid_action(act):
                print(err)
                continue
        
        # Agent's turn
        else:
            print("\n[...] AI is thinking...")
            act = choose(state)
            print("[Opponent's Turn] > " + str(act))
        
        state = state.get_next_state(act)
        players_turn = not players_turn
    
    print("\n********************************")
    print(("[L] You got dunked on!" if players_turn else "[W] You are the T3 elite!") if state.is_win() else "[T] Tie game!")
    print(state)
    print("********************************")