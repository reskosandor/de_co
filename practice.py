import csv

import mesh_2d
import mesh_3d
import tomesh_2d
import tomesh_3d


#asd = mesh_2d.create_grid_2d(10, 10, False, 2)
#print("asd is " + str(asd))
#print(type(asd))


header = ["number of agents", "after_init", "move_count"]

example_header = ['name', 'area', 'country_code2', 'country_code3']
example_data = [
    ['Albania', 28748, 'AL', 'ALB'],
    ['Algeria', 2381741, 'DZ', 'DZA'],
    ['American Samoa', 199, 'AS', 'ASM'],
    ['Andorra', 468, 'AD', 'AND'],
    ['Angola', 1246700, 'AO', 'AGO']
]

with open('sim.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    #writer.writerow(header)

    #write multiple rows
    #writer.writerows(example_data)
    writer.writerow('tomesh2d m1')

    for i in range(5):
        dimensions = [i+1, i+1, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 1))

    writer.writerow('tomesh2d m2')

    for i in range(5):
        dimensions = [i+1, i+1, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 2))

    writer.writerow('tomesh2d m3')

    for i in range(5):
        dimensions = [i+1, i+1, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 3))

    writer.writerow('tomesh2d m4')

    for i in range(5):
        dimensions = [i+1, i+1, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 4))

a = 0

def trie(c):
    global a
    a = -5
    c = c+1
    print(c)
    a = 0
    a = a + 10
    print("a is " + str(a))

trie(0)
print("a after f is " + str(a))