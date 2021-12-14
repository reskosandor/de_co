import networkx as nx
import matplotlib.pyplot as plt
import functions
import random
import time
import math

previous_node = -1
move_counter = 0
error_happened = False
def tree(lr, m):
    start_time = time.time()
    global move_counter
    global number_of_agents
    global previous_node
    global error_happened
    previous_node = -1
    T = nx.algorithms.tree.coding.from_prufer_sequence(lr)
    T_degree = T.degree()


    def subtree(T, v_1, v):
        T_v1_v = T.copy()
        T_v1_v.remove_edge(v_1, v)
        for node in list(T_v1_v):
            if node in nx.algorithms.dag.descendants(T_v1_v, v_1) or node == v_1:
                pass
            else:
                T_v1_v.remove_node(node)
        return T_v1_v

    def neighbors_of_v(T, v):
        return [n for n in T.neighbors(v)]

    def degree(T, v):
        for x, y in T.edges():
            if x == v:
                return y
            elif y == v:
                return x

    def branch3(base, dict):
        condition = True
        for key in dict:
            if key != base:
                if dict[base] <= dict[key]:
                    condition = False
        return condition

    def branch4(base, dict):
        condition = True
        for key in dict:
            if key != base:
                if dict[base] < dict[key]:
                    condition = False
        return condition

    def alpha(v, T, m):
        if T.degree[v] > 0:
            v_1 = neighbors_of_v(T, v)[0]
            alpha_of_neighbors = {}
            neigh_list = neighbors_of_v(T, v)
            for node in neigh_list:
                alpha_of_neighbors[node] = alpha(node, subtree(T, node, v), m)
            max_key = max(alpha_of_neighbors, key=alpha_of_neighbors.get)
        if T.degree[v] == 0:
            return 1
        elif 0 < T.degree[v] <= m:
            value = alpha_of_neighbors[max_key]
            return value
        elif T.degree[v] > m and branch3(max_key, alpha_of_neighbors):
            value = alpha_of_neighbors[max_key]
            return value
        elif T.degree[v] > m and branch4(max_key, alpha_of_neighbors):
            value = alpha_of_neighbors[max_key] + 1
            return value

    agents = {}
    previous_agents = {}
    backup_agents = {}
    previous_backup_agents = {}
    color = {}

    for nodes in T:
        color[nodes] = "grey"
    functions.color_sync_with_error(T, agents, previous_agents, color, m, backup_agents, previous_backup_agents)
    print("color is " + str(color))
    T_original = T.copy()

    def mu(v, T, m):

        neigh_list = neighbors_of_v(T, v)
        if T.degree[v] == 0:
            return 0
        else:
            ret = 0
            for node in neigh_list:
                ret = ret + mu(node, subtree(T, node, v), m) + 2 * alpha(node, subtree(T, node, v), m)
            return ret


    def decontaminate(T, v, m, T_original, number_of_moves, original_root, error_point):
        global previous_node
        global move_counter
        global number_of_agents
        global error_happened
        previous_agents = agents.copy()
        previous_backup_agents = backup_agents.copy()
        nr_of_agents = alpha(v, T, m)

        for i in range(nr_of_agents):
            if previous_node == -1:
                agents[i] = v
                backup_agents[i] = v
                number_of_agents = nr_of_agents
            else:
                if agents[i] == previous_node:
                    agents[i] = v
                    move_counter = move_counter + 1

        if previous_node == -1:
            print("agents are entering the tree")
        else:
            print("descending in the tree")

        #creating backup agents and moving them. if they became active, their value in backup_agents will be -1
        for i in range(len(backup_agents)):
            if previous_node == -1:
                backup_agents[i] = v
            elif backup_agents[i] != -1 and error_happened == False and backup_agents[i] != previous_agents[i]:
                backup_agents[i] = previous_agents[i]
                move_counter = move_counter + 1

        functions.color_sync_with_error(T_original, agents, previous_agents, color, m, backup_agents, previous_backup_agents)
        print("agents are " + str(agents))
        spare_print(backup_agents)
        print("color is " + str(color))

        #doing the error check
        if move_counter >= error_point and error_happened == False:
            #updating previous agent positions
            previous_agents = agents.copy()
            previous_backup_agents = backup_agents.copy()
            erroneous_agent = random.randint(0, len(agents) - 1)
            print("agent " + str(erroneous_agent) + " broke down")
            #eliminating the error agent
            agents[erroneous_agent] = -1
            print("agents are " + str(agents))
            spare_print(backup_agents)
            #color sync
            functions.color_sync_with_error(T_original, agents, previous_agents, color, m, backup_agents,
                                            previous_backup_agents)
            #moving the single backup agent
            backup_agents[erroneous_agent] = previous_agents[erroneous_agent]
            move_counter = move_counter + 1
            print("agents after correcting position: " + str(agents))
            print("spare agents after correcting position: " + str(backup_agents))
            #color sync
            functions.color_sync_with_error(T_original, agents, previous_agents, color, m, backup_agents,
                                            previous_backup_agents)
            #updating the previous agent positions
            previous_agents = agents.copy()
            previous_backup_agents = backup_agents.copy()
            #the single backup agent becomes an active agent
            agents[erroneous_agent] = backup_agents[erroneous_agent]
            backup_agents[erroneous_agent] = -1
            print("agents after correcting IDs: " + str(agents))
            print("spare agents after correcting IDs: " + str(backup_agents))

            #color sync
            functions.color_sync_with_error(T_original, agents, previous_agents, color, m, backup_agents,
                                            previous_backup_agents)
            error_happened = True


        if T.degree(v) != 0:
            v_neighbours = neighbors_of_v(T, v)
            a = {}
            #calculating alpha for all neighbours
            for node in v_neighbours:
                a[node] = (alpha(node, T, m))
            ordered_v_neighbours = []
            for key in a:
                max_key = max(a, key=a.get)
                ordered_v_neighbours.append(max_key)
                a[max_key] = -1
                if len(ordered_v_neighbours) == len(a):
                    break
            for neighbor in reversed(ordered_v_neighbours):
                previous_node = v
                decontaminate(subtree(T, neighbor, v), neighbor, m, T_original, number_of_moves, original_root, error_point)
                #this is the moving back part
                previous_agents = agents.copy()
                previous_backup_agents = backup_agents.copy()
                howmany = 0
                for i in agents:
                    if agents[i] == neighbor:
                        agents[i] = v
                        howmany = howmany+1
                        move_counter = move_counter + 1
                #moving the backup agents one step back on the shortest route to the root
                for i in backup_agents:
                    if backup_agents[i] != -1 and backup_agents[i] != original_root and error_happened == False and backup_agents[i] != previous_agents[i]:
                        shortest_path_to_root = nx.shortest_path(T_original, backup_agents[i], original_root)
                        backup_agents[i] = shortest_path_to_root[1]
                        move_counter = move_counter + 1



                functions.color_sync_with_error(T_original, agents, previous_agents, color, m, backup_agents, previous_backup_agents)
                print("agents are " + str(agents))
                spare_print(backup_agents)
                print("color is " + str(color))

                # doing the error check
                if move_counter >= error_point and error_happened == False:
                    previous_agents = agents.copy()
                    previous_backup_agents = backup_agents.copy()
                    erroneous_agent = random.randint(0, len(agents) - 1)
                    print("agent " + str(erroneous_agent) + " broke down")
                    agents[erroneous_agent] = -1
                    print("agents are " + str(agents))
                    spare_print(backup_agents)
                    functions.color_sync_with_error(T_original, agents, previous_agents, color, m, backup_agents,
                                                    previous_backup_agents)
                    backup_agents[erroneous_agent] = previous_agents[erroneous_agent]
                    move_counter = move_counter + 1
                    print("agents after correcting position: " + str(agents))
                    print("spare agents after correcting position: " + str(backup_agents))
                    functions.color_sync_with_error(T_original, agents, previous_agents, color, m, backup_agents,
                                                    previous_backup_agents)
                    previous_agents = agents.copy()
                    previous_backup_agents = backup_agents.copy()
                    agents[erroneous_agent] = backup_agents[erroneous_agent]
                    backup_agents[erroneous_agent] = -1
                    print("agents after correcting IDs: " + str(agents))
                    print("spare agents after correcting IDs: " + str(backup_agents))
                    functions.color_sync_with_error(T_original, agents, previous_agents, color, m, backup_agents,
                                                    previous_backup_agents)
                    error_happened = True

        else:
            print("we have reached a leaf")
    #print(mu(3, T, m))
    #decontaminate(T, 3, m, T_original)

    a_try = {}
    for node in list(T):
        a_try[node] = (alpha(node, T, m))

    mu_try = {}
    for node in list(T):
        mu_try[node] = (mu(node, T, m))
    #getting nodes with minimum alpha value
    min_a = []
    minval = min(a_try.values())
    min_a = [k for k, v in a_try.items() if v==minval]
    #getting nodes with minimum mu value, where they have the min alpha value
    min_mu_temp = mu_try.copy()
    min_mu = min_mu_temp.copy()
    for i in min_mu_temp:
        if i not in min_a:
            del min_mu[i]
    minimum_mu = []
    minval = min(min_mu.values())
    minimum_mu = [k for k, v in min_mu.items() if v==minval]

    def optimaltreedecontamination(T, m, T_original):
        starting_node = minimum_mu[0]
        number_of_moves = minval
        error_point = random.randint(1 , minval)
        decontaminate(T, starting_node, m, T_original, number_of_moves, starting_node, error_point)

    optimaltreedecontamination(T, m, T_original)


    nr_of_black_nodes = 0
    for key in color:
        if color[key] == "black":
            nr_of_black_nodes = nr_of_black_nodes + 1
    for key in color:
        if color[key] == "grey":
            print("some nodes are grey, algorithm failed")
            exit()
    print("no grey nodes remain")
    move_counted = move_counter
    print("total moves: " + str(move_counted))
    move_counter = 0
    end_time = time.time() - start_time
    return(number_of_agents*2, move_counted, end_time)

def spare_print(backup_agents):
    global error_happened
    if error_happened == False:
        print("spare agents are " + str(backup_agents))