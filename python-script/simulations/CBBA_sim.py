"""
@author: Pierre Lague
@older version credit: keep9oing
"""

from algorithms.CBBA_algorithm import CBBA_agent
from utils.Task import Task
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import imageio
import os
from utils.network_topology import Network_Topology

np.random.seed(3)


class CBBA():
  def __init__(self):
    pass

  def save_plot_gif(self, phase, ax, save_gif, plot_gap, fig, filenames, t):
        ax.set_title(f"Time Step:{t}, {phase} Process")
        plt.pause(plot_gap)
        if save_gif:
            filename = f'{t}_{phase}.png'
            filenames.append(filename)
            fig.savefig(filename)


  def simulation(self, task_num, agent_num, max_t, save_gif, topology):
    net = Network_Topology()
    #topology TODO : limit the number of communications between the agents to log(num_agents) or study the KNN communication process
    #  This limits the network topologies that can be used since a connected network is required between the agents in order to route all of the bid information.
    G = None
    pos = None
    match topology:
        case 1:
            G = net.get_star_network_topology(agent_num) #does not allow single task assignement per agents because of the communication gaps between agents.
        case 2:
            G = net.get_fully_connected_network_topology(agent_num) #allows single task assignement per agents because all agents know what the others are doing.
        case 3:
            G = net.get_ring_network_topology(agent_num)#does not allow single task assignement per agents because of the communication gaps between agents.
        case 4:
            G = net.get_mesh_network_topology(agent_num)#allows single task assignement per agents because all agents know what the others are doing.
        case 5:
            G = net.get_random_network_topology(agent_num, 0.5) #random based


    #SIMULATION PARAMETERS
    #------------------------------------------------------------------------------------------------------------------------------------------+
    task_num = task_num
    agent_num = agent_num
    task = Task(task_num).get_position()
    agent_list = [CBBA_agent(id=i, vel=1, task_num=task_num, agent_num=agent_num, L_t=task.shape[0]) for i in range(agent_num)]
    t = 0 # Iteration number
    assign_plots = []
    max_t = max_t
    plot_gap = 0.1
    save_gif = save_gif
    filenames = []
    #------------------------------------------------------------------------------------------------------------------------------------------+


    fig, ax = plt.subplots()
    ax.set_xlim((-0.1,1.1))
    ax.set_ylim((-0.1,1.1))
    ax.plot(task[:,0],task[:,1],'r^',label="Task")
    robot_pos = np.array([r.position[0].tolist() for r in agent_list])
    ax.plot(robot_pos[:,0],robot_pos[:,1],'go',label="Robot")

    for i in range(agent_num-1):
      for j in range(i+1,agent_num):
        if G[i][j] == 1:
          ax.plot([robot_pos[i][0],robot_pos[j][0]],[robot_pos[i][1],robot_pos[j][1]],'g--',linewidth=1)

    handles, labels = ax.get_legend_handles_labels()
    custom_line = Line2D([0], [0], color="g",linestyle="--",label="communication")
    handles.append(custom_line)
    ax.legend(handles=handles)

    

    if save_gif:
      if not os.path.exists("my_gif"):
        os.makedirs("my_gif")

    while True:
      converged_list = []

      print(f"## Iteration {t} ##")
      ## Phase 1: Auction Process
      print("\t Phase 1 : Auction ")
      for robot_id, robot in enumerate(agent_list):
        # select task by local information
        robot.build_bundle(task)

        ## Plot
        if len(robot.p) > 0:
          x_data=[robot.position[0][0]]+task[robot.p,0].tolist()
          y_data=[robot.position[0][1]]+task[robot.p,1].tolist()
        else:
          x_data=[robot.position[0][0]]
          y_data=[robot.position[0][1]]
        if t == 0:
          assign_line, = ax.plot(x_data,y_data,'k-',linewidth=1)
          assign_plots.append(assign_line)
        else:
          assign_plots[robot_id].set_data(x_data,y_data)

      # print("Bundle")
      # for robot in agent_list:
      #   print(robot.b)
      # print("Path")
      # for robot in agent_list:
      #   print(robot.p)

      ## Plot
      self.save_plot_gif("Auction", ax, save_gif, plot_gap, fig, filenames, t)

      ## Communication stage
      print("Communicating...")
      # Send winning bid list to neighbors (depend on env)
      message_pool = [robot.send_message() for robot in agent_list]

      for robot_id, robot in enumerate(agent_list):
        # Recieve winning bidlist from neighbors
        g = G[robot_id]

        connected, = np.where(g==1)
        connected = list(connected)
        connected.remove(robot_id)

        if len(connected) > 0:
          Y = {neighbor_id:message_pool[neighbor_id] for neighbor_id in connected}
        else:
          Y = None

        robot.receive_message(Y)

      ## Phase 2: Consensus Process
      print("\t Phase 2 : Consensus")
      for robot_id, robot in enumerate(agent_list):
        # Update local information and decision
        if Y is not None:
          converged = robot.update_task()
          converged_list.append(converged)

        ## Plot
        if len(robot.p) > 0:
          x_data=[robot.position[0][0]]+task[robot.p,0].tolist()
          y_data=[robot.position[0][1]]+task[robot.p,1].tolist()
        else:
          x_data=[robot.position[0][0]]
          y_data=[robot.position[0][1]]

        assign_plots[robot_id].set_data(x_data,y_data)

      ## Save plot for gif
      self.save_plot_gif("Consensus", ax, save_gif, plot_gap, fig, filenames, t)


      # print("Bundle")
      # for robot in agent_list:
      #   print(robot.b)
      # print("Path")
      # for robot in agent_list:
      #   print(robot.p)

      t += 1

      if sum(converged_list) == agent_num:
        ax.set_title("Time Step:{}, Converged!".format(t))
        break
      if t>max_t:
        ax.set_title("Time Step:{}, Max time step overed".format(t))
        break


    if save_gif:
        filename = f'./my_gif/{t}_F.png'
        filenames.append(filename)
        plt.savefig(filename)

        #build gif
        files=[]
        for filename in filenames:
            image = imageio.imread(filename)
            files.append(image)
        imageio.mimsave("./my_gif/CBBA_simulation.gif", files, format='GIF', fps = 0.5)
        with imageio.get_writer('./my_gif/CBBA_simulation.gif', mode='I') as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)
        # Remove files
        for filename in set(filenames):
            os.remove(filename)