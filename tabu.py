import operator
from graph import Graph
from collections import deque
import random
from math import log

#TODO: ❗
# ustalenie parametrów
# warunek stopu = 2 min.
# po upłynięciu czasu ulepsza rozwiązanie, w miejscu konfliktów stosując greedy, żeby było poprawne

#IDEA: 🤔
# zacząć od 1000 kolorów i zmniejszać ilość, odrzucając po 1


class Solution:
    def __init__(self, incidence_list: list, coloring: list, move: tuple):
        self.move = move
        self.reversed_move = (move[0], coloring[move[0]])
        self.delta_value = self.delta_objective_function(incidence_list, coloring)

    def delta_objective_function(self, incidence_list: list, coloring: list) -> int:
        conflicts_old_color = 0
        conflicts_new_color = 0
        vertex = self.move[0]
        new_color = self.move[1]
        old_color = coloring[vertex]

        for close_vertex in incidence_list[vertex]:
            if old_color == coloring[close_vertex]:
                conflicts_old_color += 1
            if new_color == coloring[close_vertex]:
                conflicts_new_color += 1

        return conflicts_new_color-conflicts_old_color #im mniejsza tym lepiej

    def __str__(self):
        return "ruch "+str(self.move)+" Δf "+str(self.delta_value)

    def __eq__(self, other): #!!! takie nie do końca equal
        return self.move == other.move

class Tabu:

    def __init__(self, graph: Graph):
        graph.graph_coloring_greedy()
        self.upper_bound = graph.colors
        self.colors_number = max(int(graph.colors/2), graph.colors - 10)
        if self.colors_number < 2: self.colors_number = 2
        self.graph = graph
        self.size = graph.size
        self.neighbours_number = 30 if self.size >= 30 else self.size
        self.list_of_edges = graph.list_of_edges_pairs()
        self.max_number_of_iterations = 800
        #self.max_number_of_iterations = int(len(self.list_of_edges)/2)
            # int(50*log(len(self.list_of_edges), 2))  # zależy od rozmiaru i nasycenia grafu
        self.tabu_moves = deque([], maxlen=7)  # długość zależy od rozmiaru i nasycenia grafu
        # self.tabu_vertexes = deque([], maxlen=7)
        self.current_solution = [random.randint(0, self.colors_number-1) for _ in range(self.size)]
        self.all_conflicts, self.vertex_conflicts = self.objective_function()
        self.best_value = 10000000000
        # print("początkowe rozw:", self.current_solution)

    def objective_function(self) -> list:
        vertexes_conflicts = [0 for _ in range(self.size)]
        conflicts = 0
        for edge in self.list_of_edges:
            if self.current_solution[edge[0]] == self.current_solution[edge[1]]:
                vertexes_conflicts[edge[0]] += 1
                vertexes_conflicts[edge[1]] += 1
                conflicts += 1
        # print("konflikty:", conflicts, vertexes_conflicts)
        return conflicts, vertexes_conflicts


    def generate_neighbours(self) -> list:  # obiekty Solution
        # generowanie sąsiadów – jeden wierzchołek może być z kilkoma kolorami
        # generowanie niepowtarzających się ruchów
        neighbours_tuples = set()
        neighbours = []
        neighbours_left = self.neighbours_number
        indexes = [x for x in range(self.size)]
        indexes.sort(reverse = True, key=self.vertex_conflicts.__getitem__)

        for vertex_nr in indexes:
            colors_for_this_vertex = min(self.colors_number-1, self.neighbours_number)
            neighbours_left -= colors_for_this_vertex
            for color in random.sample({c for c in range(self.colors_number)}, colors_for_this_vertex):
                if color != self.current_solution[vertex_nr]:
                    neighbours_tuples.add((vertex_nr, color))
            if neighbours_left <= 0: break

        # stworzenie obiektów na ich podstawie
        for move in neighbours_tuples:
            neighbours.append(Solution(self.graph.incidence_list, self.current_solution, move))

        return neighbours

    def is_in_tabu(self, solution) -> bool:
        if solution.move in self.tabu_moves:
            if (self.all_conflicts + solution.delta_value) < self.best_value:
                return False
            # print("ten ruch jest tabu!")
            return True
        else:
            return False

    def improve_solution(Solution):
        pass

    def apply_solution(self, solution: Solution):
        vertex = solution.move[0]
        new_color = solution.move[1]
        old_color = self.current_solution[vertex]
        self.all_conflicts += solution.delta_value
        # print(self.all_conflicts)
        self.vertex_conflicts[vertex] += solution.delta_value

        for close_vertex in self.graph.incidence_list[vertex]:
            if new_color == self.current_solution[close_vertex]:
                self.vertex_conflicts[close_vertex] += 1
            if old_color == self.current_solution[close_vertex]: #jeżeli wcześniej były takie same, teraz nie są
                self.vertex_conflicts[close_vertex] -= 1

        self.current_solution[vertex] = new_color

    def main(self) -> list:
        number_of_iterations = 0
        while self.colors_number < self.upper_bound:
            for i in range(self.max_number_of_iterations):
                # if number_of_iterations % 3 == 0:
                neighbours = self.generate_neighbours()
                neighbours.sort(key=operator.attrgetter('delta_value'))
                for neighbour in neighbours:
                    if not self.is_in_tabu(neighbour):
                        # print(neighbour)
                        self.apply_solution(neighbour)
                        # print(self.current_solution, "konflikty:", self.all_conflicts, self.vertex_conflicts)
                        self.tabu_moves.append(neighbour.reversed_move)  # automatycznie usuwa 0. el., jak przekroczy długość kolejki
                        neighbours.remove(neighbour)
                        self.best_value = min(self.all_conflicts, self.best_value)
                        break
                # zakładamy, że w końcu coś znalazł
                if self.all_conflicts == 0:
                    # print(self.coloring, self.value, self.colors_number)
                    # print("ilość iteracji:", number_of_iterations)
                    return [self.current_solution, self.colors_number]
                number_of_iterations += 1

            self.colors_number += 1
            # print(self.colors_number, number_of_iterations, self.best_value)
        print("rozwiązanie zachłanne. Najlepsze wygenerowane przez tabu:", self.best_value)
        return [self.graph.coloring, self.graph.colors]
            # print(self.colors_number, self.best_value)
