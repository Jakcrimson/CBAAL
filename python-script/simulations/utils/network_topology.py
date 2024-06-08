"""
@author : Pierre LAGUE
"""

import numpy as np


class Network_Topology():
    """
    A class for generating various network topology adjacency matrices.

    Attributes:
    - network_topology (str): The type of network topology.

    Methods:
    - get_star_network_topology(num_nodes): Generates a star network topology.
    - get_fully_connected_network_topology(num_nodes): Generates a fully connected network topology.
    - get_ring_network_topology(num_nodes): Generates a ring network topology.
    - get_mesh_network_topology(num_nodes): Generates a mesh network topology.
    - get_random_network_topology(num_nodes, density): Generates a random network topology.
    """

    def __init__(self):
        pass

    def get_star_network_topology(self, num_nodes):
        """
        Generates a star network topology adjacency matrix.

        Args:
        - num_nodes (int): Number of nodes in the network.

        Returns:
        - adjacency_matrix (ndarray): Adjacency matrix representing the star network topology.
        """
        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        center_node = num_nodes // 2
        adjacency_matrix[center_node, :] = 1
        adjacency_matrix[:, center_node] = 1
        np.fill_diagonal(adjacency_matrix, 1)
        return adjacency_matrix

    def get_fully_connected_network_topology(self, num_nodes):
        """
        Generates a fully connected network topology adjacency matrix.

        Args:
        - num_nodes (int): Number of nodes in the network.

        Returns:
        - np.ones(...) : Adjacency matrix representing the fully connected network topology.
        """
        adjacency_matrix = np.ones((num_nodes, num_nodes))

        return adjacency_matrix

    def get_ring_network_topology(self, num_nodes):
        """
        Generates a ring network topology adjacency matrix.

        Args:
        - num_nodes (int): Number of nodes in the network.

        Returns:
        - adjacency_matrix (ndarray): Adjacency matrix representing the ring network topology.
        """
        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)        
        for i in range(num_nodes):
            adjacency_matrix[i, (i + 1) % num_nodes] = 1
            adjacency_matrix[(i + 1) % num_nodes, i] = 1
        np.fill_diagonal(adjacency_matrix, 1)
    
        return adjacency_matrix

    def get_random_network_topology(self, num_nodes, density):
        """
        Generates a random network topology adjacency matrix.

        Args:
        - num_nodes (int): Number of nodes in the network.
        - density (float): Density of connections created in the network (between 0 and 1).

        Returns:
        - adjacency_matrix (ndarray): Adjacency matrix representing the random network topology.
        """
        adjacency_matrix = np.random.rand(num_nodes, num_nodes)
        threshold = 1 - density
        adjacency_matrix[adjacency_matrix > threshold] = 0
        adjacency_matrix[adjacency_matrix <= threshold] = 1
        np.fill_diagonal(adjacency_matrix, 0)
        return adjacency_matrix