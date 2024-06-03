
from CBAA_sim import CBAA_plot
from CBBA_sim import CBBA_plot
from CBAA_simulation_GUI import CBAA
from CBBA_simulation_GUI import CBBA
import numpy
import argparse
import os


if "__main__" == __name__:
    parser = argparse.ArgumentParser(description="Simulation of Single/Multi-Task Assignement in a fleet of robots using Consensus-Based Algorithms")
    parser.add_argument("algorithm",        help="Algorithm to execute CBAA/CBBA",       type=str)
    parser.add_argument("--nb_agents",        help="number of agents in the simulation",    type=int)
    parser.add_argument("--nb_tasks",         help="number of tasks in the simulation", type=int)
    parser.add_argument("--max_t",           help="maximum iteration", type=int)
    parser.add_argument("--topology",        help="network topology [(1)star, (2)fc, (3)ring (4)mesh, (5)random]", type=int)
    parser.add_argument("--viz",             help="If set to gui, displays the GUI viz, if not the plot viz", type=str)
    args = parser.parse_args()

    print(r"""

   ____    ____      _         _       _      
U /"___|U | __")uU  /"\  u U  /"\  u  |"|     
\| | u   \|  _ \/ \/ _ \/   \/ _ \/ U | | u   
 | |/__   | |_) | / ___ \   / ___ \  \| |/__  
  \____|  |____/ /_/   \_\ /_/   \_\  |_____| 
 _// \\  _|| \\_  \\    >>  \\    >>  //  \\  
(__)(__)(__) (__)(__)  (__)(__)  (__)(_")("_) 
          
CONSENSUS-BASED AUCTION ALGORITHMS LIBRARY
          by. Pierre LAGUE
""")
    
    # CBAAL.py -cbba/cbaa -nb_tasks -nb_agents -net_topo -gui/plot
    algo = args.algorithm
    nb_tasks = args.nb_tasks
    nb_agents = args.nb_agents
    max_t = args.max_t
    topology = args.topology
    viz = args.viz

    print(algo)

    if algo == "cbaa":
        if viz == "gui":
            CBAA().simulation(nb_tasks, nb_agents, max_t, topology)
        else:
            CBAA_plot().simulation(nb_tasks, nb_agents, max_t, True, 2)
    else:
        if viz == "gui":
            CBBA().simulation(nb_tasks, nb_agents, max_t, topology)
        else:
            CBBA_plot().simulation(nb_tasks, nb_agents, max_t, True, 2)

    


