from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def carry(qc, c_in, a, b, c_out):
    qc.ccx(a, b, c_out)
    qc.cx(a, b)
    qc.ccx(c_in, b, c_out)

def carry_inv(qc, c_in, a, b, c_out):
    qc.ccx(c_in, b, c_out)
    qc.cx(a, b)
    qc.ccx(a, b, c_out)

def sum_gate(qc, c_in, a, b):
    qc.cx(c_in, b)
    qc.cx(a, b)

def adder(a_val, b_val):
    qc = QuantumCircuit(13, 5)

    a  = [0, 1, 2, 3]
    b  = [4, 5, 6, 7]
    c  = [8, 9, 10, 11]
    ov = 12

    for i in range(4):
        if (a_val >> i) & 1: qc.x(a[i])
        if (b_val >> i) & 1: qc.x(b[i])

    carry(qc, c[0], a[0], b[0], c[1])
    carry(qc, c[1], a[1], b[1], c[2])
    carry(qc, c[2], a[2], b[2], c[3])
    carry(qc, c[3], a[3], b[3], ov)

    qc.cx(a[3], b[3])

    carry_inv(qc, c[2], a[2], b[2], c[3])
    sum_gate(qc,  c[2], a[2], b[2])
    carry_inv(qc, c[1], a[1], b[1], c[2])
    sum_gate(qc,  c[1], a[1], b[1])
    carry_inv(qc, c[0], a[0], b[0], c[1])
    sum_gate(qc,  c[0], a[0], b[0])

    qc.measure([b[0], b[1], b[2], b[3], ov], [0, 1, 2, 3, 4])
    return qc

tests = [(5, 7), (3, 4), (15, 1), (0, 0)]

for a_val, b_val in tests:
    qc = adder(a_val, b_val)
    result = AerSimulator().run(qc, shots=1).result()
    bits = list(result.get_counts().keys())[0]
    print(f"{a_val} + {b_val} = {int(bits, 2)}")