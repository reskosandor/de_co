import csv
import networkx as nx
import mesh_2d
import mesh_3d
import tomesh_2d
import tomesh_3d
import tree
import tree_1_error
import tree_chain
import mesh_2d_1_error
import mesh_3d_1_error
import tomesh_2d_1_error
import tomesh_3d_1_error

with open('sim.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    #write multiple rows into sim.csv
    writer.writerow('mesh2d_m1')
    for i in range(19):
        writer.writerow(mesh_2d.create_grid_2d(i+2, i+2, 2))

    #write a single row into sim.csv
    '''writer.writerow
    writer.writerow(mesh_2d.create_grid_2d(4, 4, 1))'''

    #simulation examples
    '''dimensions = [6, 6, 6]
    mesh_2d.create_grid_2d(6, 6, 1)
    mesh_2d.create_grid_2d(6, 6, 2)
    mesh_3d.create_grid_3d(dimensions, 1)
    mesh_3d.create_grid_3d(dimensions, 2)
    mesh_3d.create_grid_3d(dimensions, 3)
    tomesh_2d.create_grid_2d(6, 6, 1)
    tomesh_2d.create_grid_2d(6, 6, 2)
    tomesh_3d.create_grid_3d(dimensions, 1)
    tomesh_3d.create_grid_3d(dimensions, 2)
    tomesh_3d.create_grid_3d(dimensions, 3)
    tomesh_3d.create_grid_3d(dimensions, 4)
    mesh_2d_1_error.create_grid_2d(6, 6, 1)
    mesh_2d_1_error.create_grid_2d(6, 6, 2)
    mesh_3d_1_error.create_grid_3d(dimensions, 1)
    mesh_3d_1_error.create_grid_3d(dimensions, 2)
    mesh_3d_1_error.create_grid_3d(dimensions, 3)
    tomesh_2d_1_error.create_grid_2d(6, 6, 1)
    tomesh_2d_1_error.create_grid_2d(6, 6, 2)
    tomesh_3d_1_error.create_grid_3d(dimensions, 1)
    tomesh_3d_1_error.create_grid_3d(dimensions, 2)
    tomesh_3d_1_error.create_grid_3d(dimensions, 3)
    tomesh_3d_1_error.create_grid_3d(dimensions, 4)'''
    #prufer sequence of test 1 in trees
    #lr = [0, 0, 0, 0]
    #prufer sequence of test 2 in trees
    #lr = [0, 0, 0, 0, 1, 1, 1, 1]
    #prufer sequence of test 3 in trees
    #lr = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 7, 7, 7, 7, 12, 12, 12, 16, 16]
    #prufer sequence of full binary graph, h=5
    #lr = [15, 15, 7, 16, 16, 7, 3, 17, 17, 8, 18, 18, 8, 3, 1, 19, 19, 9, 20, 20, 9, 4, 21, 21, 10, 22, 22, 10, 4, 1, 0, 2, 23, 23, 11, 24, 24, 11, 5, 25, 25, 12, 26, 26, 12, 5, 2, 6, 27, 27, 13, 28, 28, 13, 6, 14, 29, 29, 14, 30, 30]
    #prufer sequence of full 4-ary graph, h=3
    #lr = [5, 5, 5, 5, 1, 6, 6, 6, 6, 1, 7, 7, 7, 7, 1, 8, 8, 8, 8, 1, 0, 9, 9, 9, 9, 2, 10, 10, 10, 10, 2, 11, 11, 11, 11, 2, 12, 12, 12, 12, 2, 0, 13, 13, 13, 13, 3, 14, 14, 14, 14, 3, 15, 15, 15, 15, 3, 16, 16, 16, 16, 3, 0, 4, 17, 17, 17, 17, 4, 18, 18, 18, 18, 4, 19, 19, 19, 19, 4, 20, 20, 20, 20]
    #tree.tree(lr, 1)
    #tree_1_error.tree(lr, 1)
    #tree_chain.tree(lr, 0.1)

