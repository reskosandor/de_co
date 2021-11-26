import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict
import functions

#perfectly balanced r-ary tree with h height
A = nx.balanced_tree(3, 3)
lr = nx.to_prufer_sequence(A)
print("lr is " + str(lr))

B = nx.binomial_tree(5)

C = nx.full_rary_tree(3, 13)

#nx.draw(C)
#plt.show()

d = {1: 0, 2:10, 5: 4, 3:1}
print(d)

s = sorted(d.items())
print(s)
print(type(s))
print("iwashere")
sorted = sorted(s)
print(sorted)
print(type(sorted))
di = dict(sorted)


print(di)
print(type(di))

print("b4 " + str(d))
print("a5 " + str(functions.sorted_dict(d)))


tryme = {'a': 1, 'b': 2, 'c': 3}

answer = functions.key_by_value(2, tryme)
print(answer)

