import operator
from graph import Graph
from collections import deque
import random
from math import log

#TODO: ❗
# generowanie sąsiadów – wierzchołki mogą się powtarzać
# ustalenie parametrów
# warunek stopu = 2 min.
# po upłynięciu czasu ulepsza rozwiązanie, w miejscu konfliktów stosując greedy, żeby było poprawne

#IDEA: 🤔
# rozw. zachłanne – wszystkie nieparzyste kolory np parzystym odpowiednikiem o 1 mniejszym v  wszystkie kolory powyżej x/2 zastąpić losowymi
# zacząć od 1000 kolorów i zmniejszać ilość, odrzucając po 1


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

    def __str__(self):
        return str(self.value)


class Tabu:
    def __init__(self, graph: Graph):
        graph.graph_coloring_greedy()
        self.colors_number = int(graph.colors/2)
        self.graph = graph
        self.size = graph.size
        self.neighbours_number = 30 if self.size >= 30 else self.size
        self.list_of_edges = graph.list_of_edges_pairs()
        self.max_number_of_iterations = int(len(self.list_of_edges))
            # int(50*log(len(self.list_of_edges), 2))  # zależy od rozmiaru i nasycenia grafu
        print(self.max_number_of_iterations)
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
            if solution.value < self.best_value:
                return False
            return True
        else:
            return False

    def main(self) -> list:
        number_of_iterations = 0
        while True:
            for i in range(self.max_number_of_iterations):
                if number_of_iterations % 3 == 0:
                    neighbours = self.generate_neighbours()
                    neighbours.sort(key=operator.attrgetter('value'))
                for neighbour in neighbours:
                    if not self.is_in_tabu(neighbour):
                        neighbour.coloring_from_move(self.current_solution, neighbour.move)
                        self.tabu.append(neighbour.move)  # automatycznie usuwa 0. el., jak przekroczy długość kolejki
                        # print(self.current_solution.value - neighbour.value)
                        self.current_solution = neighbour
                        self.best_value = min(self.current_solution.value, self.best_value)
                        break
                # zakładamy, że w końcu coś znalazł
                if self.current_solution.value == 0:
                    # print(self.current_solution.coloring, self.current_solution.value, self.colors_number)
                    print("ilość iteracji:", number_of_iterations)
                    return [self.current_solution.coloring, self.colors_number]
                number_of_iterations += 1

            self.colors_number += 1
            # print(self.colors_number, self.best_value)
