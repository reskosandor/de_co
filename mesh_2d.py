import networkx as nx
import matplotlib.pyplot as plt

move_counter = 0

def create_grid_2d(dim1, dim2, isperioidic, m):
    global move_counter
    if dim2 < dim1:
        print("dimensions must be in monotonic increasing sequence")
        exit()

    if m == 0:
        print("m must be a positive integer")
        exit()

    if m > 2:
        print("m must not be greater than the dimension of the mesh")
        exit()
    Z = nx.grid_2d_graph(dim1, dim2, periodic=isperioidic, create_using=None)
    #print(nx.info(Z))
    #nx.draw(Z)
    #plt.show()
    #---initial_set_(2, m)_begins)---
    #---creating_C---
    print(list(Z.nodes))
    if (m == 1):
        C = Z.copy()
        for x in range(dim1):
            for y in range(dim2-1):
                print(str(x) + " " + str(y))
                C.remove_node((x, y+1))

    if (m == 2):
        C = nx.Graph()
        C.add_node((0, 0))

    #print(nx.info(C))
    #nx.draw(C)
    #plt.show()

    #---computing shortest paths in C---
    print(list(C.nodes))
    P = []
    agents = {}
    previous_agents = {}
    color = {}
    for nodes in Z:
        color[nodes] = "grey"
    color_sync(Z, agents, previous_agents, color, m)
    print(color)
    #start with a set of |C| agents in v_(0,0)
    nr_of_agents = C.number_of_nodes()

    for i in list(C.nodes):
        print(nx.shortest_path(C, source = (0, 0), target = i))
        P.append(nx.shortest_path(C, source = (0, 0), target = i))
    print("P is :")
    print(P)
    for i in range(nr_of_agents):
        agents[i] = (0, 0)
    print(agents)
    color_sync(Z, agents, previous_agents, color, m)
    print(color)

    flipped_agents = {}
    print(len(agents.keys()))
    print(len(flipped_agents.keys()))
    #while exists v in C containing more than one agent
    while len(agents.keys()) != len(flipped_agents.keys()):
        #finding keys with duplicate values in dict
        #this is to choose a v, which has multiple agents on it
        for key, value in agents.items():
            if value not in flipped_agents:
                flipped_agents[value] = [key]
            else:
                flipped_agents[value].append(key)
        print("flipped_agents")
        print(flipped_agents)
        v = (0, 0)
        for key in flipped_agents:
            value = flipped_agents[key]
            if len(value) > 1:
                v = key
        # let (v,w_i),...,(v,w_r) be the edges from v included in a path in P
        edges_of_v_in_P = []
        for i in P:
            print("i is:")
            print(i)
            print("len(i) is: ")
            print(len(i))
            for j in i:
                print("j is:")
                print(j)
                print("len(j) is:")
                print(len(j))
                if j == v and j != i[-1]:
                    print("(i.index(j) is")
                    print((i.index(j)))
                    print("i[i.index(j)] is")
                    print(i[i.index(j)])
                    if len(i) > 1:
                        edge = []
                        edge.append(v)
                        print("i indices")
                        print(i)
                        print(len(i))
                        print(i[i.index(j)])
                        edge.append(i[i.index(j)+1])
                        edges_of_v_in_P.append(edge)
        print(edges_of_v_in_P)
        print(len(edges_of_v_in_P))
        # let p_i be the number of paths in P containing (v,w_i)
        p = []
        for i in range(len(edges_of_v_in_P)):
            counter = 0
            for j in range(len(P)):
                if str(edges_of_v_in_P[i]).strip("[]") in str(P[j]):
                    print(str(edges_of_v_in_P[i]))
                    counter = counter + 1
            p.append(counter)
        print("p is:")
        print(p)
        # for i = 1 to r
        for i in range(len(edges_of_v_in_P)):
            print(agents)
            # move p_i agents to w_i
            previous_agents = agents.copy()
            for j in range(p[i]):
                list_of_agents_on_v = []
                for key in agents:
                    if agents[key] == v:
                        list_of_agents_on_v.append(key)
                print(list_of_agents_on_v)
                print(v)
                agents[j+1] = edges_of_v_in_P[i][1]
                move_counter = move_counter + 1


            color_sync(Z, agents, previous_agents, color, m)
            print(color)
        print(agents)
        print("iteration is over")
        after_init = move_counter
    #algorithm MESH(2, m)
    #constructing canonical path
    if m == 2:
        canonical_path = []
        print(len(canonical_path))
        for i in range(dim1):
            if (i % 2) == 0:
                for j in range(dim2):
                    canonical_path.append((i, j))
            else:
                for j in range(dim2-1, -1, -1):
                    canonical_path.append((i, j))
        print("canonical_path")
        print(canonical_path)
        print(len(canonical_path))
    #moving agent through canonical path
        for i in range(len(canonical_path)-1):
            previous_agents = agents.copy()
            agents[0] = canonical_path[i+1]
            move_counter = move_counter + 1
            print(agents[0])
            color_sync(Z, agents, previous_agents, color, m)
            print(color)
    if m < 2:
        print(agents)
        for i in range(dim2-1):
            previous_agents = agents.copy()
            for j in range(dim1):
                (x, y) = agents[j]
                agents[j] = (x, y+1)
                move_counter = move_counter + 1
            print(agents)
            color_sync(Z, agents, previous_agents, color, m)
            print(color)
    print(list(Z.nodes))
    print(color)
    nr_of_black_nodes = 0
    for key in color:
        if color[key] == "black":
            # print(key)
            nr_of_black_nodes = nr_of_black_nodes + 1
    print(nr_of_black_nodes)
    # print("nr of iterations")
    # print(iterations)
    for key in color:
        if color[key] == "grey":
            print("some nodes are grey, algorithm failed")
            exit()
    print("no grey nodes remain")
    print("after_init is " + str(after_init))
    print("move_counter is " + str(move_counter))
def color_sync(graph, agents, previous_agents, color, m):
    for key in color:
        for i in agents:
            if key == agents[i]:
                color[key] = "black"


    for key in color:
        if key in previous_agents.values() and key not in agents.values():
            color[key] = "white"

    if color[key] == "white":
        neighbours = [j for j in graph[key]]
        counter = 0
        for k in range(len(neighbours)):
            if color[(neighbours[k])] == "grey":
                counter = counter + 1
            if m <= counter:
                color[key] = "grey"
            elif counter < m:
                color[key] = "white"




create_grid_2d(10, 10, False, 1)