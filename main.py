import networkx as nx
import matplotlib.pyplot as plt

def create_grid_2d(dim1, dim2, isperioidic, m):
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
        C = Z
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

    #---computing shortest pahts in C---
    print(list(C.nodes))
    P = []
    agents = {}
    #start with a set of |CW agents in v_(0,0)
    nr_of_agents = C.number_of_nodes()

    for i in list(C.nodes):
        print(nx.shortest_path(C, source = (0, 0), target = i))
        P.append(nx.shortest_path(C, source = (0, 0), target = i))
    print("P is :")
    print(P)
    for i in range(nr_of_agents):
        agents[i] = (0, 0)
    print(agents)

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
        # move p_i agents to w_i
        for i in range(len(edges_of_v_in_P)):
            print(agents)
            for j in range(p[i]):
                list_of_agents_on_v = []
                for key in agents:
                    if agents[key] == v:
                        list_of_agents_on_v.append(key)
                print(list_of_agents_on_v)
                print(v)
                agents[j+1] = edges_of_v_in_P[i][1]

        print(agents)
        print("iteration is over")

create_grid_2d(5, 5, False, 1)