from nqueens import NQueensCSP
import time

sizes = [4, 8, 16, 32, 64]

print(f"{'N':<5} {'Algorithm':<10} {'Time(s)':<10} {'Checks':<15} {'Result'}")
print("-" * 60)

for N in sizes:
    
    if N < 20:
        solver = NQueensCSP(N)
        start = time.time()
        sol = solver.solve_bt()
        dur = time.time() - start
        print(f"{N:<5} {'BT':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")
    else:
        print(f"{N:<5} {'BT':<10} {'> 1200s':<10} {'---':<15} {'Timeout'}")

    # FC
    solver = NQueensCSP(N)
    start = time.time()
    sol = solver.solve_fc()
    dur = time.time() - start
    print(f"{N:<5} {'FC':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")

    # MAC
    solver = NQueensCSP(N)
    start = time.time()
    sol = solver.solve_mac()
    dur = time.time() - start
    print(f"{N:<5} {'MAC':<10} {dur:<10.4f} {solver.constraint_checks:<15} {'Found' if sol else 'Fail'}")
    print("-" * 60)