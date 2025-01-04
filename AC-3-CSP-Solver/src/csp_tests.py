import unittest
import pytest
from datetime import *
from date_constraints import *
from csp_solver import *

class CSPTests(unittest.TestCase):
    """
    Unit tests for validating the CSP Solver's efficacy. Notes:
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
    
    def validate_solution(self, n_meetings: int, solution: Optional[list[datetime]], constraints: set[DateConstraint], solution_expected: bool=True) -> None:
        '''
        Tests a given solution to a CSP and returns instructive error messages for whenever a
        failure occurs.
        
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
        '''
        if solution_expected and solution is None:
            pytest.fail("[X] You returned an answer of None (no-solution) where one was expected")
        if not solution_expected:
            if solution is not None:
                pytest.fail("[X] You returned a solution when None was expected; your solution: " + str(solution))
            else: return
        if solution is not None and not n_meetings == len(solution):
            pytest.fail("[X] You returned an incomplete / overfull solution to be tested where one was expected: " + str(solution))
        
        # At this point, good to test the given solution against constraints
        valid_solution: list[datetime] = solution if solution is not None else []
        for constraint in constraints:
            if not constraint.is_satisfied_by_assignment(valid_solution):
                pytest.fail("[X] Your solution violated a constraint:\n  [S] Solution: " + str(valid_solution) + "\n  [C] Constraint: " + str(constraint))
        pass
    
    # CSP Filtering Tests
    # ---------------------------------------------------------------------------
    def test_csp_node_consistency_t0(self) -> None:
        constraints = {
            DateConstraint(0, "==", datetime(2023, 1, 3))
        }
        # One Meeting with possible values ranging from 2023-1-1 to 2023-1-5
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 1
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        node_consistency(domains, constraints)
        
        self.assertEqual(1, len(domains[0]))
        self.assertIn(datetime(2023, 1, 3), domains[0])
        
    def test_csp_node_consistency_t1(self) -> None:
        constraints = {
            DateConstraint(0, "<", datetime(2023, 1, 3))
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 1
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        node_consistency(domains, constraints)
        
        self.assertEqual(2, len(domains[0]))
        self.assertIn(datetime(2023, 1, 1), domains[0])
        self.assertIn(datetime(2023, 1, 2), domains[0])
        
    def test_csp_node_consistency_t2(self) -> None:
        constraints = {
            DateConstraint(0, "!=", datetime(2023, 1, 3)),
            DateConstraint(1, "<", datetime(2023, 1, 2))
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 3
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        node_consistency(domains, constraints)
        
        self.assertEqual(4, len(domains[0]))
        self.assertEqual(1, len(domains[1]))
        self.assertEqual(5, len(domains[2]))
        self.assertNotIn(datetime(2023, 1, 3), domains[0])
        self.assertIn(datetime(2023, 1, 1), domains[1])
        
    def test_csp_node_consistency_t3(self) -> None:
        constraints = {
            DateConstraint(0, "!=", datetime(2023, 1, 3)),
            DateConstraint(1, "<", datetime(2023, 1, 2))
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 3
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        node_consistency(domains, constraints)
        
        self.assertEqual(4, len(domains[0]))
        self.assertEqual(1, len(domains[1]))
        self.assertEqual(5, len(domains[2]))
        self.assertNotIn(datetime(2023, 1, 3), domains[0])
        self.assertIn(datetime(2023, 1, 1), domains[1])
        
    def test_csp_arc_consistency_t0(self) -> None:
        constraints = {
            DateConstraint(0, "!=", 1)
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 2
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        arc_consistency(domains, constraints)
        
        self.assertEqual(5, len(domains[0]))
        self.assertEqual(5, len(domains[1]))
        
    def test_csp_arc_consistency_t1(self) -> None:
        constraints = {
            DateConstraint(0, "<", 1)
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 2
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        arc_consistency(domains, constraints)
        
        self.assertEqual(4, len(domains[0]))
        self.assertEqual(4, len(domains[1]))
        self.assertNotIn(datetime(2023, 1, 5), domains[0])
        self.assertNotIn(datetime(2023, 1, 1), domains[1])
        
    def test_csp_arc_consistency_t2(self) -> None:
        constraints = {
            DateConstraint(0, "<", 1),
            DateConstraint(1, "<", 0)
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 2
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        # AC here should nuke both domains because it's unsatisfiable!
        arc_consistency(domains, constraints)
        
        self.assertEqual(0, len(domains[0]))
        self.assertEqual(0, len(domains[1]))
        
    def test_csp_arc_consistency_t3(self) -> None:
        constraints = {
            DateConstraint(0, "<", 1),
            DateConstraint(1, "<", 2),
            DateConstraint(2, "<", 0)
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 3
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        # AC here should nuke ALL domains because it's unsatisfiable!
        arc_consistency(domains, constraints)
        
        self.assertEqual(0, len(domains[0]))
        self.assertEqual(0, len(domains[1]))
        self.assertEqual(0, len(domains[2]))
        
    def test_csp_arc_consistency_t4(self) -> None:
        constraints = {
            DateConstraint(0, "==", 1),
            DateConstraint(1, "!=", 2),
            DateConstraint(2, "<", 0)
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 2)
        n_meetings = 3
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        arc_consistency(domains, constraints)
        
        self.assertEqual(1, len(domains[0]))
        self.assertEqual(1, len(domains[1]))
        self.assertEqual(1, len(domains[2]))
        self.assertIn(datetime(2023, 1, 2), domains[0])
        self.assertIn(datetime(2023, 1, 2), domains[1])
        self.assertIn(datetime(2023, 1, 1), domains[2])
        
    def test_csp_arc_consistency_t5(self) -> None:
        constraints = {
            DateConstraint(0, "==", 1),
            DateConstraint(1, "==", 2),
            DateConstraint(2, "==", datetime(2023, 1, 1))
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 2)
        n_meetings = 3
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        # C-C-C-COMBO CONSISTENCY!
        node_consistency(domains, constraints)
        arc_consistency(domains, constraints)
        
        self.assertEqual(1, len(domains[0]))
        self.assertEqual(1, len(domains[1]))
        self.assertEqual(1, len(domains[2]))
        self.assertIn(datetime(2023, 1, 1), domains[0])
        self.assertIn(datetime(2023, 1, 1), domains[1])
        self.assertIn(datetime(2023, 1, 1), domains[2])
        
    def test_csp_arc_consistency_t6(self) -> None:
        constraints = {
            DateConstraint(1, "!=", 0),
            DateConstraint(1, "<", 2),
            DateConstraint(2, "<=", datetime(2023, 1, 3)),
            DateConstraint(0, ">=", datetime(2023, 1, 3))
        }
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 3
        domains: list[set[datetime]] = [deepcopy(possible_dates) for n in range(n_meetings)]
        
        # C-C-C-COMBO CONSISTENCY!
        node_consistency(domains, constraints)
        arc_consistency(domains, constraints)
        
        self.assertEqual(3, len(domains[0]))
        self.assertEqual(2, len(domains[1]))
        self.assertEqual(2, len(domains[2]))
    
    # TODO
    
    # CSP Backtracker Tests
    # ---------------------------------------------------------------------------
    def test_csp_backtracking_t0(self) -> None:
        constraints = {
            DateConstraint(0, "==", datetime(2023, 1, 3))
        }
        # Date range of 2023-1-1 to 2023-1-5 in which the only meeting date
        # for 1 meeting can be on 2023-1-3
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 1
        
        # Example solution:
        # [2023-1-3]
        solution = solve(n_meetings, possible_dates, constraints)
        self.validate_solution(n_meetings, solution, constraints)
        
    def test_csp_backtracking_t1(self) -> None:
        constraints = {
            DateConstraint(0, "==", datetime(2023, 1, 6))
        }
        # Date range of 2023-1-1 to 2023-1-5 in which the only meeting date
        # for 1 meeting can be on 2023-1-6, which is outside of the allowable
        # range, so no solution here!
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 1
        solution = solve(n_meetings, possible_dates, constraints)
        
        # Note the solution_expected=False flag for the validator to ensure we're
        # returning None 
        self.validate_solution(n_meetings, solution, constraints, solution_expected=False)
        
    def test_csp_backtracking_t2(self) -> None:
        constraints = {
            DateConstraint(0, ">", datetime(2023, 1, 3))
        }
        # Date range of 2023-1-1 to 2023-1-5 in which the only meeting date
        # for 1 meeting can be AFTER 2023-1-3
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 1
        solution = solve(n_meetings, possible_dates, constraints)
        
        # Example Solution:
        # [2023-01-05]
        self.validate_solution(n_meetings, solution, constraints)
        
    def test_csp_backtracking_t3(self) -> None:
        constraints = {
            DateConstraint(0, ">", datetime(2023, 1, 3)),
            DateConstraint(1, ">", datetime(2023, 1, 3))
        }
        # Date range of 2023-1-1 to 2023-1-5 in which the only meeting date
        # for 2 meetings can be AFTER 2023-1-3 (nothing here saying that they
        # can't be on the same day!)
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 2
        solution = solve(n_meetings, possible_dates, constraints)
        
        # Example Solution:
        # [2023-01-05, 2023-01-05]
        self.validate_solution(n_meetings, solution, constraints)
        
    def test_csp_backtracking_t4(self) -> None:
        constraints = {
            DateConstraint(0, "<=", datetime(2023, 1, 2)),
            DateConstraint(1, "<=", datetime(2023, 1, 2)),
            DateConstraint(0, "!=", 1)
        }
        # Date range of 2023-1-1 to 2023-1-5 in which the only meeting date
        # for 2 meetings can be BEFORE or ON 2023-1-2 but NOW they can't be on the
        # same date!
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 5)
        n_meetings = 2
        solution = solve(n_meetings, possible_dates, constraints)
        
        # Example Solution:
        # [2023-01-02, 2023-01-01]
        self.validate_solution(n_meetings, solution, constraints)
        
    def test_csp_backtracking_t5(self) -> None:
        constraints = {
            DateConstraint(0, "!=", 1),
            DateConstraint(0, "!=", 2),
            DateConstraint(1, "!=", 2)
        }
        # Date range of 2023-1-1 to 2023-1-2 in which the only meeting date
        # for 3 meetings in a narrow time window that can't have the same
        # date! (impossible)
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 2)
        n_meetings = 3
        solution = solve(n_meetings, possible_dates, constraints)
        self.validate_solution(n_meetings, solution, constraints, solution_expected=False)
    
    def test_csp_backtracking_t6(self) -> None:
        constraints = {
            DateConstraint(0, "!=", 1),
            DateConstraint(0, "!=", 2),
            DateConstraint(1, "!=", 2)
        }
        # Now, however, each meeting can be placed on a separate day
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 3)
        n_meetings = 3
        solution = solve(n_meetings, possible_dates, constraints)
        
        # Example Solution:
        # [2023-01-03, 2023-01-02, 2023-01-01]
        self.validate_solution(n_meetings, solution, constraints)
        
    def test_csp_backtracking_t7(self) -> None:
        constraints = {
            DateConstraint(0, "!=", 1),
            DateConstraint(1, "==", 2),
            DateConstraint(2, "!=", 3),
            DateConstraint(3, "==", 4),
            DateConstraint(4, "<", 0),
            DateConstraint(3, ">", 2)
        }
        # Here's a puzzle for ya
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 3)
        n_meetings = 5
        solution = solve(n_meetings, possible_dates, constraints)
        
        # Example Solution:
        # [2023-01-03, 2023-01-01, 2023-01-01, 2023-01-02, 2023-01-02]
        self.validate_solution(n_meetings, solution, constraints)
    
    def test_csp_backtracking_t8(self) -> None:
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
        
        # [!] Will likely need AT LEAST node_consistency for this test
        # to pass in time, though you may have hardware able to solve without
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 134)
        n_meetings = 5
        solution = solve(n_meetings, possible_dates, constraints)
         
        # Example Solution:
        # [2023-05-15, 2023-05-15, 2023-04-30, 2023-05-14, 2023-05-14]
        self.validate_solution(n_meetings, solution, constraints)
         
    def test_csp_backtracking_t9(self) -> None:
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
        
        # [!] Will likely need BOTH node+arc_consistency for this test
        # to pass in time, though you may have hardware able to solve without
        possible_dates = self.generate_dates(datetime(2023, 1, 1), 180)
        n_meetings = 5
        solution = solve(n_meetings, possible_dates, constraints)
         
        # Example Solution:
        # [2023-05-31, 2023-04-30, 2023-04-28, 2023-04-29, 2023-05-30]
        self.validate_solution(n_meetings, solution, constraints)
        