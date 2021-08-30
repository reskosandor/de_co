import networkx as nx
import matplotlib.pyplot as plt
import mesh_2d

def create_grid_2d(dim1, dim2, isperioidic, m):

    dims = [dim1, dim2]
    y_global = 1

    if dim2 < dim1:
        print("dimensions must be in monotonic increasing sequence")
        exit()

    if m == 0:
        print("m must be a positive integer")
        exit()

    if m > 2:
        print("algorithm is not needed, decontamination is trivial")
        exit()

    Z = nx.grid_2d_graph(dim1, dim2, periodic=isperioidic, create_using=None)

    print(nx.info(Z))
    #nx.draw(Z)
    #plt.show()
    # ---initial_set_(2, m)_begins)---
    # ---creating_C---
    print(list(Z.nodes))
    C = Z.copy()
    if (m == 1):
        for i in list(C.nodes):
            (x, y) = i
            if y > 1:
                C.remove_node((x, y))

    if (m == 2):
        for i in list(C.nodes):
            (x, y) = i
            if y > 1 or x > 1:
                C.remove_node((x, y))

    if (m == 3):
        for i in list(C.nodes):
            (x, y) = i
            if y > 0 or x > 1:
                C.remove_node((x, y))

    if (m > 3):
        C = nx.Graph()
        C.add_node((0, 0))


    print("list of C nodes")
    # print(nx.info(C))
    # nx.draw(C)
    # plt.show()
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

    # constructing P in a new way
    # v = (0, 0, 0) is in the bottom left corner
    # shortest path: move "up" as long as we need to, then move "right" as long as we need to
    for i in list(C.nodes):
        #print(nx.shortest_path(C, source = (0, 0, 0), target = i))
        #P.append(nx.shortest_path(C, source = (0, 0, 0), target = i))
        sublist = []
        print("(x,y) is:")
        (x, y) = i
        print((x, y))

        sublist.append((0, 0))
        k = 0
        l = 0
        for j in range(x):
            k = k + 1
            sublist.append((k, 0))

        if y > 0:
            for j in range(y):
                l = l + 1
                sublist.append((x, l))

        print(sublist)
        P.append(sublist)
    print("P is :")
    print(P)

    for i in range(nr_of_agents):
        agents[i] = (0, 0)
    #print(agents)
    mesh_2d.color_sync(Z, agents, previous_agents, color, m)
    #print(color)

    flipped_agents = {}
    #print(len(agents.keys()))
    #print(len(flipped_agents.keys()))

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
        #print("agents")
        #print(agents)
        #print("flipped_agents")
        #print(flipped_agents)
        v = (0, 0)
        biggest_v = -1
        print("flipped_agents")
        print(flipped_agents)
        for key in flipped_agents:
            value = flipped_agents[key]
            if len(value) > 1 and len(value) > biggest_v:
                v = key
                biggest_v = len(value)

        print("v is:")
        print(v)
        truest_list_of_agents_on_v = []
        for key in agents:
            if agents[key] == v:
                truest_list_of_agents_on_v.append(key)
        print("truest")
        print(truest_list_of_agents_on_v)
        print(len(truest_list_of_agents_on_v))
        # let (v,w_i),...,(v,w_r) be the edges from v included in a path in P
        edges_of_v_in_P = []
        for i in P:
            #print("i is:")
            #print(i)
            #print("len(i) is: ")
            #print(len(i))
            for j in i:
                #print("j is:")
                #print(j)
                #print("len(j) is:")
                #print(len(j))
                if j == v and j != i[-1]:
                    #print("(i.index(j) is")
                    #print((i.index(j)))
                    #print("i[i.index(j)] is")
                    #print(i[i.index(j)])
                    if len(i) > 1:
                        edge = []
                        edge.append(v)
                        #print("i indices")
                        #print(i)
                        #print(len(i))
                        #print(i[i.index(j)])
                        edge.append(i[i.index(j)+1])
                        edges_of_v_in_P.append(edge)
        #print("edges of v in P:")
        #print(edges_of_v_in_P)
        #print(len(edges_of_v_in_P))
        #remove duplicate elements for edges_of_v_in_P
        no_duplicates = []
        for i in edges_of_v_in_P:
            if i not in no_duplicates:
                no_duplicates.append(i)
        print("edges_of_v_in_P")
        edges_of_v_in_P = no_duplicates
        print(edges_of_v_in_P)

        #print(edges_of_v_in_P)
        # let p_i be the number of paths in P containing (v,w_i)
        p = []
        for i in range(len(edges_of_v_in_P)):
            counter = 0
            for j in range(len(P)):
                if str(edges_of_v_in_P[i]).strip("[]") in str(P[j]):
                    #print(str(edges_of_v_in_P[i]))
                    counter = counter + 1
            p.append(counter)
        print("p is:")
        print(p)
        #checking how many agents do we want to send overall

        for i in range(len(p)):
            sum_p = sum_p + p[i]

        # for i = 1 to r
        previous_agents = agents.copy()
        for i in range(len(edges_of_v_in_P)):
            #print(agents)
            print("i is:")
            print(i)
            #print("p[i] is")
            #print(p[i])
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
            print("list of agents on v")
            print(list_of_agents_on_v)
            print("v is")
            print(v)


            position_of_agents_on_v = []

            # in this for loop, for each k, we only move one agent at a time, k in range(nr_of_agents_on_v total agents
            for k in range(nr_of_agents_on_v):
                #print("k is:")
                #print(type(k))
                #print(k)
                #print("nr_of_agents_on_v")
                #print(type(nr_of_agents_on_v))
                #print(nr_of_agents_on_v)
                #print("list_of_agents_on_v")
                #print(type(list_of_agents_on_v))
                #print(list_of_agents_on_v)
                #print("edges of v in P")
                #print(type(edges_of_v_in_P[i]))
                #print(edges_of_v_in_P[i])
                position_of_agents_on_v.append(edges_of_v_in_P[i][1])
                #print("#print(list_of_agents_on_v[k+1])")
                #print(list_of_agents_on_v[k])
                #print("position_of_agents_on_v[k]")
                #print("position_of_agents_on_v[k]")
                for key in agents:
                    if list_of_agents_on_v[k] == key and len(true_list_of_agents_on_v) > 1:
                        agents[key] = position_of_agents_on_v[k]
                        #print("agents")
                        #print(agents)

            #print("moved p_i agents to w_i, agents are right now at:")
            #print(agents)
            #print(color)
        mesh_2d.color_sync(Z, agents, previous_agents, color, m)
        print(agents)
        print(color)
        print("iteration is over")
        iterations = iterations + 1
        print("nr of iterations so far")
        print(iterations)

        #print(flipped_agents)
        values = list(agents.values())
        print("values")
        print(values)
        print("set(values)")
        print(set(values))
        if previous_values == values:
            print("loop stuck")
            exit()
        print(agents)
        # check for something wrong?
        if sum_p + 1 != len(truest_list_of_agents_on_v):
            print(sum_p)
            print(len(true_list_of_agents_on_v))
            print("something horrible happened")
            exit()
    print(agents)


    if m > 1:
        itercube(2, y_global, dims, m, agents, Z, color)

    if m == 1:
        brick(2, 1, dims, agents, y, Z, color, m)

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


def move(A, x, y, agents, dimensions):
    for key in agents:
        (a, b) = agents[key]
        #if first vertex
        if A[0] == 1:
            #if the first coord is right
            if a == A[1]:
                # if we want to modify the 1st index
                if x == 1:
                    agents[key] = ((a+y) % dimensions[0], b)
                # if we want to modify the 2nd index
                if x == 2:
                    agents[key] = (a, (b+y) % dimensions[1])
        # if second vertex
        if A[0] == 2:
            #if the 2nd coord is right
            if b == A[1]:
                #if we want to modify the 1st index
                if x == 1:
                    agents[key] = ((a+y) % dimensions[0], b)
                # if we want to modify the 2nd index
                if x == 2:
                    agents[key] = (a, (b+y) % dimensions[1])

def cube(t,y, dimensions, agents, Z, color, m):
    if t == 2:
        shift = 0
        print("cube is starting")
        for o in range(int(dimensions[1] / 2)):
            for i in range(dimensions[0] - 2):
                previous_agents = agents.copy()
                move([1, (shift + 1) % dimensions[0]], 1, y, agents, dimensions)
                print("we just moved the agents on the vertices, where " + str(1) + "st coord is " +str((shift + 1) % dimensions[0]) + ", its first coord is changed by " + str(y))
                shift = shift + y
                print("shift became")
                print(shift)
                mesh_2d.color_sync(Z, agents, previous_agents, color, m)
                print(agents)
            y = 0 - y
            if o < (int(dimensions[1] / 2)) - 1:
                previous_agents = agents.copy()
                move([2, (0 - o) % dimensions[1]], 2, -1, agents, dimensions)
                move([2, (1 + o) % dimensions[1]], 2, 1, agents, dimensions)
                mesh_2d.color_sync(Z, agents, previous_agents, color, m)
                print("if happened")
                print(agents)
    else:
        for h in range(dimensions[(t-1)]):
            cube(t-1, y, dimensions, agents)
            if h < dimensions[(t-1)/2] -1:
                previous_agents = agents.copy()
                move([t, 0], t, -1, agents, dimensions)
                print(agents)
                move([t, 1], t, 1, agents, dimensions)
                mesh_2d.color_sync(Z, agents, previous_agents, color, m)
                print(agents)

def itercube(s,y, dimensions, m, agents, Z, color):
    if s == 4 - m:
        cube(s, y, dimensions, agents, Z, color, m)
    else:
        for i in range(dimensions[s - 1]):
            previous_agents = agents.copy()
            itercube(s-1, y, dimensions, m, agents)
            move([1, 1], s, 1, agents)
            move([1, 2], s, 1, agents)
            mesh_2d.color_sync(Z, agents, previous_agents, color, m)

def brick(t, b, dimensions, agents, y, Z, color, m):
    if t == b+1:
        shift = 0
        print("i in range is")
        print(dimensions[b])
        for i in range((dimensions[b]) - 2):
            previous_agents = agents.copy()
            move([b+1, shift + 1], b+1, y, agents, dimensions)
            shift = shift + y
            print("moved")
            print(agents)
            mesh_2d.color_sync(Z, agents, previous_agents, color, m)
        y = 0 - y
    else:
        for o in range(int((dimensions[t-1] / 2)) - 1):
            brick(t-1)
            if o < (dimensions[t-1] / 2) - 1:
                move([t, 0], t, -1, agents, dimensions)
                move([t, 1], t, -1, agents, dimensions)



create_grid_2d(11, 11, True, 1)
