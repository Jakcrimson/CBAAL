
from CBAA_sim import CBAA_plot
from CBBA_sim import CBBA_plot
import numpy
import asyncio
import argparse
import os
import time


 ## TODO : UTILISER LA PROGRAMMATION PAR ACTEUR -> deux classes, acteur solver et acteurs worker -> until les worker ont tous renvoyé stop

if "__main__" == __name__:
    parser = argparse.ArgumentParser(description="Simulation of Single/Multi-Task Assignement in a fleet of robots using Consensus-Based Algorithms")
    parser.add_argument("algorithm",        help="Algorithm to execute CBAA/CBBA",       type=str)
    parser.add_argument("method",           help="Method C/D (Centralized/Decentralized)", type=str)
    parser.add_argument("--nb_agents",        help="number of agents in the simulation",    type=int)
    parser.add_argument("--nb_tasks",         help="number of tasks in the simulation", type=int)
    parser.add_argument("--max_t",           help="maximum iteration", type=int)
    parser.add_argument("--topology",        help="network topology [(1)star, (2)fc, (3)ring (4)mesh, (5)random]", type=int)
    parser.add_argument("--viz",             help="If set, saves a gif of the simulation in the folder 'my_gif'", action="store_true")
    parser.add_argument("--v",               help="If set to true, adds verbose, else it doesn't", action="store_true")
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
        by. Pierre LAGUE, Version 0.0
""")
    
    # CBAAL.py -cbba/cbaa -nb_tasks -nb_agents -net_topo -gui/plot
    algo = args.algorithm
    nb_tasks = args.nb_tasks
    nb_agents = args.nb_agents
    max_t = args.max_t
    topology = args.topology
    viz = args.viz
    verbose = args.v
    method = args.method

    if algo == "cbaa":
        if method == "C":
            CBAA_plot().simulation(nb_tasks, nb_agents, max_t, viz, 2, verbose)
        elif method == "D":
            print("[+] The decentralized option is work in progress...")
            # simulation = Agent_Solver(nb_agents, nb_tasks, topology, False)
            # asyncio.run(simulation.run_simulation())
            # results = asyncio.run(simulation.get_results())
    else:
        if method == "C":
            CBBA_plot().simulation(nb_tasks, nb_agents, max_t, viz, 2, verbose)
        elif method == "D":
            print("[+] The decentralized option is work in progress...")


