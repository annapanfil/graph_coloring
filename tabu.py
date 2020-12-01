from main import Graph
from collections import deque

#TODO:
# generowanie 1. rozwiązania - A
# generate_neighbours - A
# coloring_from_move – D
# is_in_tabu - D
# sort_neighbours_by_value
# usuwanie z listy tabu
# podział na pliki
# ustalenie parametrów


class Solution:
    def __init__(self, move: tuple, parent: Solution, list_of_edges):
        self.move = move
        self.coloring = self.coloring_from_move(parent)
        self.value = self.objective_function(list_of_edges)


    def coloring_from_move(self, parent: Solution) -> list:
        return []

    def objective_function(self, list_of_edges) -> int:
        conflicts = 0
        for edge in list_of_edges:
            if self.coloring[edge[0]] == self.coloring[edge[1]]:
                conflicts += 1
        print(conflicts)
        return conflicts

class Tabu:
    def __init__(self, graph: Graph):
        self.colors_number = 1
        self.max_number_of_iterations = 1000 # zależy od rozmiaru i nasycenia grafu
        self.current_solution
        self.graph = graph
        self.list_of_edges = graph.list_of_edges_pairs()
        self.tabu = deque([])
        self.tabu_tenure = 3  # zależy od rozmiaru i nasycenia grafu
        self.best_value = 10000000000

        self.solution_value = self.objective_function(self.current_solution)

    def generate_neighbours(self, how_many = 10) -> list:   # obiekty Solution
        return []  # wierzchołek 3 ->  kolor 2

    def is_in_tabu(self, solution) -> bool:
        if solution.move in self.tabu:
            return True
        else:
            return False

    def main(self) -> list:
        while True:
            for i in range(self.max_number_of_iterations):
                neighbours = self.generate_neighbours()
                neighbours = sort_neighbours_by_value()
                for neighbour in neighbours:
                    if not self.is_in_tabu(neighbour):
                        self.current_solution = neighbour
                        self.best_value = min(self.current_solution.value, self.best_value)
                        break
                # zakładamy, że w końcu coś znalazł
                if self.current_solution.value == 0:
                    return [self.current_solution.coloring, self.colors_number]

            self.colors_number += 1


if __name__ == '__main__':
    g = Graph()
    g.import_from_file("simple")

    t = Tabu(g)
    t.main()
