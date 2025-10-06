from qiskit import transpile
from qiskit.circuit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import argparse


def two_q_bell_state_circuit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)  # Apply Hadamard gate to the first qubit
    qc.cx(0, 1)  # Apply CNOT gate with qubit 0 as control and qubit 1 as target
    qc.measure([0, 1], [0, 1])  # Measure both qubits

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

    qc = two_q_bell_state_circuit()

    simulator = AerSimulator()
    run(qc, "Two-Qubit Bell-State Circuit", simulator, args.shots)


if __name__ == "__main__":
    main()