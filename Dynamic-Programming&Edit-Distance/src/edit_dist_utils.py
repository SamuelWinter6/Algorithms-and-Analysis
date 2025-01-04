'''
Variety of functions related to computing the edit distance between
strings and, importantly, which WILL be used by the DistleGame to
provide feedback to the DistlePlayer during a game of Distle.

[!] Feel free to use any of these methods as needed in your DistlePlayer.

[!] Feel free to ADD any methods you see fit for use by your DistlePlayer,
e.g., some form of entropy computation.
'''

def get_edit_dist_table(row_str: str, col_str: str) -> list[list[int]]:
    '''
    Returns the completed Edit Distance memoization structure: a 2D list
    of ints representing the number of string manupulations required to
    minimally turn each subproblem's string into the other.
    
    Parameters:
        row_str (str):
            The string located along the table's rows
        col_str (col):
            The string located along the table's columns
    
    Returns:
        list[list[int]]:
            Completed memoization table for the computation of the
            edit_distance(row_str, col_str)
    '''
    # [!] TODO

    m, n = len(row_str), len(col_str)
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                table[i][j] = j
            elif j == 0:
                table[i][j] = i
            else:
                cost = 0 if row_str[i-1] == col_str[j-1] else 1
                table[i][j] = min(
                    table[i-1][j] + 1,  # Deletion
                    table[i][j-1] + 1,  # Insertion
                    table[i-1][j-1] + cost  # Substitution
                )
                # Check for transposition
                if i > 1 and j > 1 and row_str[i-1] == col_str[j-2] and row_str[i-2] == col_str[j-1]:
                    table[i][j] = min(table[i][j], table[i-2][j-2] + cost)  # Transposition

    return table

def edit_distance(s0: str, s1: str) -> int:
    '''
    Returns the edit distance between two given strings, defined as an
    int that counts the number of primitive string manipulations (i.e.,
    Insertions, Deletions, Replacements, and Transpositions) minimally
    required to turn one string into the other.
    
    [!] Given as part of the skeleton, no need to modify
    
    Parameters:
        s0, s1 (str):
            The strings to compute the edit distance between
    
    Returns:
        int:
            The minimal number of string manipulations
    '''
    if s0 == s1: return 0
    return get_edit_dist_table(s0, s1)[len(s0)][len(s1)]

def get_transformation_list(s0: str, s1: str) -> list[str]:
    '''
    Returns one possible sequence of transformations that turns String s0
    into s1. The list is in top-down order (i.e., starting from the largest
    subproblem in the memoization structure) and consists of Strings representing
    the String manipulations of:
        1. "R" = Replacement
        2. "T" = Transposition
        3. "I" = Insertion
        4. "D" = Deletion
    In case of multiple minimal edit distance sequences, returns a list with
    ties in manipulations broken by the order listed above (i.e., replacements
    preferred over transpositions, which in turn are preferred over insertions, etc.)
    
    [!] Given as part of the skeleton, no need to modify
    
    Example:
        s0 = "hack"
        s1 = "fkc"
        get_transformation_list(s0, s1) => ["T", "R", "D"]
        get_transformation_list(s1, s0) => ["T", "R", "I"]
    
    Parameters:
        s0, s1 (str):
            Start and destination strings for the transformation
    
    Returns:
        list[str]:
            The sequence of top-down manipulations required to turn s0 into s1
    '''
    
    return get_transformation_list_with_table(s0, s1, get_edit_dist_table(s0, s1))

def get_transformation_list_with_table(s0: str, s1: str, table: list[list[int]]) -> list[str]:
    '''
    See get_transformation_list documentation.
    
    This method does exactly the same thing as get_transformation_list, except that
    the memoization table is input as a parameter. This version of the method can be
    used to save computational efficiency if the memoization table was pre-computed
    and is being used by multiple methods.
    
    [!] MUST use the already-solved memoization table and must NOT recompute it.
    [!] MUST be implemented recursively (i.e., in top-down fashion)
    '''
    # [!] TODO
    
    # Code Based off Levenshtein distance **(these kinds of comments are ok [NO])**
    #>>[NO] All methods require proper docstrings, even helper methods(-1)
    def derive_sequence(i: int, j: int) -> list[str]:
        #>>[NO] Remove comments from your code, you should be writing it in a way that is readable to others(-0.5)
        # Base case: reached the beginning of both strings
        if i == 0 and j == 0:
            return []

        if i > 0 and j > 0 and table[i][j] == table[i-1][j-1] + 1:
            return ["R"] + derive_sequence(i-1, j-1)
        elif i > 1 and j > 1 and s0[i-2] == s1[j-1] and s0[i-1] == s1[j-2] and table[i][j] == table[i-2][j-2] + 1:
            return ["T"] + derive_sequence(i-2, j-2)
        elif j > 0 and table[i][j] == table[i][j-1] + 1:
            return ["I"] + derive_sequence(i, j-1)
        elif i > 0 and table[i][j] == table[i-1][j] + 1:
            return ["D"] + derive_sequence(i-1, j)

        # Assuming characters match if no other operation is chosen
        if i > 0 and j > 0:
            return derive_sequence(i-1, j-1)

        # Fallback for unmatched conditions
        return derive_sequence(max(i-1, 0), max(j-1, 0))

    # Start the recursion from the end of both strings
    transformations = derive_sequence(len(s0), len(s1))
    return transformations

# ===================================================
# >>> [NO] Summary
# Very clean well done code. Obviously you understand the
# processes of dynamic programming and applied it well
# to the edit distance problem
# ---------------------------------------------------
# >>> [NO] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
#
# [X] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [~] Proper docstrings provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:          100 / 100
# -> EditDistUtils:      20 / 20  (-2 / missed test)
# -> DistlePlayer:      274 / 265 (-0.5 / below threshold; max -30)
# Style Penalty:       -1.5
# Total:               98.5 / 100
# ===================================================
