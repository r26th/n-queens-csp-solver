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

    # ==========================================
    # MRV HEURISTIC (The "Smart" Choice)
    # ==========================================
    def select_unassigned_variable(self, assignment, domains):
        """
        MRV Heuristic: Select the unassigned variable with the fewest remaining values.
        """
        unassigned_vars = [v for v in range(self.n) if v not in assignment]
        # Find variable with minimum domain size
        best_var = min(unassigned_vars, key=lambda var: len(domains[var]))
        return best_var

    def is_consistent(self, var, value, assignment):
        self.constraint_checks += 1
        for other_var in assignment:
            other_val = assignment[other_var]
            if other_val == value:
                return False
            if abs(other_val - value) == abs(other_var - var):
                return False
        return True

    # ==========================================
    # 1. Standard Backtracking (BT)
    # ==========================================
    def solve_bt(self):
        self.constraint_checks = 0
        self.start_time = time.time()
        return self._bt_recursive({})

    def _bt_recursive(self, assignment):
        if time.time() - self.start_time > 1200: return None 
        if len(assignment) == self.n: return assignment

        # BT usually uses static order (Column 0, 1, 2...)
        var = len(assignment)

        # RANDOM START REQUIREMENT: Shuffle rows before trying
        rows = list(range(self.n))
        random.shuffle(rows)

        for value in rows:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self._bt_recursive(assignment)
                if result: return result
                del assignment[var]
        return None

    # ==========================================
    # 2. Forward Checking (FC) WITH MRV
    # ==========================================
    def solve_fc(self):
        self.constraint_checks = 0
        self.start_time = time.time()
        return self._fc_recursive({}, copy.deepcopy(self.domains))

    def _fc_recursive(self, assignment, current_domains):
        if time.time() - self.start_time > 1200: return None
        if len(assignment) == self.n: return assignment

        # USE MRV HERE
        var = self.select_unassigned_variable(assignment, current_domains)
        
        # RANDOM REQUIREMENT: Shuffle values to try
        values_to_try = list(current_domains[var])
        random.shuffle(values_to_try)

        for value in values_to_try:
            new_domains = copy.deepcopy(current_domains)
            assignment[var] = value
            
            valid_move = True
            # Check against ALL unassigned variables (because MRV jumps around)
            for future_var in range(self.n):
                if future_var not in assignment and future_var != var:
                    # Remove row conflict
                    if value in new_domains[future_var]:
                        new_domains[future_var].remove(value)
                    
                    # Remove diagonal conflicts
                    dist = abs(future_var - var)
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
            
            del assignment[var]
            
        return None

    # ==========================================
    # 3. Maintaining Arc Consistency (MAC) WITH MRV
    # ==========================================
    def solve_mac(self):
        self.constraint_checks = 0
        self.start_time = time.time()
        return self._mac_recursive({}, copy.deepcopy(self.domains))

    def ac3(self, assignment, domains):
        queue = []
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
                    return False
                for xk in unassigned_vars:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj, domains):
        revised = False
        for x in domains[xi][:]:
            has_support = False
            for y in domains[xj]:
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

        # USE MRV HERE
        var = self.select_unassigned_variable(assignment, domains)

        # RANDOM REQUIREMENT
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
    sizes = [4, 8, 16, 32, 64] 
    
    print(f"{'N':<5} {'Algorithm':<10} {'Time(s)':<10} {'Checks':<15} {'Result'}")
    print("-" * 60)

    for N in sizes:
        # 1. Test BT (Skip for large N)
        if N < 20: 
            solver = NQueensCSP(N)
            start = time.time()
            sol = solver.solve_bt()
            dur = time.time() - start
            print(f"{N:<5} {'BT':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")
        else:
            print(f"{N:<5} {'BT':<10} {'> 1200s':<10} {'---':<15} {'Timeout'}")

        # 2. Test FC
        solver = NQueensCSP(N)
        start = time.time()
        sol = solver.solve_fc()
        dur = time.time() - start
        print(f"{N:<5} {'FC':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")

        # 3. Test MAC
        solver = NQueensCSP(N)
        start = time.time()
        sol = solver.solve_mac()
        dur = time.time() - start
        print(f"{N:<5} {'MAC':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")
        print("-" * 60)
