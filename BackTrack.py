import time 
import sys  
 
# Global variables 
constraint_checks = 0 
START_TIME = 0.0 
TIME_LIMIT_SECONDS = 1200 # 20 minute limit 
 
# checking if it is safe to place a queen in a certain position r, c relative to previous rows 
def is_position_safe(n, assignment, r, c): 
    global constraint_checks 
     
    for prev_row, prev_col in assignment.items(): 
        if prev_row >= r: 
            continue 
             
        #checking Column then checking Diagonals 
        constraint_checks += 1 
        if prev_col == c: 
            return False 
        constraint_checks += 1 
        if abs(prev_row - r) == abs(prev_col - c): 
            return False 
    return True 
 
# applying backtracking algorithm  
def placeQueen_BT(current_row, n, assignment, solution): 
    global START_TIME, TIME_LIMIT_SECONDS 
 
    # checking runtime at the start of a new row 
    if time.time() - START_TIME > TIME_LIMIT_SECONDS: 
        # Stop the search  
        return False 
 
    # base case: all rows have a queen 
    if current_row == n: 
        # adding assignmnet to solution 
        for r in range(n): 
            solution.append(assignment[r] + 1)  
        return True 
 
    # going through all columns for the current row 
    for col in range(n): 
        if is_position_safe(n, assignment, current_row, col): 
            # adding clolumn to assignment  
            assignment[current_row] = col 
            # going to the next row 
            if placeQueen_BT(current_row + 1, n, assignment, solution): 
                return True 
 
            # backtrack if placeQueen_BT() not true 
            assignment.pop(current_row)  
 
    return False 
 
# Initializing backtracking algorithm 
def nqueen_BT(n): 
    global constraint_checks, START_TIME, TIME_LIMIT_SECONDS 
     
    assignment = {} 
    solution = [] 
     
    constraint_checks = 0 # reseting checks for the run 
     
    # starting to calculate time before the search begins 
    START_TIME = time.time() 
     
    # starting the search from row 0 
    found_solution = placeQueen_BT(0, n, assignment, solution) 
     
    end_time = time.time() 
    runtime = end_time - START_TIME 
     
    return solution, runtime, constraint_checks, found_solution 
 
# the program starts from here 
if __name__ == "__main__": 
     
    sizes = [4, 8, 16, 32, 64]  
     
    print("*** N-Queens Backtracking (BT) Results **") 
 
    for size in sizes: 
        solution, runtime, checks, found= nqueen_BT(size) 
         
        print(f"\n N = {size}") 
         
        if found: 
            # printing solution and numbers 
            solution_str = " ".join(map(str, solution)) 
            print(f"Solution (Columns): {solution_str}") 
            print(f"Runtime: {runtime:.6f} seconds") 
            print(f"Constraint checks: {checks}") 
        else: 
            print(f"Program Terminated: Time exceeded the limit of {TIME_LIMIT_SECONDS} seconds .") 
            print(f"Runtime (before termination): {runtime:.6f} seconds") 
            print(f"Constraint checks: {checks}") 
            break;