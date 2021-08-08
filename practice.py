import networkx as nx
import matplotlib.pyplot as plt

def create_grid_3d(dimensions, isperioidic, m):
    print(dimensions)

    #if dim2 < dim1 or dim3 < dim2:
    #    print("dimensions must be in monotonic increasing sequence")
    #    exit()

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

    #nx.draw(C)
    #plt.show()

# grid_graph takes a list of dimensions as its input
# for some reason dimensions are in reverse order
# so the first item of the list will be the nth dimension
dimensions = [3, 2, 1]

create_grid_3d(dimensions, False, 2)