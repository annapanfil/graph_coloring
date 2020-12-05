import operator
from graph import Graph
from collections import deque
import random


#TODO:
# ustalenie parametrów
# warunki akceptowania ruchów tabu

class Solution:
    def __init__(self, list_of_edges: list, parent, move=(None, None)):
        self.move = move
        if move == (None, None):
            self.coloring = parent
        else:
            self.coloring_from_move(parent, move)
        self.value = self.objective_function(list_of_edges)

    def coloring_from_move(self, parent, move):  # parent: Solution
        self.coloring = parent.coloring.copy()
        self.coloring[move[0]] = move[1]

    def objective_function(self, list_of_edges) -> int:
        conflicts = 0
        for edge in list_of_edges:
            if self.coloring[edge[0]] == self.coloring[edge[1]]:
                conflicts += 1
        return conflicts


class Tabu:
    def __init__(self, graph: Graph):
        self.colors_number = 3
        self.graph = graph
        self.size = graph.size
        self.neighbours_number = 20 if self.size >= 20 else self.size
        self.list_of_edges = graph.list_of_edges_pairs()
        self.max_number_of_iterations = len(self.list_of_edges)  # zależy od rozmiaru i nasycenia grafu
        self.tabu = deque([], maxlen=7)  # długość zależy od rozmiaru i nasycenia grafu
        self.current_solution = Solution(self.list_of_edges, [random.randint(0, self.colors_number-1) for _ in range(self.size)])
        self.best_value = 10000000000

    def generate_neighbours(self) -> list:  # obiekty Solution
        neighbours = []
        vertexes_to_try = {i for i in range(self.size)}
        for _ in range(self.neighbours_number):
            # losuj wierzchołek i kolor tak, żeby uniknąć powtórzeń
            vertex = random.choice(tuple(vertexes_to_try))
            vertexes_to_try.remove(vertex)  #QUESTION: czy wierzchołki powinien powtarzać?

            color = random.randint(0, self.colors_number-1)
            while color == self.current_solution.coloring[vertex]:
                color = random.randint(0, self.colors_number-1)

            new_neighbour = Solution(self.list_of_edges, self.current_solution, (vertex, color))
            neighbours.append(new_neighbour)

        return neighbours

    def is_in_tabu(self, solution) -> bool:
        #TODO: warunki akceptowania ruchów tabu
        if solution.move in self.tabu:
            if solution.value == 0:
                return False
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
                    print(self.current_solution.coloring, self.current_solution.value, self.colors_number)
                    return [self.current_solution.coloring, self.colors_number]

            self.colors_number += 1
