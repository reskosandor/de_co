import networkx as nx
import matplotlib.pyplot as plt
import mesh_2d

def create_grid_3d(dimensions, isperioidic, m):
    print(dimensions)
    dim1 = dimensions[2]
    dim2 = dimensions[1]
    dim3 = dimensions[0]
    print(dim1)
    print(dim2)
    print(dim3)
    if dim2 < dim1 or dim3 < dim2:
        print("dimensions must be in monotonic increasing sequence")
        exit()

    if m == 0:
        print("m must be a positive integer")
        exit()

    if m > 3:
        print("m must not be greater than the dimension of the mesh")
        exit()
    Z = nx.grid_graph(dimensions, periodic=isperioidic)
    #print(nx.info(Z))
    #nx.draw(Z)
    #plt.show()
    #---initial_set_(2, m)_begins)---
    #---creating_C---
    print(list(Z.nodes))
    if (m == 1):
        C = Z.copy()
        for x in range(dim1):
            for y in range(dim2):
                for z in range(dim3):
                    print(str(x) + " " + str(y) + " " + str(z))
                    if z > 0:
                        C.remove_node((x, y, z))

    if (m == 2):
        C = Z.copy()
        for x in range(dim1):
            for y in range(dim2):
                for z in range(dim3):
                    print(str(x) + " " + str(y) + " " + str(z))
                    if y > 0 or z > 0:
                        C.remove_node((x, y, z))

    if (m == 3):
        C = nx.Graph()
        C.add_node((0, 0, 0))

    print(nx.info(C))
    print(list(C.nodes))
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
    mesh_2d.color_sync(Z, agents, previous_agents, color, m)
    print(color)
    #start with a set of |C| agents in v_(0,0)
    nr_of_agents = C.number_of_nodes()

    for i in list(C.nodes):
        print(nx.shortest_path(C, source = (0, 0, 0), target = i))
        P.append(nx.shortest_path(C, source = (0, 0, 0), target = i))
    print("P is :")
    print(P)
    for i in range(nr_of_agents):
        agents[i] = (0, 0, 0)
    print(agents)
    mesh_2d.color_sync(Z, agents, previous_agents, color, m)
    print(color)

    flipped_agents = {}
    print(len(agents.keys()))
    print(len(flipped_agents.keys()))
    # while exists v in C containing more than one agent
    while len(agents.keys()) != len(flipped_agents.keys()):
        # finding keys with duplicate values in dict
        # this is to choose a v, which has multiple agents on it
        for key, value in agents.items():
            if value not in flipped_agents:
                flipped_agents[value] = [key]
            else:
                flipped_agents[value].append(key)
        print("flipped_agents")
        print(flipped_agents)
        v = (0, 0, 0)
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
                agents[j + 1] = edges_of_v_in_P[i][1]

            mesh_2d.color_sync(Z, agents, previous_agents, color, m)
            print(color)
        print(agents)
        print("iteration is over")

    # algorithm MESH(3, m)
    # constructing canonical path
    if m == 3:
        # if forward_j is true, j indentation is forwards, if not, j indentation is backwards
        forward_i = False
        forward_j = False
        canonical_path = []
        print(len(canonical_path))
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
        print("canonical_path")
        print(canonical_path)
        print(len(canonical_path))
        # moving agent through canonical path
        for i in range(len(canonical_path) - 1):
            previous_agents = agents.copy()
            agents[0] = canonical_path[i + 1]
            print(agents[0])
            mesh_2d.color_sync(Z, agents, previous_agents, color, m)
            print(color)
    if m == 2:
        print(agents)
        forward_j = False
        for i in (range(dim3)):
            for j in range(dim2-1):
                previous_agents = agents.copy()
                forward_j = not forward_j
                #move one agent at a time, changing y coord
                for k in range(dim1):
                    (x, y, z) = agents[k]
                    if forward_j:
                        agents[k] = (x, y + 1, z)
                    else:
                        agents[k] = (x, y - 1, z)
                print(agents)
                mesh_2d.color_sync(Z, agents, previous_agents, color, m)
                print(color)
            previous_agents = agents.copy()
            #now all agents moved one in the y coord
            # move one agent at a time, increasing z coord
            # make sure to not move in the direction of z for the last time
            if i < (dim3 - 1):
                for k in range(dim1):
                    (x, y, z) = agents[k]
                    agents[k] = (x, y, z + 1)
                print(agents)
                mesh_2d.color_sync(Z, agents, previous_agents, color, m)
                print(color)
    if m == 1:
        print(agents)
        for i in range(dim3-1):
            previous_agents = agents.copy()
            for j in range(nr_of_agents):
                (x, y, z) = agents[j]
                agents[j] = (x, y, z+1)
            print(agents)
            mesh_2d.color_sync(Z, agents, previous_agents, color, m)
            print(color)
    print(list(Z.nodes))
    print(color)
    print(list(Z.nodes))
    print(color)

# grid_graph takes a list of dimensions as its input
# for some reason dimensions are in reverse order
# so the first item of the list will be the nth dimension
dimensions = [3, 2, 2]

create_grid_3d(dimensions, False, 1)