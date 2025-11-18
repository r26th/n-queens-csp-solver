import time
import copy
import random

class NQueensCSP:
    def __init__(self, n):
        self.n = n
        self.constraint_checks = 0
        self.start_time = 0
        # Domains: Index is column, Value is list of valid rows
        self.domains = {i: list(range(n)) for i in range(n)}

    def is_consistent(self, var, value, assignment):
        """
        Checks if placing a queen at (var, value) conflicts with existing assignment.
        var = column, value = row.
        """
        self.constraint_checks += 1
        
        for other_var in assignment:
            other_val = assignment[other_var]
            
            # 1. Row Constraint: different variables cannot have the same value
            if other_val == value:
                return False
            
            # 2. Diagonal Constraint: |X_i - X_j| != |i - j|
            if abs(other_val - value) == abs(other_var - var):
                return False
                
        return True
        
    def select_unassigned_variable(self, assignment, domains):
        """
        MRV Heuristic: Select the unassigned variable with the fewest remaining values.
        """
        # Get all variables (columns) that have not been assigned a row yet
        unassigned_vars = [v for v in range(self.n) if v not in assignment]
        
        # Find the variable with the minimum domain size
        # logic: min(iterable, key=function)
        best_var = min(unassigned_vars, key=lambda var: len(domains[var]))
        return best_var

    # ==========================================
    # 1. Standard Backtracking (BT)
    # ==========================================
    def solve_bt(self):
        self.constraint_checks = 0
        self.start_time = time.time()
        return self._bt_recursive({})

    def _bt_recursive(self, assignment):
        # Time limit check (20 mins = 1200 seconds)
        if time.time() - self.start_time > 1200:
            return None 

        # Base case: If assignment is complete
        if len(assignment) == self.n:
            return assignment

        # Select unassigned variable (Column)
        # Simple heuristic: select the next column in order
        var = len(assignment)

        # Create a list of possible rows and shuffle them
        rows = list(range(self.n))
        random.shuffle(rows)

        for value in rows:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self._bt_recursive(assignment)
                if result:
                    return result
                del assignment[var] # Backtrack
        return None

    # ==========================================
    # 2. Forward Checking (FC)
    # ==========================================
    def solve_fc(self):
        self.constraint_checks = 0
        self.start_time = time.time()
        # Pass a copy of initial domains
        return self._fc_recursive({}, copy.deepcopy(self.domains))

    def _fc_recursive(self, assignment, current_domains):
        # Time limit check
        if time.time() - self.start_time > 1200: return None
        
        # Base case: All queens placed
        if len(assignment) == self.n: return assignment

        # --- CHANGE: Use MRV to pick the best variable ---
        var = self.select_unassigned_variable(assignment, current_domains)
        
        # Copy the domain values to a new list so we don't mess up the actual domain
        values_to_try = list(current_domains[var])
        random.shuffle(values_to_try)

        for value in values_to_try:
            new_domains = copy.deepcopy(current_domains)
            assignment[var] = value
            
            # Forward Checking logic
            valid_move = True
            # We must check ALL unassigned variables, not just those > var
            # because MRV jumps around the board (e.g. col 0 -> col 15 -> col 3)
            for future_var in range(self.n):
                if future_var not in assignment and future_var != var:
                    # Remove row conflict
                    if value in new_domains[future_var]:
                        new_domains[future_var].remove(value)
                    
                    # Remove diagonal conflicts
                    dist = abs(future_var - var) # Absolute distance is required now
                    if (value + dist) in new_domains[future_var]:
                        new_domains[future_var].remove(value + dist)
                    if (value - dist) in new_domains[future_var]:
                        new_domains[future_var].remove(value - dist)
                    
                    self.constraint_checks += 1
                    
                    if not new_domains[future_var]:
                        valid_move = False
                        break
            
            if valid_move:
                result = self._fc_recursive(assignment, new_domains)
                if result: return result
            
            del assignment[var] # Backtrack
            
        return None

    # ==========================================
    # 3. Maintaining Arc Consistency (MAC)
    # ==========================================
    def solve_mac(self):
        self.constraint_checks = 0
        self.start_time = time.time()
        return self._mac_recursive({}, copy.deepcopy(self.domains))

    def ac3(self, assignment, domains):
        """
        The AC-3 algorithm to propagate constraints.
        Returns False if inconsistency found (domain wipeout), True otherwise.
        """
        queue = []
        
        # Initialize queue with arcs involving unassigned variables
        # This is a simplified MAC initialization for N-Queens
        assigned_vars = list(assignment.keys())
        unassigned_vars = [v for v in range(self.n) if v not in assigned_vars]
        
        for xi in unassigned_vars:
            for xj in unassigned_vars:
                if xi != xj:
                    queue.append((xi, xj))
        
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj, domains):
                if len(domains[xi]) == 0:
                    return False # Wipeout
                # If xi changed, re-check its neighbors
                for xk in unassigned_vars:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj, domains):
        revised = False
        for x in domains[xi][:]: # Copy for iteration
            # Check if there is any value y in domains[xj] satisfying constraints
            has_support = False
            for y in domains[xj]:
                # Check constraints (Row & Diagonal)
                if x != y and abs(x - y) != abs(xi - xj):
                    has_support = True
                    break
                self.constraint_checks += 1
            
            if not has_support:
                domains[xi].remove(x)
                revised = True
        return revised

    def _mac_recursive(self, assignment, domains):
        if time.time() - self.start_time > 1200: return None
        if len(assignment) == self.n: return assignment

        # --- CHANGE: Use MRV ---
        var = self.select_unassigned_variable(assignment, domains)

        # Copy the domain values to a new list
        values_to_try = list(domains[var])
        random.shuffle(values_to_try)

        for value in values_to_try:
            new_domains = copy.deepcopy(domains)
            assignment[var] = value
            new_domains[var] = [value] 
            
            if self.ac3(assignment, new_domains):
                result = self._mac_recursive(assignment, new_domains)
                if result: return result
            
            del assignment[var]
        
        return None

# ==========================================
# Main Execution Block
# ==========================================
if __name__ == "__main__":
    # We separate small sizes (where BT works) and large sizes
    sizes = [4, 8, 16, 32, 64] 
    
    print(f"{'N':<5} {'Algorithm':<10} {'Time(s)':<10} {'Checks':<15} {'Result'}")
    print("-" * 60)

    for N in sizes:
        # 1. Test BT (Only run for small N, otherwise it hangs)
        if N < 20: 
            solver = NQueensCSP(N) # Or NQueensCSP_MRV if you renamed it
            start = time.time()
            sol = solver.solve_bt()
            dur = time.time() - start
            print(f"{N:<5} {'BT':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")
        else:
            # For 32 and 64, we just print "Timeout" or "Skipped" for BT
            print(f"{N:<5} {'BT':<10} {'> 1200s':<10} {'---':<15} {'Timeout'}")

        # 2. Test FC (Run for all)
        solver = NQueensCSP(N)
        start = time.time()
        sol = solver.solve_fc()
        dur = time.time() - start
        print(f"{N:<5} {'FC':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")

        # 3. Test MAC (Run for all)
        solver = NQueensCSP(N)
        start = time.time()
        sol = solver.solve_mac()
        dur = time.time() - start
        print(f"{N:<5} {'MAC':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")
        print("-" * 60)
