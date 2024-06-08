import numpy as np
from scipy.spatial import distance_matrix
import copy

class CBAA_agent:
    def __init__(self, id=0, J=None):
        self.position = np.random.uniform(low=0, high=1, size=(1, 2))
        self.num_of_tasks = J.shape[0]
        self.xj = [0 for _ in range(self.num_of_tasks)]
        self.yj = np.array([-np.inf for _ in range(self.num_of_tasks)])
        self.c = -distance_matrix(self.position, J).squeeze()
        self.id = id
        self.J = None

    def select_task(self):
        if sum(self.xj)==0:
            hi = (self.c > self.yj)
            if hi.any():
                c = copy.deepcopy(self.c)
                c[hi==False] = -np.inf 
                self.J = np.argmax(c) 
                self.xj[self.J] = 1 
                self.yj[self.J] = self.c[self.J]
        return self.xj, self.yj, self.J
    
    def get_xj(self):
        return self.xj
    
    def get_yj(self):
        return self.yj

    
    def update_task(self, Y):
        x_prev = copy.deepcopy(self.xj)
        neighbor_ids = list(Y.keys())
        neighbor_ids.insert(0, self.id)
        all_bids_list = np.array(list(Y.values()))

        if len(all_bids_list.shape) == 1:
            all_bids_list = all_bids_list[None, :]

        all_bids_list = np.vstack((self.yj[None, :], all_bids_list))
        self.yj = all_bids_list.max(0)
        winner_agent_id = np.argmax(all_bids_list[:, self.J])
        z = neighbor_ids[winner_agent_id]
        if z != self.id:
            self.xj[self.J] = 0
        converged = x_prev == self.xj
        self.update_xj(self.xj)
        self.update_yj(self.yj)
        self.update_J(self.J)
        return converged

    def send_message_in_neighborhood(self):
        return self.yj.tolist()
    
    def update_xj(self, xj):
        self.xj = xj

    def update_yj(self, yj):
        self.yj = yj

    def update_J(self, J):
        self.J = J



import multiprocessing as mp
import numpy as np
from utils import Task, Network_Topology
class CBAA_Solver:
    def __init__(self, task_num, agent_num, topology, verbose):
        self.task_num = task_num
        self.agent_num = agent_num
        self.verbose = verbose
        self.topology = topology
        self.task = Task(task_num).get_position()
        self.agents = [CBAA_agent(id=i, J=self.task) for i in range(agent_num)]

    def run_simulation(self):
        G = Network_Topology().get_fully_connected_network_topology(self.agent_num)
        t = 0
        pool = mp.Pool(mp.cpu_count())

        while True:
            converged_list = []
            if self.verbose:
                print(f"## Iteration {t} ##")
                print("\t Phase 1 : Auction")

            # Phase 1: Each agent selects a task based on their current utility values
            info = pool.map(self.select_task_wrapper, self.agents)
            
            for i, intel in enumerate(info):
                # print("xj:",intel[0])
                # print("yj:",np.array(intel[1]))
                self.agents[i].update_xj(intel[0])
                self.agents[i].update_yj(np.array(intel[1]))
                self.agents[i].update_J(intel[2])

            # Phase 2: Sending and receiving messages to/from neighbors
            neighboring_msgs = pool.map(self.send_message_in_neighborhood_wrapper, self.agents)
            if self.verbose:
                print("\t Phase 2 : Consensus")

            # Phase 3: Consensus and task update
            for agent_id, agent in enumerate(self.agents):
                g = G[agent_id]
                connected, = np.where(g == 1)
                connected = list(connected)
                connected.remove(agent_id)

                if connected:
                    Y = {neighbor_id: neighboring_msgs[neighbor_id] for neighbor_id in connected}
                else:
                    Y = None

                if Y is not None:
                    converged = pool.apply(self.update_task_wrapper, args=(agent, Y))
                    converged_list.append(converged)
            t += 1
            if all(converged_list):
                print("Converged!")
                break

        pool.close()
        pool.join()

    @staticmethod
    def select_task_wrapper(agent):
        return agent.select_task()
    
    @staticmethod
    def get_xj_wrapper(agent):
        return agent.get_xj()
    
    @staticmethod
    def get_yj_wrapper(agent):
        return agent.get_yj()

    @staticmethod
    def send_message_in_neighborhood_wrapper(agent):
        return agent.send_message_in_neighborhood()
    
    @staticmethod
    def update_task_wrapper(agent, Y):
        return agent.update_task(Y)

import matplotlib.pyplot as plt

def visualize_task_allocation(agents, tasks):
    plt.figure(figsize=(8, 8))
    
    # Plot tasks
    for i, task in enumerate(tasks):
        plt.scatter(task[0], task[1], color='blue', label=f'Task {i}')
    
    # Plot agents and their assigned tasks
    for agent in agents:
        plt.scatter(agent.position[0, 0], agent.position[0, 1], color='red', label=f'Agent {agent.id}')
        for i, task_assigned in enumerate(agent.xj):
            if task_assigned == 1:
                plt.plot([agent.position[0, 0], tasks[i][0]], [agent.position[0, 1], tasks[i][1]], color='black')
    
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Task Allocation Visualization')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    solver = CBAA_Solver(task_num=10, agent_num=10, topology="fully_connected", verbose=False)
    solver.run_simulation()
    visualize_task_allocation(solver.agents, solver.task)
