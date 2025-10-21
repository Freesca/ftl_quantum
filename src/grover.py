from qiskit import transpile
from qiskit_ibm_runtime import (
    QiskitRuntimeService,
    SamplerV2 as RuntimeSamplerV2,
    Batch,
)
from qiskit.circuit import QuantumCircuit
from qiskit_aer.primitives import SamplerV2 as AerSamplerV2
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import argparse

def oracle(n=3):
    qc = QuantumCircuit(n)
    qc.h(n-1)
    qc.mcx([i for i in range(n-1)], n-1)
    qc.h(n-1)
    qc.x(0)

    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return "Toffoli oracle", qc

def diffuser_qc(n):
    qc = QuantumCircuit(n)
    qc.h([i for i in range(n)])
    qc.x([i for i in range(n)])
    qc.h(n-1)
    qc.mcx([i for i in range(n-1)], n-1)  # Multi-controlled Toffoli
    qc.h(n-1)
    qc.x([i for i in range(n)])
    qc.h([i for i in range(n)])
    return qc


def grover_circuit(oracle, n=3):
    qc = QuantumCircuit(n, n)
    qc.h([i for i in range(n)])  # Initialize in superposition
    oracle_name, oracle_qc = oracle
    for i in range(n // 2):
        qc.compose(oracle_qc, inplace=True)
        qc.compose(diffuser_qc(n), inplace=True)
    
    qc.measure([i for i in range(n)], [i for i in range(n)])  # Measure all qubits

    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return f"Grover with {oracle_name} Oracle", qc

def run(qcs, sampler, shots, backend=None):
    for qcirc_name, qcirc in qcs:
        qcirc = transpile(qcirc, backend=backend)
        results = sampler.run([qcirc], shots=shots).result()
        counts = results[0].data.c.get_counts()

        print(f"{qcirc_name} counts: {counts}")
        plot_histogram(counts, title=f'{qcirc_name} counts')
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="")
    #argument to make the code run on IBM Quantum computers
    parser.add_argument("--ibm", action="store_true", help="Run on IBM Quantum")
    parser.add_argument("--shots", type=int, default=500, help="Number of shots for the simulation")
    parser.add_argument("--n", type=int, default=3, help="Number of bits arguments of the function")
    args = parser.parse_args()

    qcs = [
        grover_circuit(oracle(args.n), n=args.n)
    ]

    if args.ibm:
        try:
            service = QiskitRuntimeService()
            backend = service.least_busy(operational=True, simulator=False)
        except Exception as e:
            print(f"Error loading IBMQ account or getting backend: {e}")
            return
        with Batch(backend=backend) as batch:
            sampler = RuntimeSamplerV2(mode=batch)
            run(qcs, sampler, args.shots, backend=backend)
    else:
        sampler = AerSamplerV2()
        run(qcs, sampler, args.shots)


if __name__ == "__main__":
    main()