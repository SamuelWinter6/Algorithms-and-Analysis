'''
Calendar Satisfaction Problem (CSP) Solver
Designed to make scheduling those meetings a breeze! Suite of tools
for efficiently scheduling some n meetings in a given datetime range
that abides by some number of constraints.

In this module:
- A solver that uses the backtracking exact solver approach
- Tools for pruning domains using node and arc consistency
'''
from datetime import *
from date_constraints import *
from dataclasses import *
from copy import *


# CSP Backtracking Solver
# ---------------------------------------------------------------------------
def solve(n_meetings: int, date_range: set[datetime], constraints: set[DateConstraint]) -> Optional[list[datetime]]:
    '''
    When possible, returns a solution to the given CSP based on the need to
    schedule n meetings within the given date range and abiding by the given
    set of DateConstraints.
      - Implemented using the Backtracking exact solution method
      - May return None when the CSP is unsatisfiable
    
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
    '''
    # [!] TODO: Implement your backtracking CSP Solver!
    print('\n\nNumber of Meetings:', n_meetings)
    print('Number of Constraints:', len(constraints))
    print('Constraints:', constraints)

    domains = [set(date_range) for _ in range(n_meetings)]
    node_consistency(domains, constraints)
    arc_consistency(domains, constraints)

    def evaluate_constraints(assignment: List[datetime], current_index: int) -> bool:
        '''
        Evaluates all relevant constraints for the meeting scheduled at the given index
        in the assignment list to ensure the current state of the assignment does not violate
        any constraints.

        This function is typically called after adding or changing the date of a meeting in
        the assignment list to check if the change adheres to all specified constraints
        involving the changed meeting's date.

        Parameters:
            assignment (List[datetime]):
                A list of datetimes where each index corresponds to a scheduled meeting. 
                The list length equals the current number of scheduled meetings, which may be
                less than the total required if the scheduling is in progress.
            current_index (int):
                The index of the meeting that was last added or updated. This parameter is
                used to identify which constraints need to be checked based on the meetings
                involved in each constraint.

        Returns:
            bool:
                Returns True if all relevant constraints are satisfied by the current state of
                the assignment, False otherwise. If False, the latest change causes a conflict
                and should be reconsidered or backtracked.
        '''
        for constraint in constraints:
            if constraint.L_VAL == current_index or (isinstance(constraint.R_VAL, int) and constraint.R_VAL == current_index):
                if len(assignment) <= constraint.L_VAL:
                    continue
                left_date = assignment[constraint.L_VAL] if len(assignment) > constraint.L_VAL else None
                right_date = constraint.R_VAL if isinstance(constraint.R_VAL, datetime) else (
                    assignment[constraint.R_VAL] if len(assignment) > constraint.R_VAL else None)
                
                if left_date is not None and right_date is not None:
                    if not constraint.is_satisfied_by_values(left_date, right_date):
                        return False
        return True

    def backtrack(assignment: List[datetime], meeting_index: int = 0) -> Optional[List[datetime]]:
        '''
        Recursively tries to assign dates to meetings and checks constraints at each step
        to find a solution that satisfies all constraints. This function employs the backtracking
        algorithm, a depth-first search technique for solving constraint satisfaction problems.

        Parameters:
            assignment (List[datetime]):
                The current list of assigned dates to meetings; partially filled.
            meeting_index (int, optional):
                The index of the meeting to try and assign a date to. Starts at 0 and increments
                as deeper levels of the recursion assign dates to subsequent meetings.

        Returns:
            Optional[List[datetime]]:
                If a valid assignment for all meetings is found that satisfies all constraints:
                    Returns a list of datetimes, one for each meeting.
                If no valid assignment is found:
                    Returns None, indicating failure to find a solution.
        '''
        if meeting_index == n_meetings:
            return assignment[:] if evaluate_constraints(assignment, meeting_index - 1) else None

        for date in domains[meeting_index]:
            assignment.append(date)
            if evaluate_constraints(assignment, meeting_index):
                result = backtrack(assignment, meeting_index + 1)
                if result:
                    return result
            assignment.pop()

        return None

    results = backtrack([])

    if results:
        print("All constraints are satisfied.", results)
        return results
    else:
        print("Constraints are violated.")
        return None

# CSP Filtering: Node Consistency
# ---------------------------------------------------------------------------
def node_consistency(domains: list[set[datetime]], constraints: set[DateConstraint]) -> None:
    '''
    Enforces node consistency for all variables' domains given in the set of domains.
    Meetings' domains' index in each of the provided constraints correspond to their index
    in the list of domains.
    
    [!] Note: Only applies to Unary DateConstraints, i.e., those whose arity() method
    returns 1
    
    Parameters:
        domains (list[set[datetime]]):
            A list of domains where each domain is a set of possible date times to assign
            to each meeting. Each domain in the given list is indexed such that its index
            corresponds to the indexes of meetings mentioned in the given constraints.
        constraints (set[DateConstraint]):
            A set of DateConstraints specifying how the meetings must be scheduled.
            See DateConstraint documentation for different types of DateConstraints
            that might be found, and useful methods for implementing this solver.
            [!] Hint: see a DateConstraint's is_satisfied_by_values
    
    Side Effects:
        Although no values are returned, the values in any pruned domains are changed
        directly within the provided domains parameter
    '''
    # [!] TODO: Implement node consistency filtering
    for constraint in constraints:
        if constraint.arity() == 1:
            meeting_index = constraint.L_VAL
            valid_dates = set()
            for date in domains[meeting_index]:
                if constraint.is_satisfied_by_values(date, None):
                    valid_dates.add(date)
            domains[meeting_index] = valid_dates

# CSP Filtering: Arc Consistency
# ---------------------------------------------------------------------------
class Arc:
    '''
    Helper Arc class to be used to organize domains for pruning during the AC-3
    algorithm, organized as (TAIL -> HEAD) Arcs that correspond to a given
    CONSTRAINT.
    
    [!] Although you do not need to, you *may* modify this class however you see
    fit to accomplish the arc_consistency method
    
    Attributes:
        CONSTRAINT (DateConstraint):
            The DateConstraint represented by this arc
        TAIL (int):
            The index of the meeting variable at this arc's tail.
        HEAD (int):
            The index of the meeting variable at this arc's head.
    
    [!] IMPORTANT: By definition, the TAIL = CONSTRAINT.L_VAL and
        HEAD = CONSTRAINT.R_VAL
    '''
    
    def __init__(self, constraint: DateConstraint):
        '''
        Constructs a new Arc from the given DateConstraint, setting this Arc's
        TAIL to the constraint's L_VAL and its HEAD to the constraint's R_VAL
        
        Parameters:
            constraint (DateConstraint):
                The constraint represented by this Arc
        '''
        self.CONSTRAINT: DateConstraint = constraint
        self.TAIL: int = constraint.L_VAL
        if isinstance(constraint.R_VAL, int):
            self.HEAD: int = constraint.R_VAL
        else:
            raise ValueError("[X] Cannot create Arc from Unary Constraint")
    
    def __eq__(self, other: Any) -> bool:
        if other is None: return False
        if not isinstance(other, Arc): return False
        return self.CONSTRAINT == other.CONSTRAINT and self.TAIL == other.TAIL and self.HEAD == other.HEAD
    
    def __hash__(self) -> int:
        return hash((self.CONSTRAINT, self.TAIL, self.HEAD))
    
    def __str__(self) -> str:
        return "Arc[" + str(self.CONSTRAINT) + ", (" + str(self.TAIL) + " -> " + str(self.HEAD) + ")]"
    
    def __repr__(self) -> str:
        return self.__str__()

def arc_consistency(domains: list[set[datetime]], constraints: set[DateConstraint]) -> None:
    '''
    Enforces arc consistency for all variables' domains given in the set of domains.
    Meetings' domains' index in each of the provided constraints correspond to their index
    in the list of domains.
    
    [!] Note: Only applies to Binary DateConstraints, i.e., those whose arity() method
    returns 2
    
    Parameters:
        domains (list[set[datetime]]):
            A list of domains where each domain is a set of possible date times to assign
            to each meeting. Each domain in the given list is indexed such that its index
            corresponds to the indexes of meetings mentioned in the given constraints.
        constraints (set[DateConstraint]):
            A set of DateConstraints specifying how the meetings must be scheduled.
            See DateConstraint documentation for different types of DateConstraints
            that might be found, and useful methods for implementing this solver.
            [!] Hint: see a DateConstraint's is_satisfied_by_values
    
    Side Effects:
        Although no values are returned, the values in any pruned domains are changed
        directly within the provided domains parameter
    '''
    # [!] TODO: Implement AC-3 Preprocessing Filtering
    queue = [Arc(constraint) for constraint in constraints if constraint.arity() == 2]

    while queue:
        arc = queue.pop(0)
        if revise(domains, arc):
            for constraint in constraints:
                if constraint.arity() == 2:
                    queue.append(Arc(constraint))

def revise(domains: List[Set[datetime]], arc: Any) -> bool:
    '''
    Revises the domains of the variables in the constraint satisfaction problem to ensure
    that all domain values are consistent with the constraints. The function uses the arc
    consistency algorithm to prune values from the domains that are not consistent with
    the constraints. If any values are removed from a domain, indicating that a revision
    was made, the function returns True.

    Parameters:
        domains (List[Set[datetime]]):
            A list where each index represents a variable and each set contains the
            possible datetime values that the variable can take. The domains are updated
            in-place to remove inconsistent values.
        arc (Any):
            An object representing the arc or the constraint between two variables.
            This object must have the following properties:
                - HEAD: An index pointing to the 'head' variable of the arc in the domains list.
                - TAIL: An index pointing to the 'tail' variable of the arc.
                - CONSTRAINT: An object or function that can evaluate whether a given
                  value pair satisfies the constraint. It must support a method or function
                  call `is_satisfied_by_values(tail_value, head_value)` that returns a boolean.

    Returns:
        bool:
            True if any changes were made to the domains (i.e., if any values were pruned),
            otherwise False. This allows for further processing or repeated revision until
            no more changes are made (reaching arc consistency across all variables).
    '''
    revised = False
    valid_tail_values = set()
    valid_head_values = set(domains[arc.HEAD])

    for tail_value in domains[arc.TAIL]:
        valid = any(arc.CONSTRAINT.is_satisfied_by_values(tail_value, head_value) for head_value in domains[arc.HEAD])
        if valid:
            valid_tail_values.add(tail_value)

    for head_value in domains[arc.HEAD]:
        valid = any(arc.CONSTRAINT.is_satisfied_by_values(tail_value, head_value) for tail_value in domains[arc.TAIL])
        if not valid:
            valid_head_values.remove(head_value)

    if valid_tail_values != domains[arc.TAIL]:
        domains[arc.TAIL] = valid_tail_values
        revised = True
    if valid_head_values != domains[arc.HEAD]:
        domains[arc.HEAD] = valid_head_values
        revised = True

    return revised