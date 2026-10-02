# N-Queens CSP Solver

A Python implementation of the N-Queens problem as a Constraint Satisfaction Problem (CSP). The project compares three search algorithms and evaluates their performance using execution time and constraint-check counts across multiple board sizes.

## Implemented Algorithms

- **Backtracking (BT)** — assigns queens column by column while checking row and diagonal constraints.
- **Forward Checking (FC)** — removes conflicting values from future domains and uses the Minimum Remaining Values (MRV) heuristic.
- **Maintaining Arc Consistency (MAC)** — applies AC-3 constraint propagation during search and uses MRV.

The value order is randomized before each search, so execution times and constraint-check counts may vary between runs.

## Tested Board Sizes

The main program evaluates:

```text
N = 4, 8, 16, 32, 64
```

To keep larger comparisons computationally practical, standard Backtracking is executed for board sizes below 20, while Forward Checking and MAC are evaluated across all configured sizes. Board visualizations are displayed for board sizes up to 32.

## Project Files

- `nqueens.py` — defines the `NQueensCSP` class and implements Backtracking, Forward Checking, MRV, MAC, and AC-3.
- `main.py` — runs the algorithms, measures execution time and constraint checks, displays solutions, and generates a final performance summary.

## Requirements

- Python 3
- No external packages are required.

## How to Run

Clone the repository and enter its directory:

```bash
git clone https://github.com/r26th/n-queens-csp-solver.git
cd n-queens-csp-solver
```

Run the program:

```bash
python main.py
```

## Output

For each algorithm and board size, the program reports:

- Whether a solution was found
- Execution time in seconds
- Number of recorded constraint checks
- Solution configuration
- Board visualization for supported sizes

The program concludes with a combined performance-summary table for the evaluated algorithms and board sizes.
