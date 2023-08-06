import os
import sys
from feyn import QLattice

def test_update():
    good=0
    simple=0
    runs = 30
    steps = 4
    for _ in range(runs):
        lt = QLattice()
        lt.reset()


        registers = ["age","smoker","insurable", "a", "b", "c", "d"]

        qgraph = lt.get_classifier(registers, "insurable", max_depth=steps)

        the_graph = None
        for g in qgraph._graphs:
            if len(g)>5 and g.edge_count>8:
                the_graph = g
                break


        if the_graph:
            lt.update(the_graph)
            new_qgraph = lt.get_classifier(registers, "insurable", max_depth=steps)

            if the_graph in new_qgraph._graphs:
                good+=1
                print("+", end="")
            else:
                print("-", end="")
        else:
            print("s", end="")
            simple +=1
        sys.stdout.flush()

    print("\nGood %i, Simple: %i, Bad: %i"%(good, simple, runs-good-simple))

test_update()
