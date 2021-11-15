import networkx as nx
import matplotlib.pyplot as plt

#perfectly balanced r-ary tree with h height
A = nx.balanced_tree(3, 3)
lr = nx.to_prufer_sequence(A)
print("lr is " + str(lr))

B = nx.binomial_tree(5)

C = nx.full_rary_tree(3, 13)

#nx.draw(C)
#plt.show()

Adict = {1: 0, 2:10, 5: 4, 3:1}
print(Adict)

adict_items= Adict.items()
sorted = sorted(adict_items)
print(sorted)