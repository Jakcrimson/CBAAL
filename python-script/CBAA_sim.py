"""
@author : Pierre LAGUE
CBAA is considered to be a specific case of CBBA where the bundle is composed on only one task.
"""

from CBAA_algorithm import CBAA_agent
from Task import Task
from network_topology import Network_Topology
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import imageio.v2 as imageio
import numpy as np
import os


np.random.seed(3)

class CBAA():
    def __init__(self):
        print("[+] CBAA Initialized...")
        

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
                G, pos = net.get_star_network_topology(agent_num) #does not allow single task assignement per agents because of the communication gaps between agents.
            case 2:
                G, pos = net.get_fully_connected_network_topology(agent_num) #allows single task assignement per agents because all agents know what the others are doing.
            case 3:
                G, pos = net.get_ring_network_topology(agent_num)#does not allow single task assignement per agents because of the communication gaps between agents.
            case 4:
                G, pos = net.get_mesh_network_topology(agent_num)#allows single task assignement per agents because all agents know what the others are doing.
            case 5:
                G, pos = net.get_random_network_topology(agent_num, 0.5) #random based

        #SIMULATION PARAMETERS        
        #---------------------------------------------------------------------+
        task_num = task_num
        agent_num = agent_num
        task = Task(task_num).get_position()
        agent_list = [CBAA_agent(id=i, J=task) for i in range(agent_num)]          
        t = 0 # Iteration number             
        assign_plots = []             
        max_t = max_t             
        plot_gap = 0.1             
        save_gif = save_gif             
        filenames = []    
        #----------------------------------------------------------------------+

        fig, ax = plt.subplots()
        ax.set_xlim((-0.1,1.1))
        ax.set_ylim((-0.1,1.1))
        ax.plot(task[:,0],task[:,1],'r^',label="Task")
        robot_pos = np.array([r.position[0].tolist() for r in agent_list])
        ax.plot(robot_pos[:,0],robot_pos[:,1],'go',label="Robot")
        
        for i in range(agent_num-1):
            for j in range(i+1,agent_num):
                if G[i][j] == 1:
                    ax.plot([robot_pos[i][0],robot_pos[j][0]],[robot_pos[i][1],robot_pos[j][1]],'g--',linewidth=0.2)

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

            #Phase 1 : Auction process
            print("\t Phase 1 : Auction")
            for agent in agent_list:
                agent.select_task()

                #Plot Auction process
                if t == 0:
                    assign_line, = ax.plot([agent.position[0][0],task[agent.J,0]],[agent.position[0][1],task[agent.J,1]],'k-',linewidth=1)
                    assign_plots.append(assign_line)
                else:
                    assign_plots[agent_id].set_data([agent.position[0][0],task[agent.J,0]],[agent.position[0][1],task[agent.J,1]])

            ## Save plot for gif
            self.save_plot_gif("Auction", ax, save_gif, plot_gap, fig, filenames, t)

            print("\t Phase 2 : Consensus")
            #send the winning bid list to neighbors
            neighboring_msg = [agent.send_message_in_neighborhood() for agent in agent_list]

            for agent_id, agent in enumerate(agent_list):
                g = G[agent_id] # connections of the agent that is being visited
                #find connected agents by the network
                connected, = np.where(g==1)
                connected = list(connected)
                connected.remove(agent_id) #agent has been visited

                if len(connected)>0:
                    Y = {neighbor_id:neighboring_msg[neighbor_id] for neighbor_id in connected}
                else:
                    Y = None

                #update the local information and task allocation
                if Y is not None:
                    converged = agent.update_task(Y)
                    converged_list.append(converged)

                #Plot the consensus process
                if any(agent.xj):
                    assign_plots[agent_id].set_data([agent.position[0][0],task[agent.J,0]],[agent.position[0][1],task[agent.J,1]])
                else:
                    assign_plots[agent_id].set_data([agent.position[0][0],agent.position[0][0]],[agent.position[0][1],agent.position[0][1]])

            ## Save plot for gif
            self.save_plot_gif("Consensus", ax, save_gif, plot_gap, fig, filenames, t)

            t+=1
            #next iteration

            if sum(converged_list) == agent_num:
                ax.set_title("Time Step:{}, Converged!".format(t))
                break
            if t>max_t:
                ax.set_title("Time Step:{}, Max time step overed".format(t))
                break


        if save_gif:
            filename = f'./my_gif/{t}_F.png'
            filenames.append(filename)
            fig.savefig(filename)

            #build gif
            files=[]
            for filename in filenames:
                image = imageio.imread(filename)
                files.append(image)
            imageio.mimsave("./my_gif/CBAA_simulation.gif", files, format='GIF', fps=1)
            with imageio.get_writer('./my_gif/CBAA_simulation.gif', mode='I') as writer:
                for filename in filenames:
                    image = imageio.imread(filename)
                    writer.append_data(image)
            # Remove files
            for filename in set(filenames):
                os.remove(filename)


        

    