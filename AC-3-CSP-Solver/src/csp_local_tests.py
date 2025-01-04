import unittest
import pytest
import math
from datetime import *
from date_constraints import *
from csp_local_solver import *

# The number of times a local solver must find the correct solution
# for a test to be considered "passed"
THRESHOLD   = 8
# The number of times each test will be run
REPETITIONS = 10

class CSPLocalTests(unittest.TestCase):
    """
    Unit tests for validating the LOCAL CSP Solver's efficacy. Notes:
    - If this is the set of tests provided in the solution skeleton, it represents an
      incomplete set that you are expected to add to to adequately test your submission!
    - Your correctness score on the assignment will be assessed by a more complete,
      grading set of unit tests.
    - A portion of your style grade will also come from proper type hints; remember to
      validate your submission using `mypy .` and ensure that no issues are found.
    """
    
    def generate_dates(self, start_date: datetime, n_days: int) -> set[datetime]:
        '''
        Constructs a range of dates starting at the given start_date and then advancing
        some n_days into the future, each datetime separated by exactly 1 day.
        
        Parameters:
            start_date (datetime):
                The date at which to begin the range
            n_days (int):
                The number of days that this range spans
        
        Returns:
            set[datetime]
                The set of dates in the range provided by the parameters
        '''
        return {start_date + timedelta(days=x) for x in range(n_days)}
    
    def validate_solution(self, n_meetings: int, solution: Optional[list[datetime]], constraints: set[DateConstraint], solution_expected: bool=True) -> int:
        '''
        Tests a given solution to a CSP and returns 0 if the test failed, 1 otherwise.
        
        Parameters:
            n_meetings (int):
                The number of meetings that must be scheduled for this CSP if a solution exists
            solution (Optional[list[datetime]]):
                The solution provided by your CSP Solver; can be either a list of datetimes if
                your solver believes a solution exists, or None if it believes that no solution does
            constraints (set[DateConstraint]):
                The set of DateConstraints that must all be satisfied to have a working solution
            solution_expected (bool):
                Whether or not we're expecting the given problem to have a solution; by default,
                True, but when set to False, expects that the solution argument is None, signaling
                that your solver thought that there was no solution.
        
        Returns:
            int:
                0 if the given solution failed the test, 1 otherwise.
        '''
        if solution_expected and solution is None:
            return 0
        if not solution_expected:
            if solution is not None:
                return 0
            else: return 1
        if solution is not None and not n_meetings == len(solution):
            return 0
        
        # At this point, good to test the given solution against constraints
        valid_solution: list[datetime] = solution if solution is not None else []
        for constraint in constraints:
            if not constraint.is_satisfied_by_assignment(valid_solution):
                return 0
        return 1
    
    def log_outcome(self, n_meetings: int, possible_dates: set[datetime], constraints: set[DateConstraint], solution_expected: bool=True) -> None:
        '''
        Runs the given test some REPETITIONS times (a constant set in this file) and checks that
        a correct solution was obtained by your local solver at least THRESHOLD times (also a
        constant defined at the top of this file).
        
        Parameters:
            n_meetings (int):
                The number of meetings that must be scheduled for this CSP if a solution exists
            possible_dates (set[datetime]):
                The range of datetimes in which the n meetings must be scheduled; by default,
                these are each separated a day apart
            constraints (set[DateConstraint]):
                The set of DateConstraints that must all be satisfied to have a working solution
            solution_expected (bool):
                Whether or not we're expecting the given problem to have a solution; by default,
                True, but when set to False, expects that the solution argument is None, signaling
                that your solver thought that there was no solution.
        
        Returns:
            int:
                0 if the given solution failed the test, 1 otherwise.
        '''
        solutions = [local_solve(n_meetings, possible_dates, constraints) for _ in range(REPETITIONS)]
        results = [self.validate_solution(n_meetings, solutions[r], constraints, solution_expected) for r in range(REPETITIONS)]
        total_correct = sum(results)
        if total_correct < THRESHOLD:
            pytest.fail("[X] Your local solver only returned a correct answer " + 
                        str(total_correct) + " times out of the required " + 
                        str(THRESHOLD) + " having run " + str(REPETITIONS) + 
                        " repetitions of this test")
    
    # CSP Local Solver Tests
    # ---------------------------------------------------------------------------
    def test_csp_local_solver_t0(self) -> None:
        constraints = {
            DateConstraint(0, "==", datetime(2023, 1, 3))
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 1
        self.log_outcome(n_meetings, possible_dates, constraints)
        
    def test_csp_local_solver_t1(self) -> None:
        constraints = {
            DateConstraint(0, "==", datetime(2023, 1, 6))
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 1
        self.log_outcome(n_meetings, possible_dates, constraints, solution_expected=False)
        
    def test_csp_local_solver_t2(self) -> None:
        constraints = {
            DateConstraint(0, "!=", 1),
            DateConstraint(1, "==", 2),
            DateConstraint(2, "!=", 3),
            DateConstraint(3, "==", 4),
            DateConstraint(4, "<", 0),
            DateConstraint(3, ">", 2)
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 3)
        n_meetings = 5
        self.log_outcome(n_meetings, possible_dates, constraints)
        
    def test_csp_local_solver_t3(self) -> None:
        constraints = {
            DateConstraint(0, ">", datetime(2023, 1, 1)),
            DateConstraint(1, ">", datetime(2023, 2, 1)),
            DateConstraint(2, ">", datetime(2023, 3, 1)),
            DateConstraint(3, ">", datetime(2023, 4, 1)),
            DateConstraint(4, ">", datetime(2023, 5, 1)),
            DateConstraint(0, ">", 4),
            DateConstraint(1, ">", 3),
            DateConstraint(2, "!=", 3),
            DateConstraint(4, "!=", 0),
            DateConstraint(3, ">", 2)
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 134)
        n_meetings = 5
        self.log_outcome(n_meetings, possible_dates, constraints)
        
    # Here's the real test of your local solver -- the others were warmups!
    # Can you solve it before time runs out? 0_o
    def test_csp_local_solver_t4(self) -> None:
        N_CONS = 50
        constraints = set()
        for i in range(1,math.floor(N_CONS/2)):
            for j in range(math.floor(N_CONS/2), N_CONS):
                if i == j: continue
                constraints.add(DateConstraint(i, ">" if (i % 2 == 0) else "<", j))
            
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 149)
        n_meetings = N_CONS
        self.log_outcome(n_meetings, possible_dates, constraints)
