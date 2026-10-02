import time
from nqueens import NQueensCSP

# ==========================================
# Helper: Print the Board
# ==========================================
def print_board(solution, n):
    """
    Visualizes the N-Queens solution.
    solution: list where index=col, value=row
    """
    # Only print board if N is small enough to fit on screen
    if n > 32: 
        print(f"      > [Board too large to print visually (N={n})]")
        return

    print(f"      > Board Visualization:")
    for row in range(n):
        line = "        "  # Indentation for clean look
        for col in range(n):
            if solution[col] == row:
                line += " ♕ "  # Queen
            else:
                line += " □ "  # Empty square
        print(line)

# ==========================================
# Main Execution Block
# ==========================================
if __name__ == "__main__":
    sizes = [4, 8, 16, 32, 64] 
    summary_table = [] 

    print("\n" + "="*60)
    print(f"{'N-QUEENS SOLVER EXECUTION LOG':^60}")
    print("="*60)

    for N in sizes:
        print(f"\n>>> Processing Board Size: N = {N}")
        print("-" * 40)

        # ---------------------------------------
        # 1. Run BT (Skip if N >= 20)
        # ---------------------------------------
        if N < 20:
            solver = NQueensCSP(N)
            start = time.time()
            solution = solver.solve_bt()
            duration = time.time() - start
            
            result_str = "Found" if solution else "Fail"
            time_str = f"{duration:.4f}"
            checks_str = f"{solver.constraint_checks}"
            
            print(f"  [BT] Time: {time_str}s | Checks: {checks_str} | Result: {result_str}")
            if solution:
                path = [solution[i] for i in range(N)]
                print(f"      > Random Start: Queen 0 was placed at Row {path[0]}")
                print(f"      > Solution Path: {path}")
                print_board(solution, N) # <--- CALL THE BOARD PRINTER
            
            summary_table.append((N, "BT", time_str, checks_str, result_str))
        else:
            print(f"  [BT] Skipped (Timeout Risk)")
            summary_table.append((N, "BT", "> 1200s", "---", "Timeout"))

        print("") # Spacer

        # ---------------------------------------
        # 2. Run FC
        # ---------------------------------------
        solver = NQueensCSP(N)
        start = time.time()
        solution = solver.solve_fc()
        duration = time.time() - start
        
        result_str = "Found" if solution else "Fail"
        time_str = f"{duration:.4f}"
        checks_str = f"{solver.constraint_checks}"
        
        print(f"  [FC] Time: {time_str}s | Checks: {checks_str} | Result: {result_str}")
        if solution:
            path = [solution[i] for i in range(N)]
            path_str = str(path)
            
            print(f"      > Random Start: Queen 0 was placed at Row {path[0]}")
            print(f"      > Solution Path: {path_str}")
            print_board(solution, N) # <--- CALL THE BOARD PRINTER

        summary_table.append((N, "FC", time_str, checks_str, result_str))
        print("") # Spacer

        # ---------------------------------------
        # 3. Run MAC
        # ---------------------------------------
        solver = NQueensCSP(N)
        start = time.time()
        solution = solver.solve_mac()
        duration = time.time() - start
        
        result_str = "Found" if solution else "Fail"
        time_str = f"{duration:.4f}"
        checks_str = f"{solver.constraint_checks}"
        
        print(f"  [MAC] Time: {time_str}s | Checks: {checks_str} | Result: {result_str}")
        if solution:
            path = [solution[i] for i in range(N)]
            path_str = str(path)
            
            print(f"      > Random Start: Queen 0 was placed at Row {path[0]}")
            print(f"      > Solution Path: {path_str}")
            print_board(solution, N) # <--- CALL THE BOARD PRINTER

        summary_table.append((N, "MAC", time_str, checks_str, result_str))

    # ==========================================
    # FINAL SUMMARY TABLE
    # ==========================================
    print("\n" + "="*75)
    print(f"{'FINAL PERFORMANCE SUMMARY':^75}")
    print("="*75)
    print(f"{'N':<5} {'Algorithm':<10} {'Time(s)':<12} {'Checks':<15} {'Result'}")
    print("-" * 75)
    
    for row in summary_table:
        n_val, name, t_val, c_val, res = row
        print(f"{n_val:<5} {name:<10} {t_val:<12} {c_val:<15} {res}")
    print("-" * 75)
