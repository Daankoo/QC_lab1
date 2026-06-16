from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def margolus(qc, a, b, c):
    qc.ry(np.pi / 4, c)
    qc.cx(b, c)
    qc.ry(np.pi / 4, c)
    qc.cx(a, c)
    qc.ry(-np.pi / 4, c)
    qc.cx(b, c)
    qc.ry(-np.pi / 4, c)

def test_margolus(a, b, c):
    qc = QuantumCircuit(3, 3)

    if a: qc.x(0)
    if b: qc.x(1)
    if c: qc.x(2)

    margolus(qc, 0, 1, 2)

    qc.measure([0, 1, 2], [0, 1, 2])

    result = AerSimulator().run(qc, shots=1).result()
    output = list(result.get_counts().keys())[0][::-1]

    print(f"A={a} B={b} C={c} → {output}")

for a in [0, 1]:
    for b in [0, 1]:
        for c in [0, 1]:
            test_margolus(a, b, c)