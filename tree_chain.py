import networkx as nx
import matplotlib.pyplot as plt
import functions
from random import uniform, randrange
import time
import sys

previous_node = -1
starting_node = -1
nr_of_agents = -1
move_counter = 0
agents = {}
def tree(lr, m, p, nr_a = -1):
    start_time = time.time()
    global number_of_agents
    global previous_node
    global starting_node
    global nr_of_agents
    global move_counter
    global agents
    previous_node = -1
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
        print("v is....")
        print(v, flush=True)
        #print(type(v), flush=True)
        #print(T, flush=True)
        #print(type(T))
        print("T consists of nodes:")
        print(list(T))
        print("v degree is...")
        print(T.degree[v])

        #print(type(T.degree[v]))
        #print(T.degree[v], flush=True)
        if T.degree[v] > 0:
            v_1 = neighbors_of_v(T, v)[0]
            alpha_of_neighbors = {}
            neigh_list = neighbors_of_v(T, v)
            for node in neigh_list:
                alpha_of_neighbors[node] = alpha(node, subtree(T, node, v), m)
            max_key = max(alpha_of_neighbors, key=alpha_of_neighbors.get)
        print("neighbors are ordered by alpha, now evaluation by degree commencing")
        if T.degree[v] == 0:
        #if degree(T, v) == 0:
            print(T.degree[v], flush=True)
            print("branch 1")
            print("returning one")
            return 1
        elif 0 < T.degree[v] <= m:
            print("branch 2")
            value = alpha_of_neighbors[max_key]
            print("returning " + str(value), flush=True)
            return value
        elif T.degree[v] > m and branch3(max_key, alpha_of_neighbors):
            print("branch 3")
            value = alpha_of_neighbors[max_key]
            print("returning " + str(value), flush=True)
            return value
        elif T.degree[v] > m and branch4(max_key, alpha_of_neighbors):
            print("branch 4")
            value = alpha_of_neighbors[max_key] + 1
            print("returning " + str(value), flush=True)
            return value







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

    def height(v, T):
        T_height = -1
        for node in T:
            if node != v:
                node_distance = len(nx.shortest_path(T, source = v, target= node))
                if T_height < node_distance:
                    T_height = node_distance
        return T_height

    def homebase_node(T):
        root = -3
        root_height = sys.maxsize
        min_of_max_dist = []
        #need to create a dummy list first
        for node in T:
            min_of_max_dist.append(-1)
        for node in T:
            print("this is T")
            print(T)
            min_of_max_dist[node] = height(node, T)
        print("minofmaxdist after")
        for i in range(len(min_of_max_dist)):
            if min_of_max_dist[i] < root_height:
                root = i
                root_height = min_of_max_dist[i]
        return root, root_height


    def chain_agents_down(root, target):
        global move_counter
        global agents
        agents_0 = agents.copy()
        agents[0] = target
        agents = functions.sorted_dict(agents)
        move_counter = move_counter + 1
        for i in agents:
            if i > 0:
                print("i is " + str(i) + " and agents is " + str(agents) + " and agents_0 is " + str(agents_0))
                agents[i] = agents_0[i-1]
                agents = functions.sorted_dict(agents)
                if agents[i] != agents_0[i]:
                    move_counter = move_counter + 1



    def chain_agents_up(root):
        global move_counter
        global agents
        agents_0 = agents.copy()
        ###last of the chain
        if agents_0[len(agents_0) - 1] != root:
            print("agents0 is " + str(agents_0))
            p_last = nx.shortest_path(T_original, agents_0[len(agents_0) - 1], root)
            agents[len(agents_0) - 1] = p_last[1]
            move_counter = move_counter + 1


        for i in agents:
            if i < len(agents) - 1:
                agents[i] = agents_0[i+1]
                if agents[i] != agents_0[i]:
                    move_counter = move_counter + 1




    def agent_replacement(agents, agents_when):
        global move_counter
        agents_0 = agents.copy()
        terminated_agents = []
        for i in agents_when:
            if agents_when[i] > move_counter:
                terminated_agents.append(i)

        for j in terminated_agents:
            for i in agents:
                if i > terminated_agents[j]:
                    agents[i] = agents_0[i-1]
                    if agents[i] != agents_0[i]:
                        move_counter = move_counter + 1

        corrected_ids = agents.copy()
        del corrected_ids[faulty_agent]
        for i in corrected_ids:
            if i >= faulty_agent:
                corrected_ids[i] = agents[i+1]
                del corrected_ids[i+1]
        agents = corrected_ids.copy()











    def decontaminate(T, v, m, T_original, agents_when):
        global previous_node
        global number_of_agents
        global starting_node
        global nr_of_agents
        global move_counter
        global agents
        print("decont v is " + str(v))
        print("decont T is " + str(list(T)))
        previous_agents = agents.copy()


        if previous_node == -1:
            for i in range(nr_of_agents):
                agents[i] = v
            number_of_agents = nr_of_agents
        else:

            print("movecounterb4 " + str(move_counter))
            chain_agents_down(starting_node, v)
            print("movecounterafter " + str(move_counter))

        print("moving the chain to " + str(v))
        functions.color_sync(T_original, agents, previous_agents, color, m)
        print("agents are " + str(agents))
        print("color is " + str(color))
        print("previous node is " + str(previous_node))
        ##breakdown handling
        ### agent replacement
        previous_agents = agents.copy()
        agents_0 = agents.copy()
        terminated_agents = []
        #breakdown happens, instead of removing broken down agent, their position is -1 (which is practically removing from the tree)
        for i in agents_when:
            if agents_when[i] < move_counter:
                print("the move counter became " + str(move_counter) + "so termination list is online, btw agents_when[i] is  " + str(agents_when[i]))
                terminated_agents.append(i)
                agents[i] = -1
        functions.color_sync(T_original, agents, previous_agents, color, m)
        # until we have handled all breakdowns
        while len(terminated_agents) > 0:
            print("while loop started")
            terminated_agents.sort()
            previous_agents = agents.copy()
            #moving all agents in the chain above the furthest down breakdown by one
            root_counter = 0
            for i in agents:
                if i > terminated_agents[0] and i not in terminated_agents and root_counter < 1:
                    print("soooo i is " + str(i) + " the whole of terminated agents are " + str(terminated_agents) + " and the terminated agent[0] is " + str(terminated_agents[0]) +  " agents is " + str(agents) + " agents_0 is " + str(agents_0))
                    if agents[i] == starting_node:
                        root_counter = root_counter + 1
                    if agents_0[i-1] != -1:
                        agents[i] = agents_0[i-1]
                    elif agents_0[i] != -1:
                        path_to_v = nx.shortest_path(T_original, agents[i], v)
                        agents[i] = path_to_v[1]
                    if agents[i] != agents_0[i]:
                        move_counter = move_counter + 1
            #now we eliminate the replaced agent and change the id-s
            corrected_ids = agents.copy()
            print("type of agents is " + str(type(agents)))
            print("type of corrected_ids is " + str(type(corrected_ids)))
            print("corrid b4 del: " + str(corrected_ids))
            del corrected_ids[terminated_agents[0]] # we deleted the broken down
            print("type of corrected_ids after del is " + str(type(corrected_ids)))
            print("corrid after del: " + str(corrected_ids))
            correcting_ids = corrected_ids.copy()
            for i in correcting_ids.keys():
                if i > terminated_agents[0]:
                    print("b4crit" + str(corrected_ids), flush = True)
                    value_of_change = corrected_ids[i]
                    del corrected_ids[i]
                    corrected_ids[i-1] = value_of_change #replace the missing one with the next one?
                    corrected_ids = functions.sorted_dict(corrected_ids)
                    print("aftercrit" + str(corrected_ids), flush = True)
                    #corrected_ids = functions.sort_dict(corrected_ids)


            agents = corrected_ids.copy() # ids and positions are correct
            print("termb4 " + str(terminated_agents))
            del agents_when[terminated_agents[0]] #delete the handled broken down from agents when
            terminated_agents.pop(0)  # delete the handled broken down agent
            if len(terminated_agents) != 0:
                for i in range(len(terminated_agents)):
                    if terminated_agents[i] > 0 and terminated_agents[i] -1 not in terminated_agents:
                        terminated_agents[i] = terminated_agents[i] - 1 #adjust the termination list id too
                functions.color_sync(T_original, agents, previous_agents, color, m)
            print("terma5 " + str(terminated_agents))
            print("agentswhenb4 adjust " + str(agents_when))
            #adjust the agents_when too:
            agents_when_new = agents_when.copy()
            for i in agents_when.keys():
                if i != 0 and i-1 not in agents_when_new.keys():
                    corrected_ids = functions.sorted_dict(corrected_ids)
                    agents_when_new[i-1] = agents_when[i]
                    del agents_when_new[i]
            agents_when = agents_when_new.copy()
            previous_agents = agents.copy()
            agents_0 = agents.copy()
            # breakdown happens, instead of removing broken down agent, their position is -1 (which is practically removing from the tree)
            for i in agents_when:
                if agents_when[i] > move_counter and i not in terminated_agents:
                    print("termage b4 " + str(terminated_agents))
                    terminated_agents.append(i)
                    print("termage a5 " + str(terminated_agents))
                    agents[i] = -1
            functions.color_sync(T_original, agents, previous_agents, color, m)
            print("agents after breakdown handle is " + str(agents) + " terminated_agents iiiis " + str(terminated_agents))
            print("agentswhenafter chaindown is " + str(agents_when))





        print("agents 1 is " + str(agents))
        print("len(list(T.nodes)) is " + (str(len(list(T.nodes)))))
        ## if there are more than one node which is equivalent with being in a leaf
        if len(list(T.nodes)) > 1:
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
            print("agents 2 is " + str(agents))
            for neighbor in reversed(ordered_v_neighbours):
                print("ordered_v_neighbours is " + str(ordered_v_neighbours))
                previous_node = v
                print("agents 3 is " + str(agents))
                #####################################halftime
                agents_when = decontaminate(subtree(T, neighbor, v), neighbor, m, T_original, agents_when)
                #####################################halftime
                print("agents 4 is " + str(agents))
                previous_agents = agents.copy()
                howmany = 0
                print("before moving back, the current value of neighbor is " + str(neighbor))
                chain_agents_up(starting_node)
                print("we were in a leaf, now we're moving back up the chain from" + str(neighbor) + " to " + str(v))
                functions.color_sync(T_original, agents, previous_agents, color, m)
                print("agents 5 is " + str(agents))



                print("agents are " + str(agents))
                print("color is " + str(color))
                print("previous node is " + str(previous_node))

                ##breakdown handling
                ### agent replacement
                previous_agents = agents.copy()
                agents_0 = agents.copy()
                terminated_agents = []
                # breakdown happens, instead of removing broken down agent, their position is -1 (which is practically removing from the tree)
                for i in agents_when:
                    if agents_when[i] < move_counter:
                        print("the move counter became " + str(
                            move_counter) + "so termination list is online, btw agents_when[i] is  " + str(
                            agents_when[i]))
                        terminated_agents.append(i)
                        agents[i] = -1
                functions.color_sync(T_original, agents, previous_agents, color, m)
                # until we have handled all breakdowns
                while len(terminated_agents) > 0:
                    print("while loop started")
                    previous_agents = agents.copy()
                    terminated_agents.sort()
                    # moving all agents in the chain above the furthest down breakdown by one
                    root_counter = 0
                    for i in agents:
                        if i > terminated_agents[0] and i not in terminated_agents and root_counter < 1:
                            print("soooo i is " + str(i) + " the whole of terminated agents are " + str(
                                terminated_agents) + " and the terminated agent[0] is " + str(
                                terminated_agents[0]) + " agents is " + str(agents) + " agents_0 is " + str(agents_0))
                            if agents[i] == starting_node:
                                root_counter = root_counter + 1
                            if agents_0[i - 1] != -1:
                                agents[i] = agents_0[i - 1]
                            elif agents_0[i] != -1:
                                path_to_v = nx.shortest_path(T_original, agents[i], v)
                                agents[i] = path_to_v[1]
                            if agents[i] != agents_0[i]:
                                move_counter = move_counter + 1
                    # now we eliminate the replaced agent and change the id-s
                    corrected_ids = agents.copy()
                    print("type of agents is " + str(type(agents)))
                    print("type of corrected_ids is " + str(type(corrected_ids)))
                    print("corrid b4 del: " + str(corrected_ids))
                    del corrected_ids[terminated_agents[0]]  # we deleted the broken down
                    print("type of corrected_ids after del is " + str(type(corrected_ids)))
                    print("corrid after del: " + str(corrected_ids))
                    correcting_ids = corrected_ids.copy()
                    for i in correcting_ids.keys():
                        if i > terminated_agents[0]:
                            print("b4crit" + str(corrected_ids), flush=True)
                            value_of_change = corrected_ids[i]
                            del corrected_ids[i]
                            corrected_ids[i - 1] = value_of_change  # replace the missing one with the next one?
                            corrected_ids = functions.sorted_dict(corrected_ids)
                            print("aftercrit" + str(corrected_ids), flush=True)
                            # corrected_ids = functions.sort_dict(corrected_ids)

                    agents = corrected_ids.copy()  # ids and positions are correct
                    print("termb4 " + str(terminated_agents))
                    del agents_when[terminated_agents[0]]  # delete the handled broken down from agents when
                    terminated_agents.pop(0)  # delete the handled broken down agent
                    if len(terminated_agents) != 0:
                        for i in range(len(terminated_agents)):
                            if terminated_agents[i] > 0 and terminated_agents[i] -1 not in terminated_agents:
                                terminated_agents[i] = terminated_agents[i] - 1  # adjust the termination list id too
                        functions.color_sync(T_original, agents, previous_agents, color, m)
                    print("terma5 " + str(terminated_agents))
                    print("agentswhenb4 adjust " + str(agents_when))
                    # adjust the agents_when too:
                    agents_when_new = agents_when.copy()
                    for i in agents_when.keys():
                        if i != 0 and i-1 not in agents_when_new.keys():
                            corrected_ids = functions.sorted_dict(corrected_ids)
                            agents_when_new[i - 1] = agents_when[i]
                            del agents_when_new[i]
                    agents_when = agents_when_new.copy()
                    previous_agents = agents.copy()
                    agents_0 = agents.copy()
                    # breakdown happens, instead of removing broken down agent, their position is -1 (which is practically removing from the tree)
                    for i in agents_when:
                        if agents_when[i] > move_counter and i not in terminated_agents:
                            print("termage b4 " + str(terminated_agents))
                            terminated_agents.append(i)
                            print("termage a5 " + str(terminated_agents))
                            agents[i] = -1
                    functions.color_sync(T_original, agents, previous_agents, color, m)
                    print("agents after breakdown handle is " + str(agents) + " terminated_agents iiiis " + str(
                        terminated_agents))
                    print("agentswhenafter chaindown is " + str(agents_when))

        else:
            print("we have reached a leaf")
        return agents_when
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
    min_a = [k for k, v in a_try.items() if v == minval]
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
    minimum_mu = [k for k, v in min_mu.items() if v == minval]
    print("minimum_mu value is: " + str(minval))
    print("minimum_mu is " +str(minimum_mu))

    def optimaltreedecontamination(T, m, T_original, p):
        global agents
        global starting_node
        global nr_of_agents
        agents_if = {}
        agents_when = {}

        '''for i in range(nr_of_agents):
            agents_if[i] = uniform(0, 1)
            print("agents_if is " + str(agents_if))



        for i in range(nr_of_agents):
            if agents_if[i] < p:
                agents_when[i] = randrange(1, 2 * T_original.size())'''
        agents_when[0] = 1
        agents_when[2] = 14


        for key in  agents_when:
            if key - 1 in agents_when.keys():
                print("two neighbouring agents are faulty, exit")
                sys.exit()

        print("agents_when at the start is " + str(agents_when))


        agents_when = decontaminate(T, starting_node, m, T_original, agents_when)
    #calculating the starting_node (where the longest shortest paths for other nodes is the minima for the same value for all other nodes
    # and the nr_of agents needed
    ###
    ##
    #
    print(T)
    starting_node, nr_of_agents = homebase_node(T)
    if nr_a != -1:
        nr_of_agents = nr_a
    print("starting node is " + str(starting_node) + "and the nr_of_agents are " + str(nr_of_agents))


    optimaltreedecontamination(T, m, T_original, p)
    #
    ##
    ###
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
    print("move counted is " + str(move_counter))

    end_time = time.time() - start_time
    return(number_of_agents, move_counted, end_time)


#lr = [1, 7, 5, 7, 7, 1]
'''
rtree = nx.random_tree(n=20, seed=0)
A = nx.balanced_tree(3, 3)
lr = nx.to_prufer_sequence(A)
print("lr is " + str(lr))


print(tree(lr, 1))'''