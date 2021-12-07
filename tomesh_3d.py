import networkx as nx
import matplotlib.pyplot as plt
import math
import functions
import time

y_global = 1
w_global = 1
move_counter = 0
def create_grid_3d(dimensions, isperioidic, m):
    start_time = time.time()
    global y_global
    global w_global
    global move_counter
    y_global = 1
    w_global = 1
    print("move counter at starting position is " + str(move_counter))


    dims = [dimensions[2], dimensions[1], dimensions[0]]
    print("dimensions are the following: " + str(dims), flush=True)
    dim1 = dims[0]
    dim2 = dims[1]
    dim3 = dims[2]


    if dim2 < dim1 or dim3 < dim2 or dim3 < dim1:
        print("dimensions must be in monotonic increasing sequence")
        exit()

    if m <= 0:
        print("m must be a positive integer")
        exit()

    if m > 4:
        print("algorithm is not needed, decontamination is trivial")
        exit()

    Z = nx.grid_graph(dimensions, periodic=isperioidic)

    print(nx.info(Z))
    #nx.draw(Z)
    #plt.show()
    # ---initial_set_(3, m)_begins)---
    # ---creating_C---
    print(list(Z.nodes))
    C = Z.copy()
    if (m == 1):
        for i in list(C.nodes):
            (x, y, z) = i
            if z > 1:
                C.remove_node((x, y, z))

    if (m == 2):
        for i in list(C.nodes):
            (x, y, z) = i
            if y > 1 or z > 1:
                C.remove_node((x, y, z))

    if (m == 3):
        for i in list(C.nodes):
            (x, y, z) = i
            if y > 1 or x > 1 or z > 1:
                C.remove_node((x, y, z))

    if (m == 4):
        for i in list(C.nodes):
            (x, y, z) = i
            if y > 1 or x > 1 or z > 0:
                C.remove_node((x, y, z))

    if (m == 5):
        for i in list(C.nodes):
            (x, y, z) = i
            if y > 0 or x > 1 or z > 0:
                C.remove_node((x, y, z))

    if (m >= 6):
        C = nx.Graph()
        C.add_node((0, 0, 0))

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
    functions.color_sync(Z, agents, previous_agents, color, m)
    print(color)
    #start with a set of |C| agents in v_(0,0)
    nr_of_agents = C.number_of_nodes()

    # constructing P in a new way
    # v = (0, 0, 0) is in the bottom left corner
    # shortest path: move forward in the first dimension as long as we need to, then second, then third dimension
    for i in list(C.nodes):
        #print(nx.shortest_path(C, source = (0, 0, 0), target = i))
        #P.append(nx.shortest_path(C, source = (0, 0, 0), target = i))
        sublist = []
        print("(x,y, z) is:")
        (x, y, z) = i
        print((x, y, z))

        sublist.append((0, 0, 0))
        k = 0
        l = 0
        n = 0
        for j in range(x):
            k = k + 1
            sublist.append((k, 0, 0))

        if y > 0:
            for j in range(y):
                l = l + 1
                sublist.append((x, l, 0))

        if z > 0:
            for n in range(z):
                n = n + 1
                sublist.append((x, y, n))

        print(sublist)
        P.append(sublist)
    print("P is :")
    print(P)
    #starting with |C| agents in v_0
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
    print("agents at the end of INITIAL SET")
    print(agents)
    #try snapshotting agents
    agents_snapshot = agents.copy()
    after_init = move_counter
    # variable declaration
    t = 6 - m
    s = 3
    b = 3 - m

    if m >= 3:
        itercube(s, dims, m, agents, Z, color, agents_snapshot)

    if m <= 2:
        brick(3, b, dims, agents, Z, color, m, agents_snapshot)

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
    print("after init is " + str(after_init))

    move_counted = move_counter
    print("move counted is " + str(move_counted))
    move_counter = 0
    y_global = 1
    w_global = 1
    end_time = time.time() - start_time
    return [nr_of_agents, after_init, move_counted, end_time]

def move(A, x, y, agents, dimensions, agents_snapshot):
    global move_counter
    for key in agents_snapshot:
        (a, b, c) = agents[key]
        (d, e ,f) = agents_snapshot[key]
        #if first vertex
        if A[0] == 1:
            #if the first coord is right
            if d == A[1]:
                # if we want to modify the 1st index
                if x == 1:
                    agents[key] = ((a+y) % dimensions[0], b, c)
                    move_counter = move_counter + 1
                # if we want to modify the 2nd index
                if x == 2:
                    agents[key] = (a, (b+y) % dimensions[1], c)
                    move_counter = move_counter + 1
                # if we want to modify the 3rd index
                if x == 3:
                    agents[key] = (a, b, (c+y) % dimensions[2])
                    move_counter = move_counter + 1
        # if second vertex
        if A[0] == 2:
            #if the 2nd coord is right
            if e == A[1]:
                #if we want to modify the 1st index
                if x == 1:
                    agents[key] = ((a+y) % dimensions[0], b, c)
                    move_counter = move_counter + 1
                # if we want to modify the 2nd index
                if x == 2:
                    agents[key] = (a, (b+y) % dimensions[1], c)
                    move_counter = move_counter + 1
                # if we want to modify the 3rd index
                if x == 3:
                    agents[key] = (a, b, (c+y) % dimensions[2])
                    move_counter = move_counter + 1
        # if third vertex
        if A[0] == 3:
            #if the 3rd coord is right
            if f == A[1]:
                # if we want to modify the 1st index
                if x == 1:
                    agents[key] = ((a + y) % dimensions[0], b, c)
                    move_counter = move_counter + 1
                # if we want to modify the 2nd index
                if x == 2:
                    agents[key] = (a, (b + y) % dimensions[1], c)
                    move_counter = move_counter + 1
                # if we want to modify the 3rd index
                if x == 3:
                    agents[key] = (a, b, (c + y) % dimensions[2])
                    move_counter = move_counter + 1


def cube(t, dimensions, agents, Z, color, m, agents_snapshot):
    global y_global
    global w_global
    if t == 2:
        #shift = 0
        print("cube is starting")
        for o in range(math.floor(dimensions[1] / 2)):
            for i in range(dimensions[0] - 2):
                previous_agents = agents.copy()
                move([1, 1 % dimensions[0]], 1, y_global, agents, dimensions, agents_snapshot)
                print("we just moved the agents on the vertices, where 1st coord is " + str(1 % dimensions[0]) + ", its first coord is changed by " + str(y_global))
                #shift = shift + y
                #print("shift became")
                #print(shift)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print(agents)
            y_global = 0 - y_global
            print("value of y is " + str(y_global))
            if o < (math.floor(dimensions[1] / 2)) - 1:
                previous_agents = agents.copy()
                #this is the move along the second dimension
                #this needs to be working for odd dimensions
                #also keep in mind the + 1 for the iteration (<= correction)
                move([2, 0 % dimensions[1]], 2, -w_global, agents, dimensions, agents_snapshot)
                move([2, 1 % dimensions[1]], 2, w_global, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("if happened (moving along second dimension)")
                print(agents)
            if dimensions[1] % 2 == 1 and o == (math.floor(dimensions[1] / 2)) - 1:
                print("this is where the fun begins")
                previous_agents = agents.copy()
                move([2, 0 % dimensions[1]], 2, -w_global, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("agents are " + str(agents))
                for i in range(dimensions[0] - 2):
                    previous_agents = agents.copy()
                    move([1, 1 % dimensions[0]], 1, y_global, agents, dimensions, agents_snapshot)
                    print("we just moved the agents on the vertices, where 1st coord is " + str(1 % dimensions[0]) + ", its first coord is changed by " + str(y_global))
                    #shift = shift + y
                    #print("shift became")
                    #print(shift)
                    functions.color_sync(Z, agents, previous_agents, color, m)
                    print(agents)
                y_global = 0 - y_global
                print("we finished with the odd stuff")
            print("we finshed")

        w_global = 0 - w_global
    else:
        for h in range(math.ceil(dimensions[(t-1)]/2)):
            print("calling CUBE recursively for t-1")
            cube(t-1, dimensions, agents, Z, color, m, agents_snapshot)
            if h < int((dimensions[t-1])/2) -1:
                print("h is " + str(h))
                previous_agents = agents.copy()
                move([t, 0], t, -1, agents, dimensions, agents_snapshot)
                print(agents)
                move([t, 1], t, 1, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print(agents)

def itercube(s, dimensions, m, agents, Z, color, agents_snapshot):
    if s == 6 - m:
        print("ITERCUBE s == 6-m commencing")
        cube(s, dimensions, agents, Z, color, m, agents_snapshot)
    else:
        print("ITERCUBE else is commencing")
        for i in range(dimensions[s - 1]):
            previous_agents = agents.copy()
            #print("y is " + str(y_global))
            itercube(s-1, dimensions, m, agents, Z, color, agents_snapshot)
            functions.color_sync(Z, agents, previous_agents, color, m)
            print("moving 1 in the " + str(s) + "th dimension")
            if functions.color_check(color) == False:
                previous_agents = agents.copy()
                move([1, 1], s, 1, agents, dimensions, agents_snapshot)
                move([1, 0], s, 1, agents, dimensions, agents_snapshot)
                print(agents)
                functions.color_sync(Z, agents, previous_agents, color, m)

def brick(t, b, dimensions, agents, Z, color, m, agents_snapshot):
    global y_global
    print("are we getting at the start of the brick?")
    if t == b+1:
        print("did we pass t == b+1?")
        print("i in range is")
        print(dimensions[b])
        for i in range((dimensions[b]) - 2):
            previous_agents = agents.copy()
            #this is the move in the second dimension, i dont think there is a problem here
            #need to check if cube problem is present here tho
            move([b+1, 1], b+1, y_global, agents, dimensions, agents_snapshot)
            print("moved")
            print(agents)
            functions.color_sync(Z, agents, previous_agents, color, m)
        y_global = 0 - y_global
    else:
        for o in range(math.ceil((dimensions[t-1] / 2))):
            print("range of the o is " +str(int((dimensions[t-1] / 2)) - 1))
            print("o currently is " +str(o))
            brick(t-1, b, dimensions, agents, Z, color, m, agents_snapshot)
            if o < (dimensions[t-1] / 2) - 1:
                previous_agents = agents.copy()
                #moving in the 3rd dimension, this needs to be working for odd numbers
                #just move one of them one more time
                move([t, 0], t, -1, agents, dimensions, agents_snapshot)
                move([t, 1], t, +1, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
            if o == math.ceil((dimensions[t-1] / 2)) - 1 and (dimensions[t-1]) % 2 == 1:
                print("this is where the fun begins")
                print("the ceiling is the " + str(math.ceil((dimensions[t-1] / 2)) - 1))
                previous_agents = agents.copy()
                move([t, 0], t, -1, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("funny business over")


