from BackTrack import NQueenBT
from ForwardChecking import NQueenFC
from MAC import NQueenMAC
from MAC_MRV import NQueenMAC_MRV

class Main:
    def run(self):
        sizes = [4, 8, 16, 32]  
        algorithms = [
            ("Backtracking (BT)", NQueenBT()),
            ("Forward Checking (FC)", NQueenFC()),
            ("MAC", NQueenMAC()),
            ("MAC + MRV", NQueenMAC_MRV())
        ]

        for name, algo in algorithms:
            print(f"\n*** Running {name} ***")
            for size in sizes:
                # Call the appropriate function for each algorithm
                if name == "Backtracking (BT)":
                    solution, runtime, checks, found = algo.nqueen_BT(size)
                elif name == "Forward Checking (FC)":
                    solution, runtime, checks, found = algo.nqueen_FC(size)
                elif name == "MAC":
                    solution, runtime, checks, found = algo.nqueen_MAC(size)
                elif name == "MAC + MRV":
                    solution, runtime, checks, found = algo.nqueen_MAC_MRV(size)

                print(f"\nN = {size}")
                if found:
                    solution_str = " ".join(map(str, solution))
                    print(f"Solution (Columns): {solution_str}")
                    print(f"Runtime: {runtime:.6f} seconds")
                    print(f"Constraint checks: {checks}")
                else:
                    print("No solution found or time limit exceeded.")
                    print(f"Runtime: {runtime:.6f} seconds")
                    print(f"Constraint checks: {checks}")
                    break  # Stop the current algorithm if it fails

if __name__ == "__main__":
    Main().run()
