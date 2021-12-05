import csv
import networkx as nx

import mesh_2d
import mesh_3d
import tomesh_2d
import tomesh_3d
import tree
import tree_1_fault
import tree_chain
import mesh_2d_1_error
import mesh_3d_1_error
import tomesh_2d_1_error
import tomesh_3d_1_error

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
    '''writer.writerow('mesh2d m1')
    for i in range(20):
        writer.writerow(mesh_2d.create_grid_2d(i+1, i+1, False, 1))
    writer.writerow('mesh2d m2')
    for i in range(20):
        writer.writerow(mesh_2d.create_grid_2d(i+1, i+1, False, 2))
    writer.writerow("mesh3d m1")
    for i in range(20):
        dimensions = [i+1, i+1, i+1]
        writer.writerow(mesh_3d.create_grid_3d(dimensions, False, 1))'''
    '''writer.writerow("mesh3d m2")
    for i in range(20):
        dimensions = [i + 1, i + 1, i + 1]
        writer.writerow(mesh_3d.create_grid_3d(dimensions, False, 2))'''
    '''writer.writerow("mesh3d m3")
    for i in range(20):
        dimensions = [i + 1, i + 1, i + 1]
        writer.writerow(mesh_3d.create_grid_3d(dimensions, False, 3))
    writer.writerow('tomesh2d m1')
    for i in range(20):
        writer.writerow(tomesh_2d.create_grid_2d(i+1, i+1, True, 1))
    writer.writerow('tomesh2d m2')
    for i in range(20):
        writer.writerow(tomesh_2d.create_grid_2d(i+1, i+1, True, 2))'''
    '''writer.writerow('tomesh3d m1')
    for i in range(20):
        dimensions = [i+1, i+1, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 1))'''
    '''writer.writerow('tomesh3d m2')'''
    '''for i in range(20):
        dimensions = [i+1, i+1, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 2))'''
    '''writer.writerow('tomesh3d m3')
    for i in range(20):
        dimensions = [i+1, i+1, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 3))
    writer.writerow('tomesh3d m4')
    for i in range(20):
        dimensions = [i+1, i+1, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 4))'''

    
    '''writer.writerow('mesh3d m1 n2_20')
    for i in range(20):
        dimensions = [20, 20, i+1]
        writer.writerow(mesh_3d.create_grid_3d(dimensions, False, 1))'''


    '''
    writer.writerow('tree')
    A = nx.balanced_tree(3, 3)
    lr = nx.to_prufer_sequence(A)
    writer.writerow(tree.tree(lr, 1))'''


    '''print("asd")
    for r in range(5):
        for h in range(5):
            for m in range(r):
                print("are we here?")
                example_data = [r+1, h+1, m+1]
                writer.writerow(example_data)

                A = nx.balanced_tree(r+1, h+1)
                lr = nx.to_prufer_sequence(A)
                writer.writerow(tree.tree(lr, m+1))'''

    '''for m in range(3):
        for i in range(4, 22):
            example_data = [3, i, m + 1]
            writer.writerow(example_data)
            A = C = nx.full_rary_tree(3, i)
            lr = nx.to_prufer_sequence(A)
            writer.writerow(tree_chain.tree(lr, m + 1, 0.1))'''

    '''
    print("start simming")
    example_data = [3, 3, 3]
    print(example_data)
    A = nx.balanced_tree(3, 3)
    #lr = nx.to_prufer_sequence(A)
    lr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(tree_chain.tree(lr, 1, 0.3))
    '''
    '''#print(mesh_2d_1_error.create_grid_2d(10, 10, False, 2))'''
    '''dimensions = [6, 6, 6]
    print(mesh_2d.create_grid_2d(6, 6, False, 1))'''

    '''lr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(tree_chain.tree(lr, 1, 0.3))'''
    '''dimensions = [6, 6, 6]
    print(tomesh_2d.create_grid_2d(6, 6, False, 1))'''

    '''lr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(tree_1_fault.tree(lr, 1))'''
    '''dimensions = [6, 6, 6]
    tomesh_3d_1_error.create_grid_3d(dimensions, True, 2)'''

    '''dimensions = [10, 10, 10]
    tomesh_3d.create_grid_3d(dimensions, True, 2)'''

    '''writer.writerow('tomesh3d m1')
    for i in range(10):
        dimensions = [10, 10, i+1]
        print("when writing to csv, i is " + str(i+1), flush=True)
        writer.writerow(tomesh_3d.create_grid_3d(dimensions, True, 1))'''
    '''dimensions = [6, 6, 6]
    mesh_3d_1_error.create_grid_3d(dimensions, False, 1)'''
    '''mesh_2d_1_error.create_grid_2d(6, 6, False, 1)'''
    tomesh_2d_1_error.create_grid_2d(6, 6, True, 1)

