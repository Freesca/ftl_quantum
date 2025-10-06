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


def two_q_bell_state_circuit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return "Two-Qubit Bell-State Circuit", qc


def bell_state_circuit():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    print(qc.draw())
    qc.draw("mpl")
    plt.show()
    return "Bell-State Circuit", qc


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
        bell_state_circuit(),
        two_q_bell_state_circuit()
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