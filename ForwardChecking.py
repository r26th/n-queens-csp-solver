import time 
 
# Global variables 
constraint_checks = 0 
START_TIME = 0.0 
TIME_LIMIT_SECONDS = 1200  # 20 minute limit 
 
def update_domains(n, row, col, domains): 
    global constraint_checks 
     
    # Track which domains we modify for easy backtracking 
    modifications = [] 
     
    for r in range(row + 1, n): 
        cols_to_remove = set() 
        row_diff = r - row 
         
        for c in list(domains[r]):  # Iterate over copy to avoid modification during iteration 
            # Column conflict check 
            constraint_checks += 1 
            if c == col: 
                cols_to_remove.add(c) 
                continue 
                 
            # Diagonal conflict check 
            constraint_checks += 1 
            if abs(c - col) == row_diff: 
                cols_to_remove.add(c) 
         
        if cols_to_remove: 
            # Store modification for potential backtracking 
            modifications.append((r, cols_to_remove)) 
            domains[r] -= cols_to_remove 
             
            if not domains[r]: 
                # Restore domains before returning failure 
                for mod_r, removed_cols in modifications: 
                    domains[mod_r] |= removed_cols 
                return False, modifications 
                 
    return True, modifications 
 
def placeQueen_FC(current_row, n, assignment, domains): 
    global START_TIME, TIME_LIMIT_SECONDS 
     
    # Time check 
    if time.time() - START_TIME > TIME_LIMIT_SECONDS: 
        return False 
     
    # Base case 
    if current_row == n: 
        return True 
 
    # Try each value in current domain 
    for col in list(domains[current_row]): 
        assignment[current_row] = col 
         
        # Apply forward checking 
        success, modifications = update_domains(n, current_row, col, domains) 
         
        if success: 
            # Recursively place next queen 
            if placeQueen_FC(current_row + 1, n, assignment, domains): 
                return True 
         
        # Backtrack: restore domains 
        for mod_r, removed_cols in modifications: 
            domains[mod_r] |= removed_cols 
         
        # Remove assignment 
        if current_row in assignment: 
            del assignment[current_row] 
             
    return False 
 
def nqueen_FC(n): 
    global constraint_checks, START_TIME 
     
    assignment = {} 
    domains = {r: set(range(n)) for r in range(n)} 
    constraint_checks = 0 
     
    START_TIME = time.time() 
    found = placeQueen_FC(0, n, assignment, domains) 
    runtime = time.time() - START_TIME 
     
    solution = [] 
    if found: 
        for r in range(n): 
            solution.append(assignment[r] + 1) 
     
    return solution, runtime, constraint_checks, found 
 
 
# the program starts from here 
if __name__ == "__main__": 
     
    sizes = [4, 8, 16, 32, 64]  
     
    print("*** N-Queens Forward Checking (FC) Results ***") 
 
    for size in sizes: 
        solution, runtime, checks, found = nqueen_FC(size) 
         
        print(f"\nN = {size}") 
 
        if found: 
            solution_str = " ".join(map(str, solution)) 
            print(f"Solution (Columns): {solution_str}") 
            print(f"Runtime: {runtime:.6f} seconds") 
            print(f"Constraint checks: {checks}") 
         
        else: 
            print(f"Program Terminated: Time exceeded the limit of {TIME_LIMIT_SECONDS} seconds.") 
            print(f"Runtime (before termination): {runtime:.6f} seconds") 
            print(f"Constraint checks: {checks}") 
            break;