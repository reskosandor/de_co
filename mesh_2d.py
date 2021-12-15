import networkx as nx
import functions
import time

move_counter = 0

def create_grid_2d(dim1, dim2, m):
    start_time = time.time()
    global move_counter
    move_counter = 0
    if dim2 < dim1:
        print("dimensions must be in monotonic increasing sequence")
        exit()

    if m == 0:
        print("m must be a positive integer")
        exit()

    if m > 2:
        print("m must not be greater than the dimension of the mesh")
        exit()
    Z = nx.grid_2d_graph(dim1, dim2, periodic=False, create_using=None)
    #print(nx.info(Z))
    #nx.draw(Z)
    #plt.show()
    #---initial_set_(2, m)_begins)---
    #---creating_C---
    if (m == 1):
        C = Z.copy()
        for x in range(dim1):
            for y in range(dim2-1):
                C.remove_node((x, y+1))

    if (m == 2):
        C = nx.Graph()
        C.add_node((0, 0))


    #---computing shortest paths in C---
    P = []
    agents = {}
    previous_agents = {}
    color = {}
    for nodes in Z:
        color[nodes] = "grey"
    functions.color_sync(Z, agents, previous_agents, color, m)
    print("color is " + str(color))
    #start with a set of |C| agents in v_(0,0)
    nr_of_agents = C.number_of_nodes()

    for i in list(C.nodes):
        P.append(nx.shortest_path(C, source = (0, 0), target = i))
    print("Starting INITIAL-SET")
    for i in range(nr_of_agents):
        agents[i] = (0, 0)
    print("agents are " + str(agents))
    functions.color_sync(Z, agents, previous_agents, color, m)
    print("color is " + str(color))

    flipped_agents = {}
    #while exists v in C containing more than one agent
    while len(agents.keys()) != len(flipped_agents.keys()):
        #finding keys with duplicate values in dict
        #this is to choose a v, which has multiple agents on it
        for key, value in agents.items():
            if value not in flipped_agents:
                flipped_agents[value] = [key]
            else:
                flipped_agents[value].append(key)
        v = (0, 0)
        for key in flipped_agents:
            value = flipped_agents[key]
            if len(value) > 1:
                v = key
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
        # let p_i be the number of paths in P containing (v,w_i)
        p = []
        for i in range(len(edges_of_v_in_P)):
            counter = 0
            for j in range(len(P)):
                if str(edges_of_v_in_P[i]).strip("[]") in str(P[j]):
                    counter = counter + 1
            p.append(counter)
        # for i = 1 to r
        for i in range(len(edges_of_v_in_P)):

            # move p_i agents to w_i
            previous_agents = agents.copy()
            for j in range(p[i]):
                list_of_agents_on_v = []
                for key in agents:
                    if agents[key] == v:
                        list_of_agents_on_v.append(key)
                if agents[j+1] != edges_of_v_in_P[i][1]:
                    agents[j+1] = edges_of_v_in_P[i][1]
                    move_counter = move_counter + 1


            functions.color_sync(Z, agents, previous_agents, color, m)

        print("agents are " + str(agents))
        print("color is " + str(color))
        after_init = move_counter
    #algorithm MESH(2, m)
    #constructing canonical path
    print("Starting MESH")
    if m == 2:
        canonical_path = []

        for i in range(dim1):
            if (i % 2) == 0:
                for j in range(dim2):
                    canonical_path.append((i, j))
            else:
                for j in range(dim2-1, -1, -1):
                    canonical_path.append((i, j))

    #moving agent through canonical path
        for i in range(len(canonical_path)-1):
            previous_agents = agents.copy()
            agents[0] = canonical_path[i+1]
            move_counter = move_counter + 1
            print("the agent is " + str(agents[0]))
            functions.color_sync(Z, agents, previous_agents, color, m)
            print("color is " + str(color))
    if m < 2:

        for i in range(dim2-1):
            previous_agents = agents.copy()
            for j in range(dim1):
                (x, y) = agents[j]
                agents[j] = (x, y+1)
                move_counter = move_counter + 1
            print("agents are " + str(agents))
            functions.color_sync(Z, agents, previous_agents, color, m)
            print("color is " + str(color))
    nr_of_black_nodes = 0
    for key in color:
        if color[key] == "black":
            # print(key)
            nr_of_black_nodes = nr_of_black_nodes + 1
    # print("nr of iterations")
    # print(iterations)
    for key in color:
        if color[key] == "grey":
            print("some nodes are grey, algorithm failed")
            exit()
    print("no grey nodes remain")
    print("number of moves after INITIAL-SET is " + str(after_init))
    print("total number of moves is " + str(move_counter))
    move_counted = move_counter
    move_counter = 0
    end_time = time.time() - start_time
    return [nr_of_agents, after_init, move_counted, end_time]


