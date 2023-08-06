from abc import ABC, abstractmethod
from inspect import signature
from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)
import sympy as sp
import numpy as np

import cirq
from cirq.ops.gate_features import SingleQubitGate, TwoQubitGate

from quple import QuantumCircuit, TemplateCircuitBlock
from quple.components.interaction_graphs import interaction_graph
from quple.utils.utils import merge_pqc


class ParameterisedCircuit(QuantumCircuit, ABC):
    """Parameterised Quantum Circuit (PQC)
    
    For construction of parameterised quantum circuit with strongly entangling
    circuit architecture referenced from the circuit-centric classifier design
    https://arxiv.org/pdf/1804.00633.pdf. 
    
    In this architecture, the parameterised circuit is composed of L copies of
    a primary circuit block. Each circuit block consists of a layer of single
    qubit gates (the rotation layer) applied to each of the n qubits, followed
    by a layer of two (or three) qubit gates (the entanglement layer) to entangle
    all input qubits with a given interaction graph.
    
    Common single qubit gates in the rotation layer include the Hadamard gate,
    Pauli X, Pauli Y, Pauli Z gate and the corresponding rotation gates
    
    Common two qubit gates in the entangling layer include the CNOT (CX) gate,
    CZ gate, XX, YY, ZZ gate and the corresponding rotation gates.
    

    Examples:
        >> cq = ParameterisedCircuit(n_qubit=4)
        >> cq.build(rotation_blocks=['H','RZ'],
                    entanglement_blocks=['CNOT'],
                    entangle_strategy='linear',
                    copies=2)
        >> cq
        (0, 0): ───H───Rz(θ_0)───@───────H───Rz(θ_4)───@─────────────────
                                 │                     │
        (0, 1): ───H───Rz(θ_1)───X───@───H───Rz(θ_5)───X─────────@───────
                                     │                           │
        (0, 2): ───H───Rz(θ_2)───────X───@───H─────────Rz(θ_6)───X───@───
                                         │                           │
        (0, 3): ───H───Rz(θ_3)───────────X───H─────────Rz(θ_7)───────X───
    Args:
        n_qubit: int
           Number of qubits in the circuit
        copies: int
           Number of times the layers are repeated.
        rotation_blocks: A list of single qubit gate operations to be applied in the rotation layer.
        entanglement_blocks: A list of multi qubit gate operations to be applied in the entanglement layer.
        entangle_strategy: default='full'
            Determines how the qubits are connected in an entanglement block.
            If str, it specifies the name of the strategy.
            If callable, it specifies the function to map to an interaction graph.
            If list of str, it specifies the names of a list of strategies. The 
            strategy to use is decided by the current block index. For example, if
            the circuit is building the n-th entanglement block in the entanglement layer,
            then the n-th strategy in the list will be used.
            If list of callable, it specifies the list of functions to map to an interaction
            graph. The function to use is decided by the current block index.
        parameter_symbol: str
           Symbol prefix for circuit parameters.
        final_rotation_layer: boolean, default=False
           Whether to add an extra final rotation layer to the circuit.
        flatten_circuit: boolean, default=False
           Whether to flatten circuit parameters when the circuit is modified.
        name: str
           Name of the circuit.    
    """
    def __init__(self, n_qubit:int, copies:int=1,
                rotation_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entanglement_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                parameter_symbol:str='θ',
                final_rotation_layer:bool=False,
                flatten_circuit:bool=False,
                name:str='ParameterisedCircuit',
                *args, **kwargs):
        """ Creates a parameterised circuit following the scheme of 
            alternating rotation and entanglement layers 
           
            Args:
                n_qubit: int
                   Number of qubits in the circuit
                copies: int
                   Number of times the layers are repeated.
                rotation_blocks: A list of single qubit gate operations to be applied in the rotation layer.
                entanglement_blocks: A list of multi qubit gate operations to be applied in the entanglement layer.
                entangle_strategy: default='full'
                    Determines how the qubits are connected in an entanglement block.
                    If str, it specifies the name of the strategy.
                    If callable, it specifies the function to map to an interaction graph.
                    If list of str, it specifies the names of a list of strategies. The 
                    strategy to use is decided by the current block index. For example, if
                    the circuit is building the n-th entanglement block in the entanglement layer,
                    then the n-th strategy in the list will be used.
                    If list of callable, it specifies the list of functions to map to an interaction
                    graph. The function to use is decided by the current block index.
                parameter_symbol: str
                   Symbol prefix for circuit parameters.
                final_rotation_layer: boolean, default=False
                   Whether to add an extra final rotation layer to the circuit.
                flatten_circuit: boolean, default=False
                   Whether to flatten circuit parameters when the circuit is modified.
                name: str
                   Name of the circuit. 
        """
        super().__init__(n_qubit, name=name, *args, **kwargs)
        self._parameter_symbol = parameter_symbol
        self._parameters = np.array([], dtype=object)
        self._readout_qubit = None
        self._flatten_circuit = flatten_circuit
        self._entangle_strategy = entangle_strategy
        self.build(rotation_blocks, entanglement_blocks, entangle_strategy, copies,
                  final_rotation_layer)
    
    @property
    def entangle_strategy(self):
        return self._entangle_strategy
        
    @property
    def readout_qubit(self):
        """Returns the readout qubit of the circuit
        """
        return self._readout_qubit
            
    @property
    def num_param(self):
        """Number of parameters in the circuit created through the 
           add rotation layer and add entanglement layer methods
        """
        return len(self._parameters)

    def new_param(self, size:int=1) -> sp.Symbol:
        """Returns a new parameter(s) with updated array index(indices)
        
        Args:
            size: int
                Number of new parameters to return 
        
        Returns:
            New parameter(s) with updated array index(indices)
        """
        start = self.num_param
        params = np.array([sp.Symbol('%s_%s' % (self.parameter_symbol, i)) \
                          for i in range(start, start+size)])
        self._parameters = np.append(self._parameters, params)
        if len(params) == 1:
            return params[0]
        return params
        
    @property
    def parameters(self):
        """Returns an array of parameters in the circuit
        """
        return self._parameters
    
    @property
    def flatten_circuit(self):
        """Whether to flatten the circuit upon construction or modification
        """
        return self._flatten_circuit
    
    @property
    def parameter_symbol(self) -> str:
        """The symbol prefix for the arrays of parameters in the circuit
        """
        return self._parameter_symbol

    def _parse_rotation_blocks(self, rotation_blocks):
        result = ParameterisedCircuit._parse_blocks(rotation_blocks)
        ParameterisedCircuit._validate_blocks(result, SingleQubitGate)
        return result
    
    def _parse_entanglement_blocks(self, entanglement_blocks):
        result = ParameterisedCircuit._parse_blocks(entanglement_blocks)
        ParameterisedCircuit._validate_blocks(result, TwoQubitGate)
        return result
        
    @staticmethod
    def _parse_blocks(blocks) -> List:
        if not blocks:
            return []
        blocks = [blocks] if not isinstance(blocks, list) else blocks
        blocks = [QuantumCircuit._parse_gate_operation(block) \
                  if not isinstance(block, TemplateCircuitBlock) \
                  else block for block in blocks]
        return blocks
    
    @staticmethod
    def _validate_blocks(blocks, gate_feature=None) -> None:
        for block in blocks:
            if isinstance(block, TemplateCircuitBlock):
                continue
            elif isinstance(block, cirq.Gate):
                if gate_feature and \
                    not isinstance(block, gate_feature):
                    raise ValueError('Gate operation {} should be a subclass of '
                                     '{}'.format(type(block), gate_feature))
            elif callable(block):
                n_param = ParameterisedCircuit._get_parameter_count(block)
                if not n_param:
                    raise ValueError('not a valid gate operation or'
                                     'circuit block: {}'.format(block))
                dummy_params = tuple(sp.symarray('x',n_param))
                ParameterisedCircuit._validate_blocks([block(*dummy_params)], gate_feature)
        
    @staticmethod
    def _get_parameter_count(gate_expr) -> int:
        '''Returns the number of parameters required for a gate operation expression
        a gate operation expression can be a cirq.Gate instance, a string that can be mapped
        to a cirq.Gate instance, a function that maps to cirq.Gate or a TemplateCircuitBlock instance
        '''
        if isinstance(gate_expr, cirq.Gate):
            if isinstance(gate_expr, (cirq.XXPowGate, cirq.YYPowGate, cirq.ZZPowGate)):
                return 1
            return 0
        elif isinstance(gate_expr, TemplateCircuitBlock):
            return gate_expr.num_params
        elif callable(gate_expr):
            return len(signature(gate_expr).parameters)
        else:
            raise ValueError('invalid gate expression {} of type {}'.format(gate_expr, type(gate_expr)))

    def get_wavefunction(self, vals:np.ndarray):
        """Returns the simulated wavefunction of the circuit
        """
        simulator = cirq.Simulator()
        param_resolver = self.get_parameter_resolver(vals)
        return simulator.simulate(self, param_resolver=param_resolver).final_state   
    
    
    def add_readout(self, gate:Union[str, cirq.Gate]='XX',
                    readout_qubit:Optional['cirq.GridQubit']=None):
        """Adds a readout qubit to the parameterised circuit
        
        The readout qubit will be entangled to all input qubits via certain two qubit gate operations.
        
        Args:
            gate: The gate operation for entangling the readout qubit to input qubits. 
            readout_qubit: The qubit as readout. Default as (-1, -1).
        """
        parsed_gate = QuantumCircuit._parse_gate_operation(gate)
        readout_qubit = cirq.GridQubit(-1, -1) if readout_qubit is None else readout_qubit
        for qubit in self.qubits:
            final_gate = self.parameterise_gate(parsed_gate)
            self.apply_gate_operation(final_gate, (readout_qubit, qubit))
        if self.flatten_circuit:
            self.flatten()            
        self._readout_qubit = readout_qubit
    
    def readout_measurement(self):
        """Returns the readout gate operation for the readout qubit
        """
        if self.readout_qubit is None:
            raise ValueError('no readout qubit defined in the circuit')
        return cirq.Z(self.readout_qubit)
        
    def merge(self, other):
        """Merges the current circuit with another parameterised circuit
        
        This will update the parameters in the current circuit. If the current 
        circuit is flattened, the merged circuit will be flattened as well.
        
        Args:
            other: the parameterised circuit to be merged with the current circuit
        """
        self._moments = merge_pqc([self, other])._moments
        self._parameters = sp.symarray(self.parameter_symbol, len(self.symbols))
        if self.flatten_circuit:
            self.flatten()
                        
    def get_interaction_graphs(self, block_index:int, num_block_qubits:int,
                               entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                               *args, **kwargs):
        """Returns the interaction graphs for an entanglement block
        
        Args:
            block_index: int
                Index of the current entanglement block in the entanglement layer.
            num_block_qubits: int
                Number of qubits in the entanglement block. That is the number of 
                qubits involved in a gate operation of the entanglement block.
            entangle_strategy: Determines how the qubits are entangled.
                If str, it specifies the name of the strategy.
                If callable, it specifies the function to map to an interaction graph.
                If list of str, it specifies the names of a list of strategies. The 
                strategy to use is decided by the current block index. For example, if
                the circuit is building the n-th entanglement block in the entanglement layer,
                then the n-th strategy in the list will be used.
                If list of callable, it specifies the list of functions to map to an interaction
                graph. The function to use is decided by the current block index.
        Returns:
            A list of tuples specifying the interaction graphs for an entanglement block
        """
        strategy = entangle_strategy if entangle_strategy is not None else self.entangle_strategy
        if isinstance(strategy, str):
            return interaction_graph[strategy](self.n_qubit, num_block_qubits)
        elif callable(strategy):
            return strategy(self.n_qubit, num_block_qubits)
        elif isinstance(strategy, list):
            if all(isinstance(strat, str) for strat in strategy):
                return interaction_graph[strategy[block_index]](self.n_qubit, num_block_qubits)
            elif all(callable(strat) for strat in strategy):
                return strategy[block_index](self.n_qubit, num_block_qubits)
        else:
            raise ValueError('invalid entangle strategy: {}'.format(strategy))
        
    def parameterise_gate(self, gate:Union[cirq.Gate, Callable]):
        """Parameterises a gate operation
        
        The gate operation will be parameterised by new symbols from the parameterised circuit.
        This will update the parameter arrays in the circuit.
        
        Args:
            gate: The gate operation to be parameterised
        Returns:
            A parameterised gate operation
        """
        if isinstance(gate, cirq.Gate):
            if isinstance(gate, (cirq.XXPowGate, cirq.YYPowGate, cirq.ZZPowGate)):
                param = self.new_param()
                return gate**param
            return gate
        else:
            n_param = ParameterisedCircuit._get_parameter_count(gate)
            params = self.new_param(size=n_param)
            params = tuple(params) if isinstance(params, np.ndarray) else (params,)
            return gate(*params)
        
    def add_rotation_layer(self, rotation_blocks:Optional[Union[str, cirq.Gate, Callable,
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None):
        """Adds a rotation layer to the parameterised circuit
        
        Args:
            rotation_blocks: A list of single qubit gate operations to be applied in the rotation layer.
        """
        rotation_blocks = self._parse_rotation_blocks(rotation_blocks)
        for i, block in enumerate(rotation_blocks):
            if isinstance(block, TemplateCircuitBlock):
                interaction_graphs = self.get_interaction_graphs(i, block.num_block_qubits)
                for qubits in interaction_graphs:
                    block.build(self, qubits)
            else:
                for qubit in range(self.n_qubit):
                    gate = self.parameterise_gate(block)
                    self.apply_gate_operation(gate, qubit)
                
    def add_entanglement_layer(self, entanglement_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None):
        """Adds an entanglement layer to the parameterised circuit
        
        Args:
            entanglement_blocks: A list of multi qubit gate operations to be applied in the entanglement layer.
            entangle_strategy: Determines how the qubits are entangled in an entanglement block.
                If str, it specifies the name of the strategy.
                If callable, it specifies the function to map to an interaction graph.
                If list of str, it specifies the names of a list of strategies. The 
                strategy to use is decided by the current block index. For example, if
                the circuit is building the n-th entanglement block in the entanglement layer,
                then the n-th strategy in the list will be used.
                If list of callable, it specifies the list of functions to map to an interaction
                graph. The function to use is decided by the current block index.
        """       
        entangle_strategy = entangle_strategy or 'full' 
        entanglement_blocks = self._parse_entanglement_blocks(entanglement_blocks)
        for i, block in enumerate(entanglement_blocks):
            if isinstance(block, TemplateCircuitBlock):
                interaction_graphs = self.get_interaction_graphs(i, block.num_block_qubits,
                                                                entangle_strategy)
                for qubits in interaction_graphs:
                    block.build(self, qubits)
            else:
                interaction_graphs = self.get_interaction_graphs(i, 2, entangle_strategy)
                for qubits in interaction_graphs:
                    gate = self.parameterise_gate(block)
                    self.apply_gate_operation(gate, qubits)
                    
                    
    def build(self, rotation_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entanglement_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                copies:int=1, final_rotation_layer:bool=False):
        """Builds a parameterised circuit following the scheme of 
           alternating rotation and entanglement layers 
           
           Args:
               rotation_blocks: A list of single qubit gate operations to be applied in the rotation layer.
               entanglement_blocks: A list of multi qubit gate operations to be applied in the entanglement layer.
               entangle_strategy: Determines how the qubits are entangled in an entanglement block.
                   If str, it specifies the name of the strategy.
                   If callable, it specifies the function to map to an interaction graph.
                   If list of str, it specifies the names of a list of strategies. The 
                   strategy to use is decided by the current block index. For example, if
                   the circuit is building the n-th entanglement block in the entanglement layer,
                   then the n-th strategy in the list will be used.
                   If list of callable, it specifies the list of functions to map to an interaction
                   graph. The function to use is decided by the current block index.
               copies: int
                   Number of times the layers are repeated.
                   
            Examples:
                >> cq = ParameterisedCircuit(n_qubit=4)
                >> cq.build(rotation_blocks=['H','RZ'],
                            entanglement_blocks=['CNOT'],
                            entangle_strategy='linear',
                            copies=2)
                >> cq
                (0, 0): ───H───Rz(θ_0)───@───────H───Rz(θ_4)───@─────────────────
                                         │                     │
                (0, 1): ───H───Rz(θ_1)───X───@───H───Rz(θ_5)───X─────────@───────
                                             │                           │
                (0, 2): ───H───Rz(θ_2)───────X───@───H─────────Rz(θ_6)───X───@───
                                                 │                           │
                (0, 3): ───H───Rz(θ_3)───────────X───H─────────Rz(θ_7)───────X───
        """
        self.clear()
        for _ in range(copies):
            self.add_rotation_layer(rotation_blocks)
            self.add_entanglement_layer(entanglement_blocks, entangle_strategy)
            
        if final_rotation_layer:
            self.add_rotation_layer(rotation_blocks)
        if self.flatten_circuit:
            self.flatten()                    
    
    def clear(self) -> None:
        """Clears all gate operations in the circuit
        """
        super().clear()
        self._parameters = np.array([], dtype=object)
        
        
    def run_simulator(self, repetitions:int=1):
        pass
        #simulator = cirq.Simulator()
        #simulator.run(resolved_circuit, repetitions=repetitions)
        ## to get wave function:
        #simulator.simulate(resolved_circuit)
        #cirq.measure_state_vector   
        #output_state_vector = simulator.simulate(self, resolver).final_state
        #z0 = cirq.X(q0)
        #qubit_map = {q0: 0, q1: 1}
        #z0.expectation_from_wavefunction(output_state_vector, qubit_map).real