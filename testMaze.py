from Maze import *
"""
laby = Maze(4, 4)
print(laby.info())

print(laby)

laby.neighbors = {
    (0, 0): {(1, 0)},
    (0, 1): {(0, 2), (1, 1)},
    (0, 2): {(0, 1), (0, 3)},
    (0, 3): {(0, 2), (1, 3)},
    (1, 0): {(2, 0), (0, 0)},
    (1, 1): {(0, 1), (1, 2)},
    (1, 2): {(1, 1), (2, 2)},
    (1, 3): {(2, 3), (0, 3)},
    (2, 0): {(1, 0), (2, 1), (3, 0)},
    (2, 1): {(2, 0), (2, 2)},
    (2, 2): {(1, 2), (2, 1)},
    (2, 3): {(3, 3), (1, 3)},
    (3, 0): {(3, 1), (2, 0)},
    (3, 1): {(3, 2), (3, 0)},
    (3, 2): {(3, 1)},
    (3, 3): {(2, 3)}
}
print(laby)

laby.neighbors[(1,3)].remove((2,3))
laby.neighbors[(2,3)].remove((1,3))
print(laby)

laby.neighbors[(1, 3)].add((2, 3))
laby.neighbors[(2, 3)].add((1, 3))
print(laby)

laby.neighbors[(1, 3)].remove((2, 3))
print(laby)
print(laby.info())
c1 = (1, 3)
c2 = (2, 3)
if c1 in laby.neighbors[c2] and c2 in laby.neighbors[c1]:
    print(f"Il n'y a pas de mur entre {c1} et {c2} car elles sont mutuellement voisines")
elif c1 not in laby.neighbors[c2] and c2 not in laby.neighbors[c1]:
    print(f"Il y a un mur entre {c1} et {c2} car {c1} n'est pas dans le voisinage de {c2} et {c2} n'est pas dans le voisinage de {c1}")
else:
    print(f"Il y a une incohérence de réciprocité des voisinages de {c1} et {c2}")

laby = Maze(4, 4,True)
print(laby.info())
print(laby)
laby.remove_wall((0,1),(0,2))
print(laby.get_cells())
print(laby.get_walls())
print(laby)
#laby.fill()

print("get_walls")
laby4=Maze(4,4,True)
laby4.add_wall((0, 0), (0, 1))
laby4.add_wall((0, 1), (1, 1))
print(laby4)
print(laby4.get_walls())
print("Fin test get_walls")

print("Test get_contigous_cells")
print(laby.get_contiguous_cells((0,0)))
print(laby.get_contiguous_cells((3,3)))
print(laby.get_contiguous_cells((1,1)))
print("Fin test get_contigous_cells")

print("Test add_wall")
laby.add_wall((0, 0), (0, 1))
laby.add_wall((0, 1), (1, 1))
print(laby)
print("Fin test add_wall ")

print("Test get_reachable_cells")
laby.add_wall((1,0),(0,0))
print(laby)

print(laby.get_walls())
print(laby.get_reachable_cells((0,0)))
print(laby.get_reachable_cells((1,0)))

print("Fin test get_reachable_cells")

print("Test empty")
laby.empty()
print(laby)
print("Fin test empty")

print("Test gen_btree ")
laby2=Maze.gen_btree(4,4)
print(laby2)
print(laby2.info())
print("Fin test gen_btree")

print("Test gen_fusion")
laby3=Maze.gen_fusion(10,10)
print(laby3)
print("Fin test gen_fuison")

print("get_walls")
laby4=Maze(4,4,True)
print(laby4.get_walls())
print(laby4)
"""
print("Test gen_sidewinder(4, 4)")
laby5 = Maze.gen_wilson(4, 4)
print(laby5)
print("Fin Test gen_sidewinder")

print("Test gen_exploration(4, 4)")
laby6 = Maze.gen_exploration(4, 4)
"""
print(laby6)
print("Fin Test gen_exploration")

print("Test gen_wilson")
for i in range(10):
    laby5=Maze.gen_wilson(4,4)
    print(laby5)

print("Fin test gen_wilson")

laby3=Maze.gen_fusion(15,15)
print(laby3)

solution = laby3.solve_dfs((0, 0), (14, 14))
str_solution = {c:'*' for c in solution}
str_solution[( 0,  0)] = 'D'
str_solution[(14, 14)] = 'A'
print(laby3.overlay(str_solution))

solution = laby3.solve_bfs((4, 3), (12, 6))
str_solution = {c:'*' for c in solution}
str_solution[( 4,  3)] = 'D'
str_solution[(12, 6)] = 'A'
print(laby3.overlay(str_solution))

print(laby3.distance_geo((4, 3),(12, 6)))


print("test solve_rhr")
laby6=Maze.gen_fusion(4,4)
#laby6.add_wall((2,0),(2,1))
#laby6.add_wall((2,0),(1,0))
print(laby6)
solution=laby6.solve_rhr((0,0),(3,3))
print(solution)
solution = {c:'*' for c in solution}
solution[( 0,  0)] = 'D'
solution[(14, 14)] = 'A'
print(laby6.overlay(solution))
print("fin solve_rhr")

print("test distance manhattan")
res=laby6.distance_man((0,0),(2,2))
print(res)
"""