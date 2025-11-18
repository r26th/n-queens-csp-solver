import time 
from collections import deque 
import copy 
 
# Global variables 
constraint_checks = 0 
START_TIME = 0.0 
TIME_LIMIT_SECONDS = 1200 
 
 
 
def is_conflict(r1, c1, r2, c2): 
    # Checks if two queens at (r1, c1) and (r2, c2) conflict. 
    global constraint_checks 
    constraint_checks += 1 
    return c1 == c2 or abs(r1 - r2) == abs(c1 - c2) 
 
 
def revise_queen(i, j, domains): 
    # Makes the arc (i, j) consistent 
    revised = False 
    values_to_remove = set() 
 
    for x in set(domains[i]): 
        has_support = False 
        for y in domains[j]: 
            if not is_conflict(i, x, j, y): 
                has_support = True 
                break 
        # Removes values from D_i that have no supporting value in D_j 
        if not has_support: 
            values_to_remove.add(x) 
            revised = True 
 
    if values_to_remove: 
        domains[i] -= values_to_remove 
    # Returns True if D_i was revised. 
    return revised 
 
 
def MAC_propagate(current_row, n, domains): 
    """ 
    Only arcs (Xi -> X_assigned) for unassigned Xi are initially added. 
    Returns True if propagation succeeds (no domain wipe-out), False otherwise. 
    """ 
    Q = deque() 
 
    # Only consider unassigned variables (rows after current_row) 
    unassigned_vars = list(range(current_row + 1, n)) 
 
    # Add arcs from each unassigned variable to the newly assigned variable 
    for i in unassigned_vars: 
        Q.append((i, current_row))  # (Xi, Xassigned) 
 
    # Run AC-3 on this restricted set of arcs (this is MAC) 
    while Q: 
        i, j = Q.popleft() 
 
        if revise_queen(i, j, domains): 
            # Domain wipe-out => failure 
            if not domains[i]: 
                return False 
 
            # If D_i was revised, add (k -> i) for all unassigned k != i 
            for k in unassigned_vars: 
                if k != i: 
                    Q.append((k, i)) 
 
    return True 
 
# This function expects to be called with the current partial assignment and domains. 
# MAC with MRV variable selection. Assigns variables until all are assigned 
 
def placeQueen_MAC_MRV(n, assignment, domains): 
    global START_TIME, TIME_LIMIT_SECONDS 
 
    # Time check 
    if time.time() - START_TIME > TIME_LIMIT_SECONDS: 
        return False 
 
    # returns True if a complete assignment is found 
    # If all variables assigned 
    if len(assignment) == n: 
        return True 
 
    # Select unassigned variable with smallest domain (MRV) 
    unassigned = [v for v in range(n) if v not in assignment] 
    var = min(unassigned, key=lambda v: len(domains[v])) 
 
    # Try each value in domain order 
    for col in list(domains[var]): 
        assignment[var] = col 
        old_domains = copy.deepcopy(domains) 
        domains[var] = {col} 
 
        # Use MAC propagate with respect to the newly assigned variable 
        if MAC_propagate(var, n, domains): 
            if placeQueen_MAC_MRV(n, assignment, domains): 
                return True 
 
        # Backtrack 
        assignment.pop(var, None) 
        domains.clear() 
        domains.update(old_domains) 
 
    return False 
 
 
def nqueen_MAC_MRV(n): 
    global constraint_checks, START_TIME, TIME_LIMIT_SECONDS 
 
    assignment = {} 
    initial_domain = set(range(n)) 
    domains = {r: set(initial_domain) for r in range(n)} 
 
    constraint_checks = 0 
    START_TIME = time.time() 
 
    found = placeQueen_MAC_MRV(n, assignment, domains) 
 
    end_time = time.time() 
    runtime = end_time - START_TIME 
 
    solution = [] 
    if found: 
        for r in range(n): 
            solution.append(assignment[r] + 1)   
 
    return solution, runtime, constraint_checks, found 
 
 
#  the program starts from here  
if name == "__main__": 
    sizes = [4, 8, 16, 32, 64] 
 
    print("*** N-Queens Maintaining Arc-Consistency (MAC) with MRV Results ***") 
 
    for size in sizes: 
        print(f"\nN = {size}") 
 
        solution, runtime, checks, found = nqueen_MAC_MRV(size) 
 
        if found: 
            solution_str = " ".join(map(str, solution)) 
            print(f"Solution: {solution_str}") 
            print(f"Runtime: {runtime:.6f} seconds") 
            print(f"Constraint checks: {checks}") 
        else: 
            print("No solution found or time limit exceeded") 
            print(f"Runtime: {runtime:.6f} seconds") 
            print(f"Constraint checks: {checks}")