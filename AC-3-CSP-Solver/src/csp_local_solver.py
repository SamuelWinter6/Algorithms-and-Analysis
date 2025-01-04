'''
Calendar Satisfaction Problem (CSP) Local Solver
Designed to make scheduling those meetings a breeze! Suite of tools
for efficiently scheduling some n meetings in a given datetime range
that abides by some number of constraints.

In this module:
- A solver that uses local search methods
  [!] These methods, while fast, are not always complete!
'''

import random
from datetime import *
from date_constraints import *
from dataclasses import *
from copy import *
from csp_solver import *

# CSP Local Search Constants
# ---------------------------------------------------------------------------
MAX_STEPS: int = 250
MAX_RESTARTS: int = 50

# CSP Local Solver
# ---------------------------------------------------------------------------
def local_solve(n_meetings: int, date_range: set[datetime], constraints: set[DateConstraint]) -> Optional[list[datetime]]:
    '''
    When possible, MAY return a solution to the given CSP based on the need to
    schedule n meetings within the given date range and abiding by the given
    set of DateConstraints.
      - Implemented using a Local Search Approximate solution method
      - May return None when the CSP is unsatisfiable or when the solver got unlucky
        and ran out of random restarts to succeed
    
    [!] Two important Constants in this file dictate behavior of the local solver:
      - MAX_STEPS = the number of steps that the solver should take from any one
        random initial state
      - MAX_RESTARTS = the number of random restarts the local solver may take before
        giving up and returning None
    
    [!] If attempting a genetic algorithm, may add any constants to the top of this
        file as deemed necessary
    
    Parameters:
        n_meetings (int):
            The number of meetings that must be scheduled, indexed from 0 to n-1
        date_range (set[datetime]):
            The range of datetimes in which the n meetings must be scheduled; by default,
            these are each separated a day apart, but there's nothing to stop these from
            being meetings scheduled down to the second
            [!] WARNING: AVOID ALIASING -- Remember that each variable must have its
            own domain but what's provided is a single reference to a set of datetimes
        constraints (set[DateConstraint]):
            A set of DateConstraints specifying how the meetings must be scheduled.
            See DateConstraint documentation for different types of DateConstraints
            that might be found, and useful methods for implementing this solver.
    
    Returns:
        Optional[list[datetime]]:
            If a solution to the CSP exists:
                Returns a list of datetimes, one for each of the n_meetings, where the
                datetime at each index corresponds to the meeting of that same index
            If no solution is possible:
                Returns None
            If the MAX_RESTARTS are reached:
                Returns None
    '''
    # [!] TODO: Implement the local search method of your choosing!
    return []
