import networkx as nx
import matplotlib.pyplot as plt
import functions
import random
import time

previous_node = -1

move_counter = 0

def tree(lr, m):
    start_time = time.time()
    global move_counter
    global number_of_agents
    global previous_node
    previous_node = -1
    print("move counter at starting position is " + str(move_counter))
    print("asd")
    T = nx.algorithms.tree.coding.from_prufer_sequence(lr)
    T_degree = T.degree()
    print(nx.info(T))
    #nx.draw(T)
    #plt.show()


    print(len([n for n in T.neighbors(0)]))
    print(T.degree[0])
    print(T.nodes)

    def subtree(T, v_1, v):
        T_v1_v = T.copy()
        T_v1_v.remove_edge(v_1, v)
        #print(list(T_v1_v))
        for node in list(T_v1_v):
            if node in nx.algorithms.dag.descendants(T_v1_v, v_1) or node == v_1:
                #print(str(node) + " can remain")
                pass
            else:
                T_v1_v.remove_node(node)
                #print(str(node) + " booped")
        return T_v1_v
    print(T.edges())
    print(list(T))
    #print(list(subtree(T, 7, 1)))





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
        #print("v is....")
        #print(v, flush=True)
        #print(type(v), flush=True)
        #print(T, flush=True)
        #print(type(T))
        #print("T consists of nodes:")
        #print(list(T))
        #print("v degree is...")
        #print(T.degree[v])

        #print(type(T.degree[v]))
        #print(T.degree[v], flush=True)
        if T.degree[v] > 0:
            v_1 = neighbors_of_v(T, v)[0]
            alpha_of_neighbors = {}
            neigh_list = neighbors_of_v(T, v)
            for node in neigh_list:
                alpha_of_neighbors[node] = alpha(node, subtree(T, node, v), m)
            max_key = max(alpha_of_neighbors, key=alpha_of_neighbors.get)
        #print("neighbors are ordered by alpha, now evaluation by degree commencing")
        if T.degree[v] == 0:
        #if degree(T, v) == 0:
            '''print(T.degree[v], flush=True)
            print("branch 1")
            print("returning one")'''
            return 1
        elif 0 < T.degree[v] <= m:
            #print("branch 2")
            value = alpha_of_neighbors[max_key]
            #print("returning " + str(value), flush=True)
            return value
        elif T.degree[v] > m and branch3(max_key, alpha_of_neighbors):
            #print("branch 3")
            value = alpha_of_neighbors[max_key]
            #print("returning " + str(value), flush=True)
            return value
        elif T.degree[v] > m and branch4(max_key, alpha_of_neighbors):
            #print("branch 4")
            value = alpha_of_neighbors[max_key] + 1
            #print("returning " + str(value), flush=True)
            return value






    agents = {}
    previous_agents = {}
    color = {}

    for nodes in T:
        color[nodes] = "grey"
    functions.color_sync(T, agents, previous_agents, color, m)
    print(color)
    T_original = T.copy()

    def mu(v, T, m):

        neigh_list = neighbors_of_v(T, v)
        print("neigh list is of " + str(v) + " is " + str(neigh_list))

        if T.degree[v] == 0:
            return 0
        else:
            ret = 0
            for node in neigh_list:
                ret = ret + mu(node, subtree(T, node, v), m) + 2 * alpha(node, subtree(T, node, v), m)
            return ret


    def decontaminate(T, v, m, T_original):
        global previous_node
        global move_counter
        global number_of_agents
        print("decont v is " + str(v))
        print("decont T is " + str(list(T)))
        previous_agents = agents.copy()
        nr_of_agents = alpha(v, T, m)

        for i in range(nr_of_agents):
            if previous_node == -1:
                agents[i] = v
                number_of_agents = nr_of_agents
            else:
                if agents[i] == previous_node:
                    agents[i] = v
                    move_counter = move_counter + 1

        print("moving " + str(nr_of_agents) + " agents to " + str(v))
        functions.color_sync(T_original, agents, previous_agents, color, m)
        print("agents are " + str(agents))
        print("color is " + str(color))
        print("previous node is " + str(previous_node))
        if T.degree(v) != 0:
            v_neighbours = neighbors_of_v(T, v)
            a = {}
            print("v_neighbours is " + str(v_neighbours))
            #calculating alpha for all neighbours
            for node in v_neighbours:
                a[node] = (alpha(node, T, m))
            ordered_v_neighbours = []
            print("state of a before the for loop is " + str(a))
            for key in a:
                print("current state of a is " + str(a))
                max_key = max(a, key=a.get)
                print("the max key is " + str(max_key))
                ordered_v_neighbours.append(max_key)
                a[max_key] = -1
                if len(ordered_v_neighbours) == len(a):
                    break
            print("len of ordered_v_neighbors is " + str(len(ordered_v_neighbours)) + "and its contents are " + str(ordered_v_neighbours))
            for neighbor in reversed(ordered_v_neighbours):
                print("ordered_v_neighbours is " + str(ordered_v_neighbours))
                previous_node = v
                decontaminate(subtree(T, neighbor, v), neighbor, m, T_original)

                previous_agents = agents.copy()
                howmany = 0
                print("before moving back, the current value of neighbor is " + str(neighbor))
                for i in agents:
                    print("the i and agent[i] we're moving is currently: " + str(i) + " " + str(agents[i]))
                    if agents[i] == neighbor:
                        agents[i] = v
                        howmany = howmany+1
                        move_counter = move_counter + 1
                print("we were in a leaf, now we're moving back " + str(howmany) + " agents from" + str(neighbor) + " to " + str(v))
                functions.color_sync(T_original, agents, previous_agents, color, m)
                print("agents are " + str(agents))
                print("color is " + str(color))
                print("previous node is " + str(previous_node))

        else:
            print("we have reached a leaf")
    #print(mu(3, T, m))
    #decontaminate(T, 3, m, T_original)

    a_try = {}
    for node in list(T):
        a_try[node] = (alpha(node, T, m))
        print("appended alpha value for node " + str(node) + " is: " + str(a_try[node]))
    print("a_try is " + str(a_try))

    mu_try = {}
    for node in list(T):
        mu_try[node] = (mu(node, T, m))
        print("appended mu value for node " + str(node) + " is: " + str(mu_try[node]))
    print("mu_try is " + str(mu_try))
    #getting nodes with minimum alpha value
    min_a = []
    minval = min(a_try.values())
    min_a = [k for k, v in a_try.items() if v==minval]
    print("a_try is " + str(a_try))
    print("min_a is " + str(min_a))
    #getting nodes with minimum mu value, where they have the min alpha value
    min_mu_temp = mu_try.copy()
    min_mu = min_mu_temp.copy()
    for i in min_mu_temp:
        if i not in min_a:
            del min_mu[i]
    minimum_mu = []
    minval = min(min_mu.values())
    minimum_mu = [k for k, v in min_mu.items() if v==minval]
    print("minimum_mu value is: " + str(minval))
    print("minimum_mu is " +str(minimum_mu))

    def optimaltreedecontamination(T, m, T_original):
        starting_node = minimum_mu[0]
        decontaminate(T, starting_node, m, T_original)

    optimaltreedecontamination(T, m, T_original)
    #decontaminate(T, 0, m, T_original)


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
    move_counted = move_counter
    print("number of agents is " +str(number_of_agents))
    print("move counted is " + str(move_counted))
    move_counter = 0
    end_time = time.time() - start_time
    return(number_of_agents, move_counted, end_time)

