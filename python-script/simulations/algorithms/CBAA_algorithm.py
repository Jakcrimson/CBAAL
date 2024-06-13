"""
@new version : Pierre Lague
"""

# TODO : CHANGE J NAME TO TASKS !!!!!!! TODO TODO 

import numpy as np
from scipy.spatial import distance_matrix
import copy
import pykka #library used for the distributed version of the program

class CBAA_agent(pykka.ThreadingActor): # Threading actor 
    def __init__(self, id=0, J=None):
        super().__init__()

        
        # ADDITIONAL PARAMETERS FOR VISUALIZATION
        #-------------------------------------------------------------------------------------------+
        #position of the agent
        #depending on the problem, here the agents are spread into a 2D space
        self.position = np.random.uniform(low=0, high=1, size=(1, 2))
        #-------------------------------------------------------------------------------------------+
        
        self.J = J
        #PARAMETERS FROM THE CHOI ET AL. PAPER
        #-------------------------------------------------------------------------------------------+
        self.num_of_tasks = J.shape[0]

        #local task assignement xij
        #xij = 1 if agent i is assigned to task j
        self.xj = [0 for i in range(self.num_of_tasks)]

        #local winning bid list
        #list of integer for each task in J
        # THIS INFORMATION IS SHARED AMONG AGENTS CONNECTED IN THE NETWORK
        self.yj = np.array([-np.inf for _ in range(self.num_of_tasks)])
        
        #agent's bid on a task, which is a score here defined by the euclidean distance
        #it is possible to change the nature of the score to see if it impacts performance
        self.c = -distance_matrix(self.position, J).squeeze()

        #agent ID
        self.id = id
        #-------------------------------------------------------------------------------------------+


    def get_position(self):
        """Returns the agent's position.

        Returns:
            tuple: The position of the agent, initialized as a random 2-uple for 2D space coordinates.
        """
        return self.position

    def get_J(self):
        """Returns the task assigned to the agent.

        Returns:
            int: The index of the task assigned to the agent.
        """
        return self.J

    def get_xj(self):
        """Returns the local task assignment of the agent.

        Returns:
            list: A list representing the local task assignment of the agent. 
                Each element indicates whether the agent is assigned to the corresponding task (1) or not (0).
        """
        return self.xj

        
    def select_task(self): #TODO : SINGATURE !!!
        """Phase 1 of the CBAA Algorithm
        Acts for the allocation of tasks for an agent.
        Selects the task of the valid tasks list hi based on the highest score in the current list of winning bids.
        If an agent has already been assigned, this phase is skipped.
        """
        # this function is executed for each agents in the environment
        
        # if an agent has no assignement (since it's a single task assignment)
        if sum(self.xj)==0:
            #valid tasks list
            # if there are no bid that would make the task "winnable"
            hi = (self.c > self.yj)

            #if there are any elements equal to 1 i.e. if a task is winnable
            if hi.any():
                c = copy.deepcopy(self.c)
                c[hi==False] = -np.inf 

                self.J = np.argmax(c) #the task with the highest bid
                self.xj[self.J] = 1 #we assign the task to the current agent and hope for the best during phase 2
                self.yj[self.J] = self.c[self.J] #the winning bid list is updated with the value of the highest bid on the task
        return self.xj, self.yj

    def update_task(self, Y=None):
        """Phase 2 of the CBAA Algorithm
        Acts as the conflit resolution (consensus) of tasks assignement in a neighborhood.
        The list of winning bids of the neighbors is passed as a parameter.
        The task is assigned to the agent with the largest bid in the neighborhood.
        An agent looses it's assignement when it is outbid.

        Args:
            Y (dict{neighbor_agent_id:bid_list}): Winning bid list of a neighboring agent. Defaults to None.
        """
        x_prev = copy.deepcopy(self.xj)
        neighbor_ids = list(Y.keys())
        neighbor_ids.insert(0, self.id)

        all_bids_list = np.array(list(Y.values()))

        #Update local winning bid list 
        
        # if no neighbor
        if len(all_bids_list.shape)==1:
            all_bids_list = all_bids_list[None,:]

        #update the agent's local winning bid list and the neighbor's winning bid list
        all_bids_list = np.vstack((self.yj[None, :], all_bids_list))

        #take the maximum value in the bidding list
        self.yj = all_bids_list.max(0) #param 0 : axis zero the stack

        # Verify if agents are not outbid
        winner_agent_id = np.argmax(all_bids_list[:,self.J])
        z = neighbor_ids[winner_agent_id] #winner of the bid

        #if self is not the winner
        if z!=self.id:
            #unassign the self agent
            self.xj[self.J]=0

        converged = False

        if x_prev == self.xj: #if there has been no change in the environment, no new assignement, then we have converged.
            converged = True

        return converged



    def send_message_in_neighborhood(self):
        """Returns the local winning bid list to tranfer to nearby agents

        Returns:
            yj:list -> local winning bid list
        """
        return self.yj.tolist()
    
    
