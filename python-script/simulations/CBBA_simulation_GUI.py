import pygame
import numpy as np
from utils.Task import Task
from utils.network_topology import Network_Topology
from algorithms.CBBA_algorithm import CBBA_agent


class CBBA:
    def __init__(self):
        print("[+] CBBA Initialized...")

    def simulation(self, task_num, agent_num, max_t, topology):
        """
        Runs the simulation of the CBBA algorithm with the specified parameters.

        Parameters
        ----------
        task_num : int
            The number of tasks in the simulation.
        agent_num : int
            The number of agents in the simulation.
        max_t : int
            The maximum number of iterations.
        save_gif : bool
            If True, save the simulation as a GIF.
        topology : int
            The network topology to use (1: star, 2: fully connected, 3: ring, 4: mesh, 5: random).

        Returns
        -------
        None
        """
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

        # SIMULATION PARAMETERS
        task = Task(task_num).get_position()
        agent_list = [CBBA_agent(id=i, vel=1, task_num=task_num, agent_num=agent_num, L_t=task.shape[0]) for i in range(agent_num)]
        t = 0  # Iteration number
        max_t = max_t
        visited_tasks = [-1] * task_num  # List to keep track of which agent visited which task

        # Initialize pygame
        pygame.init()
        screen_size = 600
        screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption('CBBA Simulation')

        # Colors
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLACK = (0, 0, 0)
        BLUE = (0, 0, 255)
        GRAY = (128, 128, 128)


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
                ("Agent Path", GREEN),
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
            # Phase 1: Auction process
            print("\t Phase 1 : Auction")
            for agent in agent_list:
                agent.build_bundle(task)

            # Communication stage
            print("Communicating...")
            # Send winning bid list to neighbors (depend on env)
            message_pool = [agent.send_message() for agent in agent_list]

            for agent_id, agent in enumerate(agent_list):
                # Receive winning bid list from neighbors
                g = G[agent_id]
                connected = list(np.where(g == 1)[0])
                connected.remove(agent_id)

                Y = {neighbor_id: message_pool[neighbor_id] for neighbor_id in connected} if connected else None

                agent.receive_message(Y)

            # Phase 2 : Consensus process
            print("\t Phase 2 : Consensus")
            neighboring_msg = [agent.send_message() for agent in agent_list]

            for agent_id, agent in enumerate(agent_list):
                g = G[agent_id]  # connections of the agent that is being visited
                # find connected agents by the network
                connected = list(np.where(g == 1)[0])
                connected.remove(agent_id)  # agent has been visited

                Y = {neighbor_id: neighboring_msg[neighbor_id] for neighbor_id in connected} if connected else None

                # update the local information and task allocation
                if Y is not None:
                    converged = agent.update_task()
                    converged_list.append(converged)

            for agent in agent_list:
                if agent.p:
                    target_pos = task[agent.p[0]]
                    direction = target_pos - agent.position.squeeze()
                    distance = np.linalg.norm(direction)
                    if distance > 0.01:
                        direction /= distance
                        agent.position += direction * 0.01
                    else:
                        visited_tasks[agent.p[0]] = agent.id  # Mark task as visited by this agent
                        agent.p.pop(0)  # Remove the task from the agent's path

            # Pygame visualization : agent position and color
            agent_positions = np.array([agent.position for agent in agent_list]).reshape((agent_num, 2)) * scale + 20
            task_positions = task * scale + 20

            for pos in task_positions:
                pygame.draw.circle(screen, RED, pos.astype(int), 5)

            for pos in agent_positions:
                pygame.draw.circle(screen, BLUE, pos.astype(int), 5)

            # Draw agent IDs next to agents
            for i, pos in enumerate(agent_positions):
                text = font.render(str(agent_list[i].id), True, BLUE)
                screen.blit(text, (pos[0] + 10, pos[1] + 10))

            # Draw dotted lines for agent paths
            for agent in agent_list:
                if len(agent.p) > 0:
                    path_positions = [agent.position.squeeze()] + [task[i] for i in agent.p]
                    path_positions = np.array(path_positions) * scale + 20
                    for i in range(len(path_positions) - 1):
                        start_pos = path_positions[i]
                        end_pos = path_positions[i + 1]
                        pygame.draw.line(screen, GREEN, start_pos.astype(int), end_pos.astype(int), 1)

            for i in range(agent_num):
                for j in range(i + 1, agent_num):
                    if G[i, j] == 1:
                        pygame.draw.line(screen, BLACK, agent_positions[i].astype(int), agent_positions[j].astype(int), 1)

            for idx, agent_id in enumerate(visited_tasks):
                if agent_id != -1:
                    pos = task_positions[idx]
                    text = font.render(str(agent_id), True, GREEN)
                    screen.blit(text, (pos[0] + 10, pos[1] - 10))

            draw_legend(screen)

            pygame.display.flip()
            clock.tick(30)

            # next iteration
            t += 1
            # end condition
            if t > max_t or all(id != -1 for id in visited_tasks):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.image.save(screen, "CBBA_SIM_GUI.jpg")
                        pygame.quit()
                pygame.image.save(screen, "CBBA_SIM_GUI.jpg")
                running = False

        pygame.quit()


