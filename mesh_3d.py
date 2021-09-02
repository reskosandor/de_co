import networkx as nx
import matplotlib.pyplot as plt
import functions
import time

move_counter = 0

def create_grid_3d(dimensions, isperioidic, m):
    start_time = time.time()
    global move_counter
    move_counter = 0
    #print(dimensions)
    dim1 = dimensions[2]
    dim2 = dimensions[1]
    dim3 = dimensions[0]
    #print(dim1)
    #print(dim2)
    #print(dim3)
    if dim2 < dim1 or dim3 < dim2 or dim3 < dim1:
        print("dimensions must be in monotonic increasing sequence")
        exit()

    if m == 0:
        print("m must be a positive integer")
        exit()

    if m > 3:
        print("m must not be greater than the dimension of the mesh")
        exit()
    Z = nx.grid_graph(dimensions, periodic=isperioidic)
    ##print(nx.info(Z))
    #nx.draw(Z)
    #plt.show()
    #---initial_set_(2, m)_begins)---
    #---creating_C---
    #print("nodes of Z")
    #print(list(Z.nodes))
    if (m == 1):
        C = Z.copy()
        for x in range(dim1):
            for y in range(dim2):
                for z in range(dim3):
                    #print(str(x) + " " + str(y) + " " + str(z))
                    if z > 0:
                        C.remove_node((x, y, z))
        #print(list(C.nodes))

    if (m == 2):
        C = Z.copy()
        for x in range(dim1):
            for y in range(dim2):
                for z in range(dim3):
                    #print(str(x) + " " + str(y) + " " + str(z))
                    if y > 0 or z > 0:
                        C.remove_node((x, y, z))

    if (m == 3):
        C = nx.Graph()
        C.add_node((0, 0, 0))

    #print(nx.info(C))
    #print(list(C.nodes))
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
    functions.color_sync(Z, agents, previous_agents, color, m)
    #print(color)
    #start with a set of |C| agents in v_(0,0)
    nr_of_agents = C.number_of_nodes()

    # constructing P in a new way
    # v = (0, 0, 0) is in the bottom left corner
    # shortest path: move "up" as long as we need to, then move "right" as long as we need to
    for i in list(C.nodes):
        #print(nx.shortest_path(C, source = (0, 0, 0), target = i))
        #P.append(nx.shortest_path(C, source = (0, 0, 0), target = i))
        sublist = []
        print("(x,y,z) is:")
        (x, y, z) = i
        print((x, y, z))

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

        print(sublist)
        P.append(sublist)
    print("P is :")
    print(P)
    for i in range(nr_of_agents):
        agents[i] = (0, 0, 0)
    #print(agents)
    functions.color_sync(Z, agents, previous_agents, color, m)
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
        v = (0, 0, 0)
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
                        move_counter = move_counter + 1
                        #print("agents")
                        #print(agents)

            #print("moved p_i agents to w_i, agents are right now at:")
            #print(agents)
            #print(color)
        functions.color_sync(Z, agents, previous_agents, color, m)
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
    after_init = move_counter
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
        #print("canonical_path")
        #print(canonical_path)
        #print(len(canonical_path))
        # moving agent through canonical path
        for i in range(len(canonical_path) - 1):
            previous_agents = agents.copy()
            agents[0] = canonical_path[i + 1]
            move_counter = move_counter + 1
            #print(agents[0])
            functions.color_sync(Z, agents, previous_agents, color, m)
            #print(color)
    if m == 2:
        previous_agents = agents.copy()
        functions.color_sync(Z, agents, previous_agents, color, m)
        print(color)
        print(agents)
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
                print(agents)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print(color)
            previous_agents = agents.copy()
            #now all agents moved one in the y coord
            # move one agent at a time, increasing z coord
            # make sure to not move in the direction of z for the last time
            if i < (dim3 - 1):
                for k in range(dim1):
                    (x, y, z) = agents[k]
                    agents[k] = (x, y, z + 1)
                    move_counter = move_counter + 1
                print(agents)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print(color)
    if m == 1:
        #print(agents)
        for i in range(dim3-1):
            previous_agents = agents.copy()
            for j in range(nr_of_agents):

                #print("agents: ")
                #print(type(agents))
                #print(agents)
                (x, y, z) = agents[j]
                agents[j] = (x, y, z+1)
                move_counter = move_counter + 1
            #print(agents)
            functions.color_sync(Z, agents, previous_agents, color, m)
            #print(color)
    #print(list(Z.nodes))
    #print(color)
    #print(list(Z.nodes))
    #print(color)
    nr_of_black_nodes = 0
    for key in color:
        if color[key] == "black":
            #print(key)
            nr_of_black_nodes = nr_of_black_nodes + 1
    print(nr_of_black_nodes)
    #print("nr of iterations")
    #print(iterations)
    for key in color:
        if color[key] == "grey":
            print("some nodes are grey, algorithm failed")
            exit()
    print("no grey nodes remain")
    print("after_init is " + str(after_init))
    print("move_counter is " + str(move_counter))
    move_counted = move_counter
    move_counter = 0
    end_time = time.time() - start_time
    return [nr_of_agents, after_init, move_counted, end_time]
# grid_graph takes a list of dimensions as its input
# for some reason dimensions are in reverse order
# so the first item of the list will be the nth dimension


dimensions = [2, 2, 2]

#create_grid_3d(dimensions, False, 1)
