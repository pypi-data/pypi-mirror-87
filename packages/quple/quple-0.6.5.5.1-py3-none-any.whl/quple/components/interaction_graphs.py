from typing import List, Tuple
import itertools


"""
Interaction graphs determine how qubits are connected in terms of multi-qubit operations.
An interaction graph accepts two inputs, n and m. Here n refers to the number of qubits in
the system and m is the number of qubits involved in the multi-qubit interaction
"""
    
def nearest_neighbor(n:int, m:int=2) -> List[Tuple[int]]:
    """The nearest neighbor interaction
    
    In the nearest neighbor interaction, each qubit is connected to its
    next nearest neighbor in a linear manner. 
    
    Examples:
    # Nearest neighbor interaction graph for 4 qubit system with 2 qubit interaction
    >> nearest_neighbor(n=4, m=2)  
    [(0, 1), (1, 2), (2, 3)]
    # Building a circuit of 4 qubits with a layer of CNOT gates using
    # the nearest neighbor interaction graph
    >> cq = ParameterisedCircuit(n_qubit=4)
    >> cq.add_entanglement_layer(['CNOT'], entangle_strategy=nearest_neighbor)
    >> cq
    (0, 0): ───@───────────
               │
    (0, 1): ───X───@───────
                   │
    (0, 2): ───────X───@───
                       │
    (0, 3): ───────────X───
    
    
    Args:
        n: int
        Number of qubits in the system
        m: int
        Number of qubits involved in the multi-qubit interaction
        
    Returns:
        A list of tuples of qubit indices. Each tuple specifies the indices of the
        qubits that are involved in the multi-qubit interaction. 
    """
    return [tuple(range(i, i+m)) for i in range(n - m + 1)]    

def cyclic(n:int, m:int=2) -> List[Tuple[int]]:
    """The cyclic interaction
    
    In the cyclic interaction, each qubit is connected to its
    next nearest neighbor in a circular manner.

    Examples:
    # Cyclic interaction graph for 4 qubit system with 2 qubit interaction
    >> cyclic(n=4, m=2) 
    [(0, 1), (1, 2), (2, 3), (3, 0)]
    # Building a circuit of 4 qubits with a layer of CNOT gates using
    # the cyclic interaction graph
    >> cq = ParameterisedCircuit(n_qubit=4)
    >> cq.add_entanglement_layer(['CNOT'], entangle_strategy=cyclic)
    >> cq
    (0, 0): ───@───────────X───
               │           │
    (0, 1): ───X───@───────┼───
                   │       │
    (0, 2): ───────X───@───┼───
                       │   │
    (0, 3): ───────────X───@───
    
    
    Args:
        n: int
        Number of qubits in the system
        m: int
        Number of qubits involved in the multi-qubit interaction
        
    Returns:
        A list of tuples of qubit indices. Each tuple specifies the indices of the
        qubits that are involved in the multi-qubit interaction. 
    """    
    return nearest_neighbor(n,m) + [tuple(range(n - m + 1, n)) + (0,)]

def fully_connected(n:int, m:int=2) -> List[Tuple[int]]:
    """The fully-connected interaction
    
    In the fully-connected interaction, every distinct unordered tuple of m qubits
    are connected exactly once. 
    
    Examples:
    # Fully connected interaction graph for 4 qubit system with 2 qubit interaction
    >> fully_connected(n=4, m=2)  
    [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    # Building a circuit of 4 qubits with a layer of CNOT gates using
    # the fully connected interaction graph
    >> cq = ParameterisedCircuit(n_qubit=4)
    >> cq.add_entanglement_layer(['CNOT'], entangle_strategy=fully_connected)
    >> cq
                       ┌──┐
    (0, 0): ───@───@────@─────────────
               │   │    │
    (0, 1): ───X───┼────┼@────@───────
                   │    ││    │
    (0, 2): ───────X────┼X────┼───@───
                        │     │   │
    (0, 3): ────────────X─────X───X───
                       └──┘
    
    Args:
        n: int
        Number of qubits in the system
        m: int
        Number of qubits involved in the multi-qubit interaction
        
    Returns:
        A list of tuples of qubit indices. Each tuple specifies the indices of the
        qubits that are involved in the multi-qubit interaction. 
    """        
    return list(itertools.combinations(list(range(n)), m))

def all_to_all(n:int, m:int=2) -> List[Tuple[int]]:
    """The all-to-all interaction
    
    In the fully-connected interaction, every distinct ordered tuple of m qubits
    are connected.
    
    Examples:
    # All to all interaction graph for 4 qubit system with 2 qubit interaction
    >> all_to_all(n=4, m=2)  
    [(0, 1),
     (0, 2),
     (0, 3),
     (1, 0),
     (1, 2),
     (1, 3),
     (2, 0),
     (2, 1),
     (2, 3),
     (3, 0),
     (3, 1),
     (3, 2)]
    # Building a circuit of 4 qubits with a layer of CNOT gates using
    # the all to all interaction graph
    >> cq = ParameterisedCircuit(n_qubit=4)
    >> cq.add_entanglement_layer(['CNOT'], entangle_strategy=all_to_all)
    >> cq
                                   ┌──┐
    (0, 0): ───@───@───@───X─────────X────────────X───────────
               │   │   │   │         │            │
    (0, 1): ───X───┼───┼───@───@────@┼────X───────┼───X───────
                   │   │       │    ││    │       │   │
    (0, 2): ───────X───┼───────X────┼@────@───@───┼───┼───X───
                       │            │         │   │   │   │
    (0, 3): ───────────X────────────X─────────X───@───@───@───
                                   └──┘

    Args:
        n: int
        Number of qubits in the system
        m: int
        Number of qubits involved in the multi-qubit interaction
        
    Returns:
        A list of tuples of qubit indices. Each tuple specifies the indices of the
        qubits that are involved in the multi-qubit interaction. 
    """        
    return list(itertools.permutations(list(range(n)), m))

def star(n:int, m:int=2) -> List[Tuple[int]]:
    """The star interaction
    
    In the star interaction, the first qubit is connected to every other qubit.
    
    Examples:
    # Star interaction graph for 4 qubit system with 2 qubit interaction
    >> star(n=4, m=2)  
    [(0, 1), (0, 2), (0, 3)]
    # Building a circuit of 4 qubits with a layer of CNOT gates using
    # the fully connected interaction graph
    >> cq = ParameterisedCircuit(n_qubit=4)
    >> cq.add_entanglement_layer(['CNOT'], entangle_strategy=star)
    >> cq
    (0, 0): ───@───@───@───
               │   │   │
    (0, 1): ───X───┼───┼───
                   │   │
    (0, 2): ───────X───┼───
                       │
    (0, 3): ───────────X───
    
    Args:
        n: int
        Number of qubits in the system
        m: int
        Number of qubits involved in the multi-qubit interaction
        
    Returns:
        A list of tuples of qubit indices. Each tuple specifies the indices of the
        qubits that are involved in the multi-qubit interaction. 
    """        
    if m != 2:
        raise ValueError('the connectiviy graphs of the "star" method'
                         ' requires 2 qubits in an interaction unit'
                        ' but {} is given'.format(m))
    return [(0, i+1) for i in range(n - m + 1)]

def alternate_linear(n:int, m:int=2) -> List[Tuple[int]]:
    if m > 2:
        raise ValueError('The "alternate linear" connectivity graphs requires <= 2 '
                         'qubits in the interaction unit'
                        ' but {} is given'.format(m))
    if n < 2:
        raise ValueError('The "alternate linear" connectivity graphs requires at least '
                         '2 qubits in the circuit')
    if m == 2:
        return [(i, i+1) for i in range(0, n - 1, m)] + [(i+1, i+2) for i in range(0, n - 2, m)]  
    else:
        return [(i,) for i in range(n)]

# dictionary for mapping a str to the corresponding interaction graph
interaction_graph = {
    'nearest_neighbor': nearest_neighbor,
    'linear': nearest_neighbor,
    'cyclic': cyclic,
    'circular': cyclic,
    'full': fully_connected,
    'fully_connected': fully_connected,
    'all_to_all': all_to_all,
    'star': star,
    'alternate_linear': alternate_linear
}