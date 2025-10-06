from qiskit import transpile
from qiskit.circuit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import argparse


def bell_state_circuit():
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate to create superposition
    qc.measure(0, 0)  # Measure the qubit

    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return qc


def run(qcirc, qcirc_name, simulator, shots):

    qcirc = transpile(qcirc, simulator)
    results = simulator.run(qcirc, shots=shots).result()
    counts = results.get_counts()

    print(f"{qcirc_name} counts: {counts}")
    plot_histogram(counts, title=f'{qcirc_name} counts')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="")
    #argument to make the code run on IBM Quantum computers
    parser.add_argument("--shots", type=int, default=500, help="Number of shots for the simulation")
    args = parser.parse_args()

    qc = bell_state_circuit()

    simulator = AerSimulator()
    run(qc, "Bell-State Circuit", simulator, args.shots)


if __name__ == "__main__":
    main()