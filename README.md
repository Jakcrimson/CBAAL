```
   ____    ____      _         _       _      
U /"___|U | __")uU  /"\  u U  /"\  u  |"|     
\| | u   \|  _ \/ \/ _ \/   \/ _ \/ U | | u   
 | |/__   | |_) | / ___ \   / ___ \  \| |/__  
  \____|  |____/ /_/   \_\ /_/   \_\  |_____| 
 _// \\  _|| \\_  \\    >>  \\    >>  //  \\  
(__)(__)(__) (__)(__)  (__)(__)  (__)(_")("_)
  CONSENSUS-BASED AUCTION ALGORITHM LIBRARY
            by Pierre LAGUE
```

# CBAAL - Consensus Based Auction Algorithm Library

## Overview

CBAAL is a library developed as part of my end-of-year assignment for my first-year master's degree. It focuses on implementing consensus-based auction algorithms (CBAA) and consensus-based bundle algorithm (CBBA) primarily for dynamic load balancing problems. The algorithms implemented in this library are inspired by the publication of Choi et al., which introduced these innovative approaches to solving load balancing challenges in dynamix environments. 📚💼




## CBAA - Consensus Based Auction Algorithm - Single Task Assignement

According to Choi et Al., the consensus-based auction algorithm (CBAA) is a single assignment strategy that makes use of both auction and consensus. The algorithm consists of iterations between two phases. The first phase of the algorithm is the auction process, while the second is a consensus algorithm that is used to converge on a winning bids list. By iterating between the two, CBAA can exploit convergence properties of decentralized consensus algorithms as well as the robustness and computational efficiency of the auction algorithms.

### Phase 1 : The Auction process

In this phase, each agents places a bid on a task asynchronously with the rest of the fleet. Let $c_{ij}$ be the bid that is placed on a task. In CBAAL, we consider this bid to be the euclidean distance between an agent and a task. Initially multiple agents may bid on the same task. In this phase, two vectors of lenght $N_t$ are also defined ($N_t$ being the number of tasks in the simulation). They are both initialized as zero vectors.
- the first vector is $x_i$, that is the agents task list. If $x_{ij}=1$, agent $i$ has been assigned to task $j$, and 0 otherwise.
- the second vector is $y_i$, that is the winning bid list. It is an up-to-date estimate of the highest bid made for each task in the simulation.

After the definition of these two vectors, the valid tasks list $h_i$ is defined as $$h_{ij} = \mathbb{1} (c_{ij} > y_{ij}), \forall j \in J$$
An unnasigned agent $i$ will compute the valid task list $h_i$. If there are valid tasks, it then select the task $j*$ giving it the maximum score based on the current winning bid list, and updates its task list $x_i$ and winning bid list $y_i$ accordingly. In the case where an agent has already been assigned a task, this auction phase is skipped and the agent jumps to phase 2 : Consensus Process.

### Phase 2 : Consensus Process

The second phase of the CBAA is the consensus section of the algorithm. Here, agents make use of a consensus strategy to converge on the list of winning bids, and use that list to determine the winner. This allows conflict resolution over all tasks while not limiting the network to a specific structure.

The simulation uses a network represented as a graph and its adjacency matrix. The network $\mathbb{G}(\tau)$, is the undirected communication network at time $\tau$ with a symetric adjacency matrix $g(\tau)$. This adjacency matrix is defined such that $g(\tau) _{ik}=1$ if a link exists between agents $i$ and $k$, and 0 otherwise. Agents $i$ and $k$ are said to be *neighbors* if such a link exists. For the implementation and as convention, each agent is a neighbor to himself (self connection nodes, $g(\tau)_{ii}=1$).

At each iteration of phase 2, each agents receives, and transmits their winning bid list $y_i$ and the consensus is reached in a way that each agent $i$ replaces its $y_ij$ values with the largest value between itself and its neighbors. Also, if an agent is outbid, it looses it's assignement and jumps back to phase 1.


## CBBA - Consensus-Based Bundle Algorithm - Multi-Task Assignement

Choi et al. define CBBA as an extension to the single-assignment problem. In CBBA, each agent has a list of tasks potentially assigned to itself, but the auction process is done at the task level rather than at the bundle level. Similar to CBAA, CBBA consists of iterations between two phases – bundle construction and conflict resolution.

### Phase 1 : Bundle Construction

During phase 1 of the algorithm, each agent continuously adds tasks to its bundle until it is incapable of adding any others. The tasks are added into the bundle in the following way. 
- each agent 

## Features

- Implementation of CBAA and CBBA algorithms.
- Designed for dynamic load balancing scenarios.
- Provides a framework for simulating load balancing strategies over various network topologies.
- Well-documented codebase for easy understanding and modification. 🛠️📝

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CBAAL.git
   ```

2. Navigate to the cloned directory:
   ```
   cd CBAAL
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

After a simulation a gif will be saved showing you the process of the task assignement : 
![](https://github.com/Jakcrimson/CBAAL/blob/master/python-script/my_gif/simulation.gif)

## Documentation

Detailed documentation can be found in scripts of the repository. This includes explanations of the algorithms, and relevant remarks about the code and theory behind the algorithms. 📖🔍

## Contribution

Contributions to the project are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository. 🚀👥

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details. 📜

## Acknowledgements

We would like to express our gratitude to Choi et al [https://dspace.mit.edu/bitstream/handle/1721.1/52330/Choi_Consensus-Based-Decentralized.pdf?sequence=2] . for their pioneering work in consensus-based auction algorithms, which served as the inspiration for this project. 🙏

## Contact

For any inquiries or questions regarding the library, please contact [pierre.lague @ protonmail.com]. 📧

---
