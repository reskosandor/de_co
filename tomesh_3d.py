import networkx as nx
import matplotlib.pyplot as plt
import math
import functions
import time

y_global = 1
w_global = 1
move_counter = 0
def create_grid_3d(dimensions, m):
    start_time = time.time()
    global y_global
    global w_global
    global move_counter
    y_global = 1
    w_global = 1


    dims = [dimensions[2], dimensions[1], dimensions[0]]
    dim1 = dimensions[0]
    dim2 = dimensions[1]
    dim3 = dimensions[2]


    if dim2 < dim1 or dim3 < dim2 or dim3 < dim1:
        print("dimensions must be in monotonic increasing sequence")
        exit()

    if m <= 0:
        print("m must be a positive integer")
        exit()

    if m > 4:
        print("algorithm is not needed, decontamination is trivial")
        exit()

    Z = nx.grid_graph(dims, periodic=True)

    # ---initial_set_(3, m)_begins)---
    # ---creating_C---
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

    # constructing P in a new way
    # v = (0, 0, 0) is in the bottom left corner
    # shortest path: move forward in the first dimension as long as we need to, then second, then third dimension
    for i in list(C.nodes):
        sublist = []
        (x, y, z) = i

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

        P.append(sublist)
    print("Starting INITIAL-SET")
    #starting with |C| agents in v_0
    for i in range(nr_of_agents):
        agents[i] = (0, 0, 0)
    print("agents are " + str(agents))
    functions.color_sync(Z, agents, previous_agents, color, m)
    print("color is " + str(color))

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
        v = (0, 0)
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
        previous_agents = agents.copy()
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

            functions.color_sync(Z, agents, previous_agents, color, m)
            print("agents are " + str(agents))
            print("color is " + str(color))

        iterations = iterations + 1

        values = list(agents.values())
        if previous_values == values:
            print("loop stuck")
            exit()
        # check for something wrong?
        if sum_p + 1 != len(truest_list_of_agents_on_v):
            print("something horrible happened")
            exit()
    #try snapshotting agents
    agents_snapshot = agents.copy()
    after_init = move_counter
    # variable declaration
    t = 6 - m
    s = 3
    b = 3 - m

    if m >= 3:
        itercube(s, dimensions, m, agents, Z, color, agents_snapshot)

    if m <= 2:
        brick(3, b, dimensions, agents, Z, color, m, agents_snapshot)

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

    move_counted = move_counter
    print("total moves: " + str(move_counted))
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
    print("Starting CUBE")
    if t == 2:
        print("t=2, continue")
        for o in range(math.floor(dimensions[1] / 2)):
            for i in range(dimensions[0] - 2):
                previous_agents = agents.copy()
                move([1, 1 % dimensions[0]], 1, y_global, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("agents are" + str(agents))
                print("color is " + str(color))
            y_global = 0 - y_global
            if o < (math.floor(dimensions[1] / 2)) - 1:
                previous_agents = agents.copy()
                #this is the move along the second dimension
                #this needs to be working for odd dimensions
                #also keep in mind the + 1 for the iteration (<= correction)
                move([2, 0 % dimensions[1]], 2, -w_global, agents, dimensions, agents_snapshot)
                move([2, 1 % dimensions[1]], 2, w_global, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("agents are" + str(agents))
                print("color is " + str(color))
            if dimensions[1] % 2 == 1 and o == (math.floor(dimensions[1] / 2)) - 1:
                previous_agents = agents.copy()
                move([2, 0 % dimensions[1]], 2, -w_global, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("agents are" + str(agents))
                print("color is " + str(color))
                for i in range(dimensions[0] - 2):
                    previous_agents = agents.copy()
                    move([1, 1 % dimensions[0]], 1, y_global, agents, dimensions, agents_snapshot)
                    functions.color_sync(Z, agents, previous_agents, color, m)
                    print("agents are" + str(agents))
                    print("color is " + str(color))
                y_global = 0 - y_global

        w_global = 0 - w_global
    else:
        print("t=2 is false, recursively calling CUBE")
        for h in range(math.ceil(dimensions[(t-1)]/2)):
            cube(t-1, dimensions, agents, Z, color, m, agents_snapshot)
            if h < int((dimensions[t-1])/2) -1 or dimensions[t-1] % 2 == 1 and h < int((dimensions[t-1])/2):
                previous_agents = agents.copy()
                move([t, 0], t, -1, agents, dimensions, agents_snapshot)
                move([t, 1], t, 1, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("agents are" + str(agents))
                print("color is " + str(color))

def itercube(s, dimensions, m, agents, Z, color, agents_snapshot):
    print("Starting ITERCUBE")
    if s == 6 - m:
        print("s = 2d-m, continue")
        cube(s, dimensions, agents, Z, color, m, agents_snapshot)
    else:
        print("s = 2d-m is false, recursively calling ITERCUBE")
        for i in range(dimensions[s - 1]):
            previous_agents = agents.copy()
            itercube(s-1, dimensions, m, agents, Z, color, agents_snapshot)
            functions.color_sync(Z, agents, previous_agents, color, m)
            if functions.color_check(color) == False:
                previous_agents = agents.copy()
                move([1, 1], s, 1, agents, dimensions, agents_snapshot)
                move([1, 0], s, 1, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("agents are" + str(agents))
                print("color is " + str(color))

def brick(t, b, dimensions, agents, Z, color, m, agents_snapshot):
    global y_global
    print("Starting BRICK")
    if t == b+1:
        print("t=b+1, continue")
        for i in range((dimensions[b]) - 2):
            previous_agents = agents.copy()
            #this is the move in the second dimension, i dont think there is a problem here
            #need to check if cube problem is present here tho
            move([b+1, 1], b+1, y_global, agents, dimensions, agents_snapshot)
            functions.color_sync(Z, agents, previous_agents, color, m)
            print("agents are" + str(agents))
            print("color is " + str(color))
        y_global = 0 - y_global
    else:
        print("t=b+1 is false, recursively calling BRICK")
        for o in range(math.ceil((dimensions[t-1] / 2))):
            brick(t-1, b, dimensions, agents, Z, color, m, agents_snapshot)
            if o < (dimensions[t-1] / 2) - 1:
                previous_agents = agents.copy()
                #moving in the 3rd dimension, this needs to be working for odd numbers
                #just move one of them one more time
                move([t, 0], t, -1, agents, dimensions, agents_snapshot)
                move([t, 1], t, +1, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("agents are" + str(agents))
                print("color is " + str(color))
            if o == math.ceil((dimensions[t-1] / 2)) - 1 and (dimensions[t-1]) % 2 == 1:
                previous_agents = agents.copy()
                move([t, 0], t, -1, agents, dimensions, agents_snapshot)
                functions.color_sync(Z, agents, previous_agents, color, m)
                print("agents are" + str(agents))
                print("color is " + str(color))


