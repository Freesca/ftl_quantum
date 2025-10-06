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


def oracle_balanced_mod(n=3):
    qc = QuantumCircuit(n+1)
    for qubit in range(n):
        qc.x(qubit)
        qc.cx(qubit, n)
        qc.x(qubit)
    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return "Balanced Mod", qc


def oracle_const_mod(n=3):
    qc = QuantumCircuit(n+1)
    qc.x(n)
    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return "Constant Mod", qc


def oracle_balanced(n=3):
    qc = QuantumCircuit(n+1)
    for qubit in range(n):
        qc.cx(qubit, n)
    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return "Balanced", qc


def oracle_const(n=3):
    qc = QuantumCircuit(n+1)
    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return "Constant", qc


def dj_circuit(oracle, n = 3):
    qc = QuantumCircuit(n+1, n)
    qc.x(n)
    qc.h([n for n in range(n+1)])
    oracle_name, oracle_qc = oracle
    qc.compose(oracle_qc, inplace=True)
    qc.h([n for n in range(n)])
    qc.measure([i for i in range(n)], [i for i in range(n)])
    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return "Deutsch-Jozsa " + oracle_name, qc


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
    args = parser.parse_args()

    qcs = [
        (dj_circuit(oracle_const())),
        (dj_circuit(oracle_balanced())),
        (dj_circuit(oracle_const_mod())),
        (dj_circuit(oracle_balanced_mod()))
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