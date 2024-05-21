import pygame
import numpy as np
from utils.Task import Task
from utils.network_topology import Network_Topology
from algorithms.CBAA_algorithm import CBAA_agent
import time

class CBAA:
    def __init__(self):
        print("[+] CBAA Initialized...")

    def simulation(self, task_num, agent_num, max_t, topology):
        net = Network_Topology()
        G = net.get_fully_connected_network_topology(agent_num)

        #SIMULATION PARAMETERS        
        #---------------------------------------------------------------------+
        task_num = task_num
        agent_num = agent_num
        task = Task(task_num).get_position()
        agent_list = [CBAA_agent(id=i, J=task) for i in range(agent_num)]          
        t = 0 # Iteration number             
        max_t = max_t             
        #----------------------------------------------------------------------+

        # Initialize pygame
        pygame.init()
        screen_size = 600
        screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption('CBAA Simulation')

        # Colors
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)
        BLUE = (0, 0, 255)

        clock = pygame.time.Clock()
        running = True
        scale = screen_size - 40  # Scale for better visualization
        font = pygame.font.SysFont(None, 24)  # Font for displaying agent IDs

        def draw_legend(screen):
            legend_x = screen_size - 150
            legend_y = 10
            line_height = 25

            legend_items = [
                ("Agents", BLUE),
                ("Tasks", RED),
                ("Comm Links", BLACK),
                ("Exit : Esc", BLACK)
            ]

            for i, (text, color) in enumerate(legend_items):
                pygame.draw.line(screen, color, (legend_x, legend_y + i * line_height), (legend_x + 20, legend_y + i * line_height), 5)
                legend_text = font.render(text, True, BLACK)
                screen.blit(legend_text, (legend_x + 30, legend_y + i * line_height - 10))

        while running:
            screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            converged_list = []

            print(f"## Iteration {t} ##")
            #Phase 1: Auction process
            print("\t Phase 1 : Auction")
            for agent in agent_list:
                agent.select_task()

            #Phase 2 : Consensus process
            print("\t Phase 2 : Consensus")
            neighboring_msg = [agent.send_message_in_neighborhood() for agent in agent_list]

            for agent_id, agent in enumerate(agent_list):
                g = G[agent_id]# connections of the agent that is being visited
                #find connected agents by the network
                connected = list(np.where(g == 1)[0])
                connected.remove(agent_id)#agent has been visited
                
                Y = {neighbor_id: neighboring_msg[neighbor_id] for neighbor_id in connected} if connected else None
                
                #update the local information and task allocation
                if Y is not None:
                    converged = agent.update_task(Y)
                    converged_list.append(converged)

            for agent in agent_list:
                if any(agent.xj):
                    target_pos = task[agent.J]
                    agent.position += (target_pos - agent.position) * 0.1


            # Pygame visualization : agent position and color
            agent_positions = np.array([agent.position for agent in agent_list]) * scale + 20
            task_positions = task * scale + 20

            for pos in task_positions:
                pygame.draw.circle(screen, RED, pos.astype(int), 5)

            for pos in agent_positions:
                pygame.draw.circle(screen, BLUE, pos.astype(int)[0], 5)

            # Draw agent IDs next to agents
            for i, pos in enumerate(agent_positions):
                text = font.render(str(agent_list[i].id), True, BLUE)
                screen.blit(text, (pos[0][0] + 10, pos[0][1] + 10))

            for i in range(agent_num):
                for j in range(i + 1, agent_num):
                    if G[i, j] == 1:
                        pygame.draw.line(screen, BLACK, agent_positions[i][0], agent_positions[j][0], 1)

            draw_legend(screen)

            pygame.display.flip()
            clock.tick(30)

            #next iteration
            t += 1
            #end condition
            # if sum(converged_list) == agent_num is a finish condition as well
            if t > max_t :
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.image.save(screen, "CBAA_SIM_GUI.jpg")
                        pygame.quit()
                pygame.image.save(screen, "CBAA_SIM_GUI.jpg")
                running = False

        pygame.quit()

