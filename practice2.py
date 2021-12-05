import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict
import functions
import sys
import tree_chain
import math
'''
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

'''
'''
a = 2

def bc(a):
    if a == 1:
        sys.exit()
    return a

b = bc(a)
print(b)'''


'''def roots_of_equation(a, b, c):
    # Finding the value of Discriminant
    D = b * b - 4 * a * c
    # other way, D = b**2 - 4*a*c

    sqrt_D = math.sqrt(abs(D))

    # checking Discriminant condition
    if D > 0:
        print("Roots are Real and Different ")
        print((-b + sqrt_D) / (2 * a))
        print((-b - sqrt_D) / (2 * a))

    elif D == 0:
        print(" real and same roots")
        print(-b / (2 * a))

        # Discriminant < 0 follows else block

    else:
        print("Complex Roots")
        print(- b / (2 * a), " + i", sqrt_D)
        print(- b / (2 * a), " - i", sqrt_D)

    return (-b + sqrt_D) / (2 * a), (-b - sqrt_D) / (2 * a)

h = 6
p = 0.3


a = h - h * p
b =  -2 * math.log(p ** p) * (1 - p)
c = 2 * math.log(p ** p) * (1 - p)

x1, x2 = roots_of_equation(a, b ,c)

k1 = h / ((1 - x1) * (1 - p))
k2 = h / ((1 - x2) * (1 - p))


print(k1)
print(k2)'''

'''G = nx.Graph()
G.add_edge(0, 1)
G.add_edge(0, 2)
G.add_edge(0, 3)
G.add_edge(1, 4)
G.add_edge(1, 5)
G.add_edge(1, 6)
G.add_edge(4, 7)
G.add_edge(4, 8)
G.add_edge(4, 9)'''

# agents increase by one, but move counter stays the same, because one agent needs to stay at the root
'''G= nx.Graph()
G.add_edge(0, 1)
G.add_edge(0, 2)
G.add_edge(0, 3)
G.add_edge(0, 4)
G.add_edge(0, 5)'''



lr = nx.to_prufer_sequence(G)
print(lr)
for i in range(len(lr)):
    lr[i] = lr[i] + 1
print(lr)


