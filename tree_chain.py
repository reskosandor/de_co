import networkx as nx
import matplotlib.pyplot as plt
import functions
from random import uniform, randrange
import time
import sys
import math

previous_node = -1
starting_node = -1
nr_of_agents = -1
move_counter = 0
agents = {}
def tree(lr, m, p, nr_a = -1):
    start_time = time.time()
    global number_of_agents
    global previous_node
    global starting_node
    global nr_of_agents
    global move_counter
    global agents
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

    previous_agents = {}
    color = {}


    for nodes in T:
        color[nodes] = "grey"
    functions.color_sync(T, agents, previous_agents, color, m)
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

    def height(v, T):
        T_height = -1
        for node in T:
            if node != v:
                node_distance = len(nx.shortest_path(T, source = v, target= node))
                if T_height < node_distance:
                    T_height = node_distance
        return T_height

    def homebase_node(T):
        root = -3
        root_height = sys.maxsize
        min_of_max_dist = []
        #need to create a dummy list first
        for node in T:
            min_of_max_dist.append(-1)
        for node in T:
            min_of_max_dist[node] = height(node, T)
        for i in range(len(min_of_max_dist)):
            if min_of_max_dist[i] < root_height:
                root = i
                root_height = min_of_max_dist[i]
        return root, root_height


    def chain_agents_down(root, target):
        global move_counter
        global agents
        agents_0 = agents.copy()
        agents[0] = target
        agents = functions.sorted_dict(agents)
        move_counter = move_counter + 1
        for i in agents:
            if i > 0:
                agents[i] = agents_0[i-1]
                agents = functions.sorted_dict(agents)
                if agents[i] != agents_0[i]:
                    move_counter = move_counter + 1



    def chain_agents_up(root):
        global move_counter
        global agents
        agents_0 = agents.copy()
        ###last of the chain
        if agents_0[len(agents_0) - 1] != root:
            p_last = nx.shortest_path(T_original, agents_0[len(agents_0) - 1], root)
            agents[len(agents_0) - 1] = p_last[1]
            move_counter = move_counter + 1

        for i in agents:
            if i < len(agents) - 1:
                agents[i] = agents_0[i+1]
                if agents[i] != agents_0[i]:
                    move_counter = move_counter + 1

    def check_chain_gap(agents):
        for i in agents:
            if i > 0 and agents[i-1] == -1 and agents[i] == -1:
                print("Failure 1.:there is at least a two agent gap in the chain, decontamination failed")
                sys.exit()

    def solve_quadratic(a, b, c):
        D = b * b - 4 * a * c
        sqrt_D = math.sqrt(abs(D))
        return (-b + sqrt_D) / (2 * a), (-b - sqrt_D) / (2 * a)

    def agents_nr_by_chernoff(h, p):
        coeff_a = h - h * p
        coeff_b = -2 * math.log(p ** p) * (1 - p)
        coeff_c = 2 * math.log(p ** p) * (1 - p)

        delta_1, delta_2 = solve_quadratic(coeff_a, coeff_b, coeff_c)

        k_1 = -1.0
        k_2 = -1.0
        if 0 < delta_1 < 1:
            k_1 = h / ((1-delta_1) * (1-p))
        if 0 < delta_2 < 1:
            k_2 = h / ((1-delta_2) * (1-p))

        return max(math.ceil(k_1), math.ceil(k_2))




    def decontaminate(T, v, m, T_original, agents_when):
        global previous_node
        global number_of_agents
        global starting_node
        global nr_of_agents
        global move_counter
        global agents
        previous_agents = agents.copy()

        if previous_node == -1:
            print("agents entering the tree")
            for i in range(nr_of_agents):
                agents[i] = v
            number_of_agents = nr_of_agents
        else:
            chain_agents_down(starting_node, v)
            print("descending in the tree")

        functions.color_sync(T_original, agents, previous_agents, color, m)
        print("agents are " + str(agents))
        print("color is " + str(color))
        ##breakdown handling
        ### agent replacement
        previous_agents = agents.copy()
        agents_0 = agents.copy()
        terminated_agents = []
        #breakdown happens, instead of removing broken down agent, their position is -1 (which is practically removing from the tree)
        for i in agents_when:
            if agents_when[i] < move_counter:
                terminated_agents.append(i)
                agents[i] = -1
                print("agent " + str(i) + " has broken down")
        functions.color_sync(T_original, agents, previous_agents, color, m)
        # until we have handled all breakdowns
        while len(terminated_agents) > 0:
            print("agent replacement is needed")
            check_chain_gap(agents)
            terminated_agents.sort()
            previous_agents = agents.copy()
            #moving all agents in the chain above the furthest down breakdown by one
            root_counter = 0
            for i in agents:
                if i > terminated_agents[0] and i not in terminated_agents and root_counter < 1:
                    if agents[i] == starting_node:
                        root_counter = root_counter + 1
                    if agents_0[i-1] != -1:
                        agents[i] = agents_0[i-1]
                    elif agents_0[i] != -1:
                        path_to_v = nx.shortest_path(T_original, agents[i], v)
                        if agents[i] != path_to_v[0]:
                            agents[i] = path_to_v[1]
                    if agents[i] != agents_0[i]:
                        move_counter = move_counter + 1
            print("agents after position correction are " + str(agents))
            #now we eliminate the replaced agent and change the id-s
            corrected_ids = agents.copy()
            del corrected_ids[terminated_agents[0]] # we deleted the broken down
            correcting_ids = corrected_ids.copy()
            for i in correcting_ids.keys():
                if i > terminated_agents[0]:
                    value_of_change = corrected_ids[i]
                    del corrected_ids[i]
                    corrected_ids[i-1] = value_of_change #replace the missing one with the next one?
                    corrected_ids = functions.sorted_dict(corrected_ids)
                    #corrected_ids = functions.sort_dict(corrected_ids)


            agents = corrected_ids.copy() # ids and positions are correct
            print("agents after ID correction")
            if len(agents) < min_nr_of_agents:
                print("Failure 2.: too few agents remaining, cannot sustain a long enough chain")
                sys.exit()
            del agents_when[terminated_agents[0]] #delete the handled broken down from agents when
            terminated_agents.pop(0)  # delete the handled broken down agent
            if len(terminated_agents) != 0:
                for i in range(len(terminated_agents)):
                    if terminated_agents[i] > 0 and terminated_agents[i] -1 not in terminated_agents:
                        terminated_agents[i] = terminated_agents[i] - 1 #adjust the termination list id too
                functions.color_sync(T_original, agents, previous_agents, color, m)
            #adjust the agents_when too:
            agents_when_new = agents_when.copy()
            for i in agents_when.keys():
                if i != 0 and i-1 not in agents_when_new.keys():
                    corrected_ids = functions.sorted_dict(corrected_ids)
                    agents_when_new[i-1] = agents_when[i]
                    del agents_when_new[i]
            agents_when = agents_when_new.copy()
            previous_agents = agents.copy()
            agents_0 = agents.copy()
            # breakdown happens, instead of removing broken down agent, their position is -1 (which is practically removing from the tree)
            for i in agents_when:
                if agents_when[i] > move_counter and i not in terminated_agents:
                    terminated_agents.append(i)
                    agents[i] = -1
                    print("agent " + str(i) + " has broken down")
            functions.color_sync(T_original, agents, previous_agents, color, m)





        ## if there are more than one node which is equivalent with being in a leaf
        if len(list(T.nodes)) > 1:
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
                #####################################halftime
                agents_when = decontaminate(subtree(T, neighbor, v), neighbor, m, T_original, agents_when)
                #####################################halftime
                previous_agents = agents.copy()
                howmany = 0
                chain_agents_up(starting_node)
                functions.color_sync(T_original, agents, previous_agents, color, m)
                print("ascending in the tree")
                print("agents are " + str(agents))
                print("color is " + str(color))


                ##breakdown handling
                ### agent replacement
                previous_agents = agents.copy()
                agents_0 = agents.copy()
                terminated_agents = []
                # breakdown happens, instead of removing broken down agent, their position is -1 (which is practically removing from the tree)
                for i in agents_when:
                    if agents_when[i] < move_counter:
                        terminated_agents.append(i)
                        agents[i] = -1
                        print("agent " + str(i) + " has broken down")
                functions.color_sync(T_original, agents, previous_agents, color, m)
                # until we have handled all breakdowns
                while len(terminated_agents) > 0:
                    check_chain_gap(agents)
                    print("agent replacement is needed")
                    previous_agents = agents.copy()
                    terminated_agents.sort()
                    # moving all agents in the chain above the furthest down breakdown by one
                    root_counter = 0
                    for i in agents:
                        if i > terminated_agents[0] and i not in terminated_agents and root_counter < 1:
                            if agents[i] == starting_node:
                                root_counter = root_counter + 1
                            if agents_0[i - 1] != -1:
                                agents[i] = agents_0[i - 1]
                            elif agents_0[i] != -1:
                                path_to_v = nx.shortest_path(T_original, agents[i], v)
                                if agents[i] != path_to_v[0]:
                                    agents[i] = path_to_v[1]
                            if agents[i] != agents_0[i]:
                                move_counter = move_counter + 1
                    print("agents after position correction are " + str(agents))
                    # now we eliminate the replaced agent and change the id-s
                    corrected_ids = agents.copy()
                    del corrected_ids[terminated_agents[0]]  # we deleted the broken down
                    correcting_ids = corrected_ids.copy()
                    for i in correcting_ids.keys():
                        if i > terminated_agents[0]:
                            value_of_change = corrected_ids[i]
                            del corrected_ids[i]
                            corrected_ids[i - 1] = value_of_change  # replace the missing one with the next one
                            corrected_ids = functions.sorted_dict(corrected_ids)

                    agents = corrected_ids.copy()  # ids and positions are correct
                    print("agents after ID correction")
                    if len(agents) < min_nr_of_agents:
                        print("Failure 2.: too few agents remaining, cannot sustain a long enough chain")
                        sys.exit()
                    del agents_when[terminated_agents[0]]  # delete the handled broken down from agents when
                    terminated_agents.pop(0)  # delete the handled broken down agent
                    if len(terminated_agents) != 0:
                        for i in range(len(terminated_agents)):
                            if terminated_agents[i] > 0 and terminated_agents[i] -1 not in terminated_agents:
                                terminated_agents[i] = terminated_agents[i] - 1  # adjust the termination list id too
                        functions.color_sync(T_original, agents, previous_agents, color, m)
                    # adjust the agents_when too:
                    agents_when_new = agents_when.copy()
                    for i in agents_when.keys():
                        if i != 0 and i-1 not in agents_when_new.keys():
                            corrected_ids = functions.sorted_dict(corrected_ids)
                            agents_when_new[i - 1] = agents_when[i]
                            del agents_when_new[i]
                    agents_when = agents_when_new.copy()
                    previous_agents = agents.copy()
                    agents_0 = agents.copy()
                    # breakdown happens, instead of removing broken down agent, their position is -1 (which is practically removing from the tree)
                    for i in agents_when:
                        if agents_when[i] > move_counter and i not in terminated_agents:
                            terminated_agents.append(i)
                            agents[i] = -1
                            print("agent " + str(i) + " has broken down")
                    functions.color_sync(T_original, agents, previous_agents, color, m)

        else:
            print("we have reached a leaf")
        return agents_when
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
    min_a = [k for k, v in a_try.items() if v == minval]
    #getting nodes with minimum mu value, where they have the min alpha value
    min_mu_temp = mu_try.copy()
    min_mu = min_mu_temp.copy()
    for i in min_mu_temp:
        if i not in min_a:
            del min_mu[i]
    minimum_mu = []
    minval = min(min_mu.values())
    minimum_mu = [k for k, v in min_mu.items() if v == minval]


    def optimaltreedecontamination(T, m, T_original, p, max_move):
        global agents
        global starting_node
        global nr_of_agents
        agents_if = {}
        agents_when = {}

        for i in range(nr_of_agents):
            agents_if[i] = uniform(0, 1)
        print("agents_if is " + str(agents_if))



        for i in range(nr_of_agents):
            if agents_if[i] < p:
                agents_when[i] = randrange(1, max_move)

        print("agent_when is " + str(agents_when))
        agents_when = decontaminate(T, starting_node, m, T_original, agents_when)

    starting_node, min_nr_of_agents = homebase_node(T)
    chernoff = agents_nr_by_chernoff(min_nr_of_agents, p)
    if nr_a != -1:
        nr_of_agents = nr_a
    else:
        nr_of_agents = chernoff
    chernoff = agents_nr_by_chernoff(min_nr_of_agents, p)

    max_move = 0
    for i in range(nr_of_agents):
        max_move = max_move + 2*T_original.size() - 2* (i+1)
    max_move = max_move + min_nr_of_agents * (nr_of_agents - min_nr_of_agents)

    optimaltreedecontamination(T, m, T_original, p, max_move)


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
    print("total moves:  " + str(move_counter))
    end_time = time.time() - start_time
    return(number_of_agents, move_counted, end_time)

