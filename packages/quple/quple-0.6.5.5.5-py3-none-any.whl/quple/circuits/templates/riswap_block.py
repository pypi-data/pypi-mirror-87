from typing import Sequence
import numpy as np

from quple import TemplateCircuitBlock

class RISWAPBlock(TemplateCircuitBlock):
    
    @staticmethod
    def RYY(self, circuit:'quple.ParameterisedCircuit', qubits:Sequence[int], theta):
        circuit.RX(np.pi/2, list(qubits))
        circuit.CX(tuple(qubits))
        circuit.RZ(theta, qubits[1])
        circuit.CX(tuple(qubits))
        circuit.RX(-np.pi/2, list(qubits))
        
    @staticmethod
    def RXX(self, circuit:'quple.ParameterisedCircuit', qubits:Sequence[int], theta):
        circuit.H(list(qubits))
        circuit.CX(tuple(qubits))
        circuit.RZ(theta, qubits[1])
        circuit.CX(tuple(qubits))
        circuit.H(list(qubits))
        

    def build(self, circuit:'quple.ParameterisedCircuit', qubits:Sequence[int]):
        theta = circuit.new_param()
        RISWAPBlock.RXX(theta, qubits)
        RISWAPBlock.RYY(theta, qubits)
    
    @property
    def num_block_qubits(self) -> int:
        return 2
