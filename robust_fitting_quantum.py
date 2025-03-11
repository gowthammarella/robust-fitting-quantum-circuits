# Robust Fitting in Gate-Based Quantum Computers
# Author: Gowtham Royal Vikramadithya

# Import required libraries
import numpy as np
import qiskit
from qiskit import QuantumCircuit, transpile, Aer, execute
from qiskit.providers.aer import noise
import matplotlib.pyplot as plt

# Function to create a simple quantum circuit
def create_quantum_circuit():
    qc = QuantumCircuit(2)  # 2-qubit circuit
    qc.h(0)  # Hadamard gate on qubit 0
    qc.cx(0, 1)  # CNOT gate (entanglement)
    qc.measure_all()  # Measurement of all qubits
    return qc

# Function to simulate noise in a quantum circuit
def simulate_noisy_circuit(qc):
    # Define noise model (depolarizing noise)
    noise_model = noise.NoiseModel()
    error = noise.depolarizing_error(0.05, 1)  # 5% depolarizing error
    noise_model.add_all_qubit_quantum_error(error, ['h', 'cx'])

    # Run the circuit with noise
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulator)
    result = execute(transpiled_qc, simulator, shots=1024, noise_model=noise_model).result()
    counts = result.get_counts()
    return counts

# Function to apply error mitigation techniques
def apply_error_mitigation(counts):
    # Simple error mitigation by rescaling probability distribution
    total_shots = sum(counts.values())
    mitigated_counts = {state: count / total_shots for state, count in counts.items()}
    return mitigated_counts

# Main function to execute the quantum circuit and apply robust fitting
def main():
    qc = create_quantum_circuit()
    print("Quantum Circuit:")
    print(qc)

    noisy_counts = simulate_noisy_circuit(qc)
    print("Noisy Measurement Results:", noisy_counts)

    mitigated_counts = apply_error_mitigation(noisy_counts)
    print("Mitigated Results:", mitigated_counts)

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.bar(mitigated_counts.keys(), mitigated_counts.values(), color='blue', alpha=0.7, label="Mitigated")
    plt.bar(noisy_counts.keys(), np.array(list(noisy_counts.values()))/1024, color='red', alpha=0.5, label="Noisy")
    plt.xlabel("Quantum States")
    plt.ylabel("Probability")
    plt.title("Noisy vs Mitigated Results")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
