"""
@new version : Pierre Lague
@old version : keep9oing
"""

import numpy as np
import copy

class CBBA_agent():
  """
    A class to represent an agent in the Consensus-Based Bundle Algorithm (CBBA) for multi-task assignment in a fleet of robots.

    Attributes
    ----------
    id : int
        The unique identifier for the agent.
    vel : float
        The velocity of the agent.
    task_num : int
        The number of tasks available in the simulation.
    agent_num : int
        The number of agents participating in the simulation.
    z : numpy.ndarray
        Local winning agent list initialized with the agent's id.
    y : numpy.ndarray
        Local winning bid list initialized with zeros.
    b : list
        Bundle list for tasks assigned to the agent.
    p : list
        Path list for the sequence of tasks.
    L_t : int
        Maximum number of tasks an agent can handle.
    time_step : int
        Local clock for the agent.
    s : dict
        Time stamp list for the agent's updates.
    position : numpy.ndarray
        Position of the agent in a 2D space.
    c : numpy.ndarray
        Initial score list based on Euclidean distance.
    Lambda : float
        Parameter for the score function.
    c_bar : numpy.ndarray
        Score function parameters.

    Methods
    -------
    tau(j):
        Estimate the time the agent will take to arrive at task j's location.
    set_position(position):
        Set the position of the agent.
    send_message():
        Return the local winning bid list, winning agent list, and time stamp list.
    receive_message(Y):
        Receive and store messages from neighboring agents.
    build_bundle(task):
        Construct bundle and path list with local information.
    update_task():
        Update task assignments based on messages received from neighbors and apply CBBA rules.
    __update(j, y_kj, z_kj):
        Update the bid and winning agent for task j.
    __reset(j):
        Reset the bid and winning agent for task j.
    __leave():
        Placeholder for no action.
    """
  

  def __init__(self, id = None, vel=None, task_num = None, agent_num = None, L_t = None):
    """
      Constructs all the necessary attributes for the CBBA agent.

      Parameters
      ----------
      id : int, optional
          The unique identifier for the agent (default is None).
      vel : float, optional
          The velocity of the agent (default is None).
      task_num : int, optional
          The number of tasks available in the simulation (default is None).
      agent_num : int, optional
          The number of agents participating in the simulation (default is None).
      L_t : int, optional
          Maximum number of tasks an agent can handle (default is None).
    """
    self.task_num = task_num
    self.agent_num = agent_num
    # Agent information
    self.id = id
    self.vel = vel

    # Local Winning Agent List
    self.z = np.ones(self.task_num, dtype=np.int8) * self.id
    # Local Winning Bid List
    self.y = np.array([ 0 for _ in range(self.task_num)], dtype=np.float64)
    # Bundle
    self.b = []
    # Path
    self.p = []
    # Maximum Task Number
    self.L_t = L_t
    # Local Clock
    self.time_step = 0
    # Time Stamp List
    self.s = {a:self.time_step for a in range(self.agent_num)}

    # This part can be modified depend on the problem
    self.position = np.random.uniform(low=0, high=1, size=(1,2)) # Agent position (Position)
    self.c = np.zeros(self.task_num) # Initial Score (Euclidean Distance)

    # socre function parameters
    self.Lambda = 0.95
    self.c_bar = np.ones(self.task_num)

  def tau(self,j):
    """
        Estimate the time the agent will take to arrive at task j's location.
        This function can be used later.

        Parameters
        ----------
        j : int
            The task index.

        Returns
        -------
        None
      """
    pass

  def set_position(self, position):
    """
        Set the position of the agent.

        Parameters
        ----------
        position : numpy.ndarray
            The new position of the agent in a 2D space.

        Returns
        -------
        None
        """
    self.position = position

  def send_message(self):
    """
        Return the local winning bid list, winning agent list, and time stamp list.

        Returns
        -------
        y : list
            Local winning bid list.
        z : list
            Local winning agent list.
        s : dict
            Time stamp list.
        """
    return self.y.tolist(), self.z.tolist(), self.s

  def receive_message(self, Y):
    """
        Receive and store messages from neighboring agents.

        Parameters
        ----------
        Y : dict
            Messages from neighboring agents.

        Returns
        -------
        None
    """
    
    self.Y = Y

  def build_bundle(self, task):
    """
        Construct the bundle and path list with local information.

        Parameters
        ----------
        task : list
            List of task positions.

        Returns
        -------
        None
    """
    J = [j for j in range(self.task_num)]

    while len(self.b) < self.L_t:
      # Calculate S_p for constructed path list
      S_p = 0
      if len(self.p) > 0:
        distance_j = 0
        distance_j += np.linalg.norm(self.position.squeeze()-task[self.p[0]])
        S_p += (self.Lambda**(distance_j/self.vel)) * self.c_bar[self.p[0]]
        for p_idx in range(len(self.p)-1):
          distance_j += np.linalg.norm(task[self.p[p_idx]]-task[self.p[p_idx+1]])
          S_p += (self.Lambda**(distance_j/self.vel)) * self.c_bar[self.p[p_idx+1]]

      # Calculate c_ij for each task j
      best_pos = {}
      for j in J:
        c_list = []
        if j in self.b: # If already in bundle list
          self.c[j] = 0 # Minimum Score
        else:
          for n in range(len(self.p)+1):
            p_temp = copy.deepcopy(self.p)
            p_temp.insert(n,j)
            c_temp = 0
            distance_j = 0
            distance_j += np.linalg.norm(self.position.squeeze()-task[p_temp[0]])
            c_temp += (self.Lambda**(distance_j/self.vel)) * self.c_bar[p_temp[0]]
            if len(p_temp) > 1:
              for p_loc in range(len(p_temp)-1):
                distance_j += np.linalg.norm(task[p_temp[p_loc]]-task[p_temp[p_loc+1]])
                c_temp += (self.Lambda**(distance_j/self.vel)) * self.c_bar[p_temp[p_loc+1]]

            c_jn = c_temp-S_p
            c_list.append(c_jn)

          max_idx = np.argmax(c_list)
          c_j = c_list[max_idx]
          self.c[j] = c_j
          best_pos[j] = max_idx

      h = (self.c > self.y)
      if sum(h)==0:# No valid task
        break
      self.c[~h] = 0
      J_i = np.argmax(self.c)
      n_J = best_pos[J_i]

      self.b.append(J_i)
      self.p.insert(n_J,J_i)

      self.y[J_i] = self.c[J_i]
      self.z[J_i] = self.id


  def update_task(self):
    """
        Update task assignments based on messages received from neighbors and apply CBBA rules.

        Returns
        -------
        converged : bool
            True if the task assignments have converged, otherwise False.
    """

    old_p = copy.deepcopy(self.p)

    id_list = list(self.Y.keys())
    id_list.insert(0, self.id)

    # Update time list
    for id in list(self.s.keys()):
      if id in id_list:
        self.s[id] = self.time_step
      else:
        s_list = []
        for neighbor_id in id_list[1:]:
          s_list.append(self.Y[neighbor_id][2][id])
        if len(s_list) > 0:
          self.s[id] = max(s_list)

    ## Update Process
    for j in range(self.task_num):
      for k in id_list[1:]:
        y_k = self.Y[k][0]
        z_k = self.Y[k][1]
        s_k = self.Y[k][2]

        z_ij = self.z[j]
        z_kj = z_k[j]
        y_kj = y_k[j]

        i = self.id
        y_ij = self.y[j]

        ## Rule Based Update
        # Rule 1~4
        if z_kj == k:
          # Rule 1
          if z_ij == self.id:
            if y_kj > y_ij:
              self.__update(j,y_kj,z_kj)
            elif abs(y_kj - y_ij) < np.finfo(float).eps: # Tie Breaker
              if k < self.id:
                self.__update(j,y_kj,z_kj)
            else:
              self.__leave()
          # Rule 2
          elif z_ij == k:
            self.__update(j,y_kj,z_kj)
          # Rule 3
          elif z_ij != -1:
            m = z_ij
            if (s_k[m] > self.s[m]) or (y_kj > y_ij):
              self.__update(j,y_kj,z_kj)
            elif abs(y_kj-y_ij) < np.finfo(float).eps: # Tie Breaker
              if k < self.id:
                self.__update(j,y_kj,z_kj)
          # Rule 4
          elif z_ij == -1:
            self.__update(j,y_kj,z_kj)
          else:
            raise Exception("Error while updating")
        # Rule 5~8
        elif z_kj == i:
          # Rule 5
          if z_ij == i:
            self.__leave()
          # Rule 6
          elif z_ij == k:
            self.__reset(j)
          # Rule 7
          elif z_ij != -1:
            m = z_ij
            if s_k[m] > self.s[m]:
              self.__reset(j)
          # Rule 8
          elif z_ij == -1:
            self.__leave()
          else:
            raise Exception("Error while updating")
        # Rule 9~13
        elif z_kj != -1:
          m = z_kj
          # Rule 9
          if z_ij == i:
            if (s_k[m]>=self.s[m]) and (y_kj > y_ij):
              self.__update(j,y_kj,z_kj)
            elif (s_k[m]>=self.s[m]) and (abs(y_kj-y_ij) < np.finfo(float).eps): # Tie Breaker
              if m < self.id:
                self.__update(j,y_kj,z_kj)
          # Rule 10
          elif z_ij == k:
            if (s_k[m]>self.s[m]):
              self.__update(j,y_kj,z_kj)
            else:
              self.__reset(j)
          # Rule 11
          elif z_ij == m:
            if (s_k[m] > self.s[m]):
              self.__update(j,y_kj,z_kj)
          # Rule 12
          elif z_ij != -1:
            n = z_ij
            if (s_k[m] > self.s[m]) and (s_k[n] > self.s[n]):
              self.__update(j,y_kj,z_kj)
            elif (s_k[m] > self.s[m]) and (y_kj > y_ij):
              self.__update(j,y_kj,z_kj)
            elif (s_k[m]>self.s[m]) and (abs(y_kj-y_ij) < np.finfo(float).eps): # Tie Breaker
              if m < n:
                self.__update(j,y_kj,z_kj)
            elif (s_k[n]>self.s[n]) and (self.s[m]>s_k[m]):
              self.__update(j,y_kj,z_kj)
          # Rule 13
          elif z_ij == -1:
            if (s_k[m] > self.s[m]):
              self.__update(j,y_kj,z_kj)
          else:
            raise Exception("Error while updating")
        # Rule 14~17
        elif z_kj == -1:
          # Rule 14
          if z_ij == i:
            self.__leave()
          # Rule 15
          elif z_ij == k:
            self.__update(j,y_kj,z_kj)
          # Rule 16
          elif z_ij != -1:
            m = z_ij
            if s_k[m] > self.s[m]:
              self.__update(j,y_kj,z_kj)
          # Rule 17
          elif z_ij == -1:
            self.__leave()
          else:
            raise Exception("Error while updating")
        else:
          raise Exception("Error while updating")

    n_bar = len(self.b)
    # Get n_bar
    for n in range(len(self.b)):
      b_n = self.b[n]
      if self.z[b_n] != self.id:
        n_bar = n
        break

    b_idx1 = copy.deepcopy(self.b[n_bar+1:])

    if len(b_idx1) > 0:
      self.y[b_idx1] = 0
      self.z[b_idx1] = -1

    if n_bar < len(self.b):
      del self.b[n_bar:]

    self.p = []
    for task in self.b:
      self.p.append(task)

    self.time_step += 1

    converged = False
    if old_p == self.p:
      converged = True

    return converged


  def __update(self, j, y_kj, z_kj):
    """
        Update the bid and winning agent for task j.

        Parameters
        ----------
        j : int
            Task index.
        y_kj : float
            Winning bid for task j.
        z_kj : int
            Winning agent for task j.

        Returns
        -------
        None
    """
    self.y[j] = y_kj
    self.z[j] = z_kj

  def __reset(self, j):
    """
        Reset the bid and winning agent for task j.

        Parameters
        ----------
        j : int
            Task index.

        Returns
        -------
        None
    """
    self.y[j] = 0
    self.z[j] = -1 # -1 means "none"

  def __leave(self):
    """
        Placeholder for no action.

        Returns
        -------
        None
    """
    pass
