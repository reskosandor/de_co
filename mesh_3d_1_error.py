import networkx as nx
import matplotlib.pyplot as plt
import functions
import time
import random
import math
from random import uniform, randrange

move_counter = 0
spare_alive = True

def create_grid_3d(dimensions, m):
    start_time = time.time()
    global move_counter
    global spare_alive
    move_counter = 0
    dim1 = dimensions[0]
    dim2 = dimensions[1]
    dim3 = dimensions[2]
    dims = [dimensions[2], dimensions[1], dimensions[0]]
    if dim2 < dim1 or dim3 < dim2 or dim3 < dim1:
        print("dimensions must be in monotonic increasing sequence")
        exit()

    if m == 0:
        print("m must be a positive integer")
        exit()

    if m > 3:
        print("m must not be greater than the dimension of the mesh")
        exit()
    Z = nx.grid_graph(dims, periodic=False)

    if (m == 1):
        C = Z.copy()
        for x in range(dim1):
            for y in range(dim2):
                for z in range(dim3):
                    if z > 0:
                        C.remove_node((x, y, z))

    if (m == 2):
        C = Z.copy()
        for x in range(dim1):
            for y in range(dim2):
                for z in range(dim3):
                    if y > 0 or z > 0:
                        C.remove_node((x, y, z))

    if (m == 3):
        C = nx.Graph()
        C.add_node((0, 0, 0))



    #---computing shortest paths in C---
    P = []
    agents = {}
    previous_agents = {}
    color = {}
    for nodes in Z:
        color[nodes] = "grey"
    functions.color_sync(Z, agents, previous_agents, color, m)
    print("color is " + str(color))
    nr_of_agents = C.number_of_nodes()

    # constructing P in a new way
    # v = (0, 0, 0) is in the bottom left corner
    # shortest path: move "up" as long as we need to, then move "right" as long as we need to
    for i in list(C.nodes):
        sublist = []
        (x, y, z) = i

        sublist.append((0, 0, 0))
        k = 0
        l = 0
        for j in range(x):
            k = k + 1
            sublist.append((k, 0, z))

        if y > 0:
            for j in range(y):
                l = l + 1
                sublist.append((x, l, z))

        P.append(sublist)
    print("Starting INITIAL-SET")
    for i in range(nr_of_agents):
        agents[i] = (0, 0, 0)
    print("agents are " + str(agents))
    spare_agent = (0, 0, 0)
    print("spare agent is " + str(spare_agent))
    functions.color_sync(Z, agents, previous_agents, color, m)
    print("color is " + str(color))
    t_init_moves, theoretical_nr_moves = theoretical_nr_of_moves(Z, C, m, dim1, dim2, dim3)
    agent_which = random.randint(0, nr_of_agents - 1)
    agent_when = random.randint(t_init_moves, theoretical_nr_moves)



    flipped_agents = {}
    values = list(agents.values())
    iterations = 0
    # while exists v in C containing more than one agent

    while len(values) != len(set(values)):
        sum_p = 0

        previous_values = values.copy()
        # finding keys with duplicate values in dict
        # this is to choose a v, which has multiple agents on it
        flipped_agents = {}
        for key, value in agents.items():
            if value not in flipped_agents:
                flipped_agents[value] = [key]
            else:
                flipped_agents[value].append(key)
        v = (0, 0, 0)
        biggest_v = -1
        for key in flipped_agents:
            value = flipped_agents[key]
            if len(value) > 1 and len(value) > biggest_v:
                v = key
                biggest_v = len(value)

        truest_list_of_agents_on_v = []
        for key in agents:
            if agents[key] == v:
                truest_list_of_agents_on_v.append(key)
        # let (v,w_i),...,(v,w_r) be the edges from v included in a path in P
        edges_of_v_in_P = []
        for i in P:
            for j in i:
                if j == v and j != i[-1]:
                    if len(i) > 1:
                        edge = []
                        edge.append(v)
                        edge.append(i[i.index(j)+1])
                        edges_of_v_in_P.append(edge)
        no_duplicates = []
        for i in edges_of_v_in_P:
            if i not in no_duplicates:
                no_duplicates.append(i)
        edges_of_v_in_P = no_duplicates

        # let p_i be the number of paths in P containing (v,w_i)
        p = []
        for i in range(len(edges_of_v_in_P)):
            counter = 0
            for j in range(len(P)):
                if str(edges_of_v_in_P[i]).strip("[]") in str(P[j]):
                    counter = counter + 1
            p.append(counter)
        #checking how many agents do we want to send overall

        for i in range(len(p)):
            sum_p = sum_p + p[i]

        # for i = 1 to r

        for i in range(len(edges_of_v_in_P)):
            # move p_i agents to w_i
            true_list_of_agents_on_v = []
            for key in agents:
                if agents[key] == v:
                    true_list_of_agents_on_v.append(key)

            #list_of_agents_on_v is actually just the number we want to send to w_i
            list_of_agents_on_v = []
            for key in agents:
                if agents[key] == v and len(list_of_agents_on_v) < p[i]:
                    list_of_agents_on_v.append(key)
            nr_of_agents_on_v = len(list_of_agents_on_v)


            position_of_agents_on_v = []
            previous_agents = agents.copy()
            # in this for loop, for each k, we only move one agent at a time, k in range(nr_of_agents_on_v total agents
            for k in range(nr_of_agents_on_v):
                position_of_agents_on_v.append(edges_of_v_in_P[i][1])
                for key in agents:
                    if list_of_agents_on_v[k] == key and len(true_list_of_agents_on_v) > 1:
                        agents[key] = position_of_agents_on_v[k]
                        move_counter = move_counter + 1
            print("agents are " + str(agents))
            functions.color_sync(Z, agents, previous_agents, color, m)
            print("color is " + str(color))
        spare_agent = spare_agent_follow(spare_agent, nr_of_agents - 1, previous_agents)

        iterations = iterations + 1

        values = list(agents.values())
        if previous_values == values:
            print("loop stuck")
            exit()
        # check for something wrong?
        if sum_p + 1 != len(truest_list_of_agents_on_v):
            print("something horrible happened")
            exit()
    after_init = move_counter
    print("Starting MESH")
    # algorithm MESH(3, m)
    # constructing canonical path
    if m == 3:
        # if forward_j is true, j indentation is forwards, if not, j indentation is backwards
        forward_i = False
        forward_j = False
        canonical_path = []
        #print(len(canonical_path))
        for k in range(dim3):
            forward_i = not forward_i
            if forward_i:
                for i in range(dim1):
                    forward_j = not forward_j
                    if forward_j:
                        for j in range(dim2):
                            canonical_path.append((i, j, k))
                    else:
                        for j in range(dim2 - 1, -1, -1):
                            canonical_path.append((i, j, k))
            else:
                for i in range(dim1 - 1, -1, -1):
                    forward_j = not forward_j
                    if forward_j:
                        for j in range(dim2):
                            canonical_path.append((i, j, k))
                    else:
                        for j in range(dim2 - 1, -1, -1):
                            canonical_path.append((i, j, k))
        # moving agent through canonical path
        for i in range(len(canonical_path) - 1):
            previous_agents = agents.copy()
            agents[0] = canonical_path[i + 1]
            move_counter = move_counter + 1
            print("the agent is " + str(agents[0]))
            spare_agent = spare_agent_follow(spare_agent, nr_of_agents-1, previous_agents)
            spare_print(spare_agent, spare_alive)
            functions.color_sync(Z, agents, previous_agents, color, m)
            previous_agents = agents.copy()
            agents = agent_replacement(Z, agent_which, agent_when, agents, spare_agent)
            functions.color_sync(Z, agents, previous_agents, color, m)
            print("color is " + str(color))
    if m == 2:
        previous_agents = agents.copy()
        functions.color_sync(Z, agents, previous_agents, color, m)
        forward_j = False
        for i in (range(dim3)):
            forward_j = not forward_j
            for j in range(dim2-1):
                previous_agents = agents.copy()

                #move one agent at a time, changing y coord
                for k in range(dim1):
                    (x, y, z) = agents[k]
                    if forward_j:
                        agents[k] = (x, y + 1, z)
                        move_counter = move_counter + 1
                    else:
                        agents[k] = (x, y - 1, z)
                        move_counter = move_counter + 1
                print("agents are " + str(agents))
                spare_agent = spare_agent_follow(spare_agent, nr_of_agents-1, previous_agents)
                spare_print(spare_agent, spare_alive)
                functions.color_sync(Z, agents, previous_agents, color, m)
                previous_agents = agents.copy()
                agents = agent_replacement(Z, agent_which, agent_when, agents, spare_agent)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("color is " + str(color))
            previous_agents = agents.copy()
            #now all agents moved one in the y coord
            # move one agent at a time, increasing z coord
            # make sure to not move in the direction of z for the last time
            if i < (dim3 - 1):
                for k in range(dim1):
                    (x, y, z) = agents[k]
                    agents[k] = (x, y, z + 1)
                    move_counter = move_counter + 1
                print("agents are " + str(agents))
                spare_agent = spare_agent_follow(spare_agent, nr_of_agents-1, previous_agents)
                spare_print(spare_agent, spare_alive)
                functions.color_sync(Z, agents, previous_agents, color, m)
                previous_agents = agents.copy()
                agents = agent_replacement(Z, agent_which, agent_when, agents, spare_agent)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("color is " + str(agents))
    if m == 1:
        for i in range(dim3-1):
            previous_agents = agents.copy()
            for j in range(nr_of_agents):

                (x, y, z) = agents[j]
                agents[j] = (x, y, z+1)
                move_counter = move_counter + 1
            print("agents are " + str(agents))
            spare_agent = spare_agent_follow(spare_agent, nr_of_agents-1, previous_agents)
            spare_print(spare_agent, spare_alive)
            functions.color_sync(Z, agents, previous_agents, color, m)
            previous_agents = agents.copy()
            agents = agent_replacement(Z, agent_which, agent_when, agents, spare_agent)
            functions.color_sync(Z, agents, previous_agents, color, m)
            print("color is " + str(color))

    nr_of_black_nodes = 0
    for key in color:
        if color[key] == "black":
            nr_of_black_nodes = nr_of_black_nodes + 1
    for key in color:
        if color[key] == "grey":
            print("some nodes are grey, algorithm failed")
            exit()
    print("no grey nodes remain")
    print("moves after INITIAL-SET: " + str(after_init))
    print("total moves: " + str(move_counter))
    move_counted = move_counter
    move_counter = 0
    end_time = time.time() - start_time
    total_agents = nr_of_agents + 1
    return [total_agents, after_init, move_counted, end_time]

def theoretical_nr_of_moves(Z, C, m, dim1, dim2, dim3):
    c_moves = 0
    t_moves = 0
    if m == 3:
        i_moves = 0
        t_moves = 2 * Z.number_of_nodes() - 3
    if m == 2:
        i_moves = 0.5 * 1 * dim1 * dim1

        t_moves = i_moves + Z.number_of_nodes() + dim2 * dim3 - dim1 - 2

    if m == 1:
        i_moves = 1 * dim2 * dim2 * dim2

        t_moves = i_moves + (Z.number_of_nodes() - dim1*dim2 + dim3 -2)
    return math.ceil(i_moves), math.ceil(t_moves)

def spare_agent_follow(spare_agent, target_agent, previous_agents):
    global move_counter
    if spare_agent != previous_agents[target_agent] and spare_alive == True:
        spare_agent = previous_agents[target_agent]
        move_counter = move_counter + 1

    return spare_agent


def error_happened(agent_when):
    global move_counter
    if move_counter >= agent_when:
        return True
    else:
        return False

def agent_replacement(Z, agent_which, agent_when, agents, spare_agent):
    global move_counter
    global spare_alive


    if error_happened(agent_when) == True and spare_alive == True:
        print("agent " + str(agent_which) + " has broken down")
        old_agents = agents.copy()
        chain = nx.shortest_path(Z, agents[agent_which], agents[0])
        chain.append(spare_agent)
        agents[agent_which] = (-1, -1, -1)
        print("agents are " + str(agents))
        print("replacement of the agent is starting")
        print("chain of replacement is " + str(chain))

        #position correction
        for i in range(len(chain)):
            #print("i in chain is a " + str(type(i)))
            for j in agents:
                #print("the agents[j] in the chain is a " + str(type(agents[j])))
                if agents[j] == chain[i]:
                    agents[j] = chain[i-1]
                    move_counter = move_counter+1
        spare_agent = chain[len(chain) - 2]
        move_counter = move_counter + 1
        print("position of agents after correction " + str(agents))
        print("position of spare agent after correction " + str(spare_agent))
        #id correction
        iterator_agents = agents.copy()
        for i in range(len(chain) - 2):
            a = functions.key_by_value(chain[i], iterator_agents)
            b = functions.key_by_value(chain[i], old_agents)
            del iterator_agents[b]
            iterator_agents[b] = chain[i]
            iterator_agents = functions.sorted_dict(iterator_agents)

        iterator_agents[0] = spare_agent
        agents = iterator_agents.copy()

        spare_alive = False
        print("agents after id correction " + str(agents))
    return agents

def spare_print(spare_agent, spare_alive):
    if spare_alive == True:
        print("spare agent is " + str(spare_agent))