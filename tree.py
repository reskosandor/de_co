import networkx as nx
import matplotlib.pyplot as plt
import mesh_2d
import random

def tree(T, m):
    print("asd")
    T = nx.algorithms.tree.coding.from_prufer_sequence(lr)
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

    def alpha(v, T, m):
        print("v is....")
        print(v, flush=True)
        print(type(v), flush=True)
        print(T, flush=True)
        print(type(T))
        print("T consists of nodes:")
        print(list(T))
        print("v degree is...")
        print(T.degree[v])
        #print(type(T.degree[v]))
        #print(T.degree[v], flush=True)
        if T.degree[v] == 0:
        #if degree(T, v) == 0:
            print(T.degree[v], flush=True)
            print("branch 1")
            print("returning 1")
            return 1
        elif 0 < T.degree[v] <= m:
            print("branch 2")
            value = alpha(neighbors_of_v(T, v)[0], subtree(T, neighbors_of_v(T, v)[0], v), m)
            print("returning " + str(value), flush=True)
            return value
        elif T.degree[v] > m and alpha(neighbors_of_v(T, v)[0], subtree(T, neighbors_of_v(T, v)[0], v), m) > alpha(neighbors_of_v(T, v)[m], subtree(T, neighbors_of_v(T, v)[m], v), m):
            print("branch 3")
            value = alpha(neighbors_of_v(T, v)[0], subtree(T, neighbors_of_v(T, v)[0], v), m)
            print("returning " + str(value), flush=True)
            return value
        elif T.degree[v] > m and alpha(neighbors_of_v(T, v)[0], subtree(T, neighbors_of_v(T, v)[0], v), m) == alpha(neighbors_of_v(T, v)[m], subtree(T, neighbors_of_v(T, v)[m], v), m):
            print("branch 4")
            value = alpha(neighbors_of_v(T, v)[0], subtree(T, neighbors_of_v(T, v)[0], v), m) + 1
            print("returning " + str(value), flush=True)
            return value

    a = {}

    print("calculating a...")
    for node in list(T):
        print(T.degree[node])
    print("type", flush=True)
    print(subtree(T, 0, 1))
    print(subtree(T, 0, 1).degree[0], flush=True)
    print("typends", flush=True)
    print(subtree(T, neighbors_of_v(T, 1)[0], 1))

    print(T.edges())
    for node in list(T):
        a[node] = (alpha(node, T, m))
        print("appended value for node " + str(node) + " is: " + str(a[node]))
    print(a)







    #T.remove_edge(1, 7)
    #nx.draw(T, with_labels=True)

    #print(nx.algorithms.descendants(T, 5))
    #T.remove_node(4)
    #print(nx.algorithms.descendants(T, 5))
    #nx.draw(subtree(T, 7, 1))
    #nx.draw(T)
    #plt.show()









#mylist = list(range(10))

#print(mylist)
#random.shuffle(mylist)
#print(mylist)
#lr = random.sample(mylist, len(mylist))
#print(lr)
lr = [1, 7, 5, 7, 7, 1]
#lr = [1]

tree(lr, 2)