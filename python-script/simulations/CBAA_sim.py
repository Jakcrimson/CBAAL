"""
@author : Pierre LAGUE
"""

from algorithms.CBAA_algorithm import CBAA_agent
from utils.Task import Task
from utils.network_topology import Network_Topology
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import imageio.v2 as imageio
import numpy as np
import os


np.random.seed(3)

class CBAA_plot():
    """
    A class to represent the plotting and simulation of the Consensus-Based Bundle Algorithm (CBAA).

    Methods
    -------
    __init__():
        Initializes the CBAA_plot object and prints a start message.
    save_plot_gif(phase, ax, save_plot, plot_gap, fig, filenames, t):
        Saves the current plot as an image file if save_plot is True.
    simulation(task_num, agent_num, max_t, save_plot, topology, verbose):
        Runs the simulation of the CBAA algorithm with the specified parameters.
    
    """

    def __init__(self):
        pass

    def save_plot_gif(self, phase, ax, save_plot, fig, filenames, t):
        """
        Saves the current plot as an image file if save_plot is True.

        Parameters
        ----------
        phase : str
            The current phase of the algorithm ("Auction" or "Consensus").
        ax : matplotlib.axes.Axes
            The axes of the current plot.
        save_plot : bool
            If True, save the plot as an image file.
        plot_gap : float
            The gap between plots in the GIF.
        fig : matplotlib.figure.Figure
            The figure of the current plot.
        filenames : list
            The list of filenames for the saved images.
        t : int
            The current time step of the simulation.

        Returns
        -------
        None
        """
        ax.set_title(f"Time Step:{t}, {phase} Process")
        if save_plot:
            filename = f'{t}_{phase}.png'
            filenames.append(filename)
            fig.savefig(filename)

    def simulation(self, task_num, agent_num, max_t, save_plot, topology, verbose):
        """
        Runs the simulation of the CBAA algorithm with the specified parameters.

        Parameters
        ----------
        task_num : int
            The number of tasks in the simulation.
        agent_num : int
            The number of agents in the simulation.
        max_t : int
            The maximum number of iterations.
        save_plot : bool
            If True, save the simulation as a GIF.
        topology : int
            The network topology to use (1: star, 2: fully connected, 3: ring, 4: mesh, 5: random).
        verbose : bool
            If True, print detailed logs during the simulation.

        Returns
        -------
        None
        """
        self.verbose = verbose
        net = Network_Topology()
        G = net.get_fully_connected_network_topology(agent_num)
        task = Task(task_num).get_position()
        agent_list = [CBAA_agent(id=i, J=task) for i in range(agent_num)]          
        t = 0              
        assign_plots = []             
        plot_gap = 0.1             
        filenames = []    

        if save_plot:
            fig, ax = plt.subplots()
            ax.set_xlim((-0.1,1.1))
            ax.set_ylim((-0.1,1.1))
            ax.plot(task[:,0], task[:,1], 'r^', label="Task")
            robot_pos = np.array([r.position[0].tolist() for r in agent_list])
            ax.plot(robot_pos[:,0], robot_pos[:,1], 'go', label="Robot")
            
            for i in range(agent_num-1):
                for j in range(i+1, agent_num):
                    if G[i][j] == 1:
                        ax.plot([robot_pos[i][0], robot_pos[j][0]], [robot_pos[i][1], robot_pos[j][1]], 'g--', linewidth=0.2)

            handles, labels = ax.get_legend_handles_labels()
            custom_line = Line2D([0], [0], color="g", linestyle="--", label="communication")
            handles.append(custom_line)
            ax.legend(handles=handles)

            if not os.path.exists("my_gif"):
                os.makedirs("my_gif")

        print("[+] CBAA Running...")
        while True:
            converged_list = []

            if verbose:
                print(f"## Iteration {t} ##")
                print("\t Phase 1 : Auction")

            for agent in agent_list:
                agent.select_task()
                if save_plot:

                    if t == 0:
                        assign_line, = ax.plot([agent.position[0][0], task[agent.J,0]], [agent.position[0][1], task[agent.J,1]], 'k-', linewidth=1)
                        assign_plots.append(assign_line)
                    else:
                        assign_plots[agent.id].set_data([agent.position[0][0], task[agent.J,0]], [agent.position[0][1], task[agent.J,1]])

            
                    self.save_plot_gif("Auction", ax, save_plot, fig, filenames, t)

            if verbose:
                print("\t Phase 2 : Consensus")

            neighboring_msg = [agent.send_message_in_neighborhood() for agent in agent_list]

            for agent_id, agent in enumerate(agent_list):
                g = G[agent_id]
                connected, = np.where(g == 1)
                connected = list(connected)
                connected.remove(agent_id)

                if len(connected) > 0:
                    Y = {neighbor_id: neighboring_msg[neighbor_id] for neighbor_id in connected}
                else:
                    Y = None

                if Y is not None:
                    converged = agent.update_task(Y)
                    converged_list.append(converged)
                if save_plot:
                    if any(agent.xj):
                        assign_plots[agent_id].set_data([agent.position[0][0], task[agent.J,0]], [agent.position[0][1], task[agent.J,1]])
                    else:
                        assign_plots[agent_id].set_data([agent.position[0][0], agent.position[0][0]], [agent.position[0][1], agent.position[0][1]])

                
                    self.save_plot_gif("Consensus", ax, save_plot, fig, filenames, t)

            t += 1

            if sum(converged_list) == agent_num:
                if save_plot:
                    ax.set_title(f"Time Step:{t}, Converged!")
                break
            if t > max_t:
                if save_plot:
                    ax.set_title(f"Time Step:{t}, Max time step overed")
                break

        if save_plot:
            filename = f'./my_gif/{t}_F.png'
            filenames.append(filename)
            fig.savefig(filename)

            files = []
            for filename in filenames:
                image = imageio.imread(filename)
                files.append(image)
            imageio.mimsave("./my_gif/CBAA_simulation.gif", files, format='GIF', fps=1)
            with imageio.get_writer('./my_gif/CBAA_simulation.gif', mode='I') as writer:
                for filename in filenames:
                    image = imageio.imread(filename)
                    writer.append_data(image)
            for filename in set(filenames):
                os.remove(filename)

        

    