import operator
from graph import Graph
from collections import deque
import random


#TODO:
# coloring_from_move – D
# ustalenie parametrów
# warunki akceptowania ruchów tabu
# przypisanie pokolorowania do grafu i wyświetlenie go (ogólnie main)


class Solution:
    def __init__(self, list_of_edges: list, parent, move=(None, None)):  # parent: Solution
        self.move = move
        self.coloring = self.coloring_from_move(parent) if move != (
            None, None) else parent  # taki trick dla 1. rozwiązania, bo nie da się zrobić dwóch konstruktorów...
        self.value = self.objective_function(list_of_edges)

    def coloring_from_move(self, parent) -> list:  # parent: Solution
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
        self.colors_number = 2
        self.max_number_of_iterations = 1000  # zależy od rozmiaru i nasycenia grafu
        self.graph = graph
        self.size = graph.size
        self.list_of_edges = graph.list_of_edges_pairs()
        self.tabu = deque([], maxlen=3) # długość zależy od rozmiaru i nasycenia grafu
        self.current_solution = Solution(self.list_of_edges, [random.randint(0, self.colors_number) for _ in range(self.size)])
        self.best_value = 10000000000

    def generate_neighbours(self, how_many=10) -> list:  # obiekty Solution
        neighbours = []
        vertexes_to_try = {i for i in range(self.size)}
        for _ in range(how_many):
            # losuj wierzchołek i kolor tak, żeby uniknąć powtórzeń
            vertex = random.choice(tuple(vertexes_to_try))
            vertexes_to_try.remove(vertex)  #QUESTION: czy wierzchołki powinien powtarzać?

            color = random.randint(0, self.colors_number)
            while color == self.current_solution.coloring[vertex]:
                color = random.randint(0, self.colors_number)

            new_neighbour = Solution(self.list_of_edges, self.current_solution, (vertex, color))
            neighbours.append(new_neighbour)

        return neighbours

    def is_in_tabu(self, solution) -> bool:
        #TODO: warunki akceptowania ruchów tabu
        if solution.move in self.tabu:
            return True
        else:
            return False

    def main(self) -> list:
        while True:
            for i in range(self.max_number_of_iterations):
                neighbours = self.generate_neighbours()
                neighbours.sort(key=operator.attrgetter('value'))
                for neighbour in neighbours:
                    if not self.is_in_tabu(neighbour):
                        self.tabu.append(neighbour.move)  # automatycznie usuwa 0. el., jak przekroczy długość kolejki
                        self.current_solution = neighbour
                        self.best_value = min(self.current_solution.value, self.best_value)
                        break
                # zakładamy, że w końcu coś znalazł
                if self.current_solution.value == 0:
                    return [self.current_solution.coloring, self.colors_number]

            self.colors_number += 1
