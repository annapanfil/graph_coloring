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
    def __init__(self, incidence_list: list, coloring: list, move: tuple, delta_value = None):
        self.move = move
        self.reversed_move = (move[0], coloring[move[0]])
        self.delta_value = delta_value if delta_value != None else self.delta_objective_function(incidence_list, coloring)

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
        self.colors_number = max(int(graph.colors/2), graph.colors - 50)
        if self.colors_number < 2: self.colors_number = 2
        self.graph = graph
        self.size = graph.size
        self.neighbours_number = min(40, self.size)
        self.list_of_edges = graph.list_of_edges_pairs()
        self.max_number_of_iterations = 800
        #self.max_number_of_iterations = int(len(self.list_of_edges)/2)
            # int(50*log(len(self.list_of_edges), 2))  # zależy od rozmiaru i nasycenia grafu
        self.tabu_vertexes = deque([], maxlen=7) # długość zależy od rozmiaru i nasycenia grafu
        self.current_solution = [random.randint(0, self.colors_number-1) for _ in range(self.size)]
        self.all_conflicts, self.vertex_conflicts = self.objective_function()
        self.vertexes_sorted = [x for x in range(self.size)]
        self.vertexes_sorted.sort(reverse=True, key=self.vertex_conflicts.__getitem__)
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

        for vertex_nr in self.vertexes_sorted:
            if vertex_nr in self.tabu_vertexes: continue
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

    def find_best_color(self, vertex):
        min_conflicts = 1000000000
        min_color = self.current_solution[vertex]
        min_list_of_conflicting_v = []

        # znalezienie koloru tworzącego najmniejszą liczbę konfliktów
        for color in range(self.colors_number):
            list_of_conflicting_v = []
            for close_vertex in self.graph.incidence_list[vertex]:
                if color == self.current_solution[close_vertex]:
                    list_of_conflicting_v.append(close_vertex)
            if len(list_of_conflicting_v) < min_conflicts:
                min_conflicts = len(list_of_conflicting_v)
                min_color = color
                min_list_of_conflicting_v = list_of_conflicting_v
                if min_conflicts == 0: break

        # zastosuj rozwiązanie
        solution = Solution(None, self.current_solution, (vertex, min_color), -(self.vertex_conflicts[vertex]-min_conflicts))
        self.apply_solution(solution)

        return min_list_of_conflicting_v

    def improve_solution(self, vertex):
        list_of_conflicting_v = self.find_best_color(vertex)
        for close_vertex in list_of_conflicting_v:
            self.find_best_color(close_vertex)


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

        # self.tabu_vertexes.append(solution.move[0]) # automatycznie usuwa 0. el., jak przekroczy długość kolejki
        self.best_value = min(self.all_conflicts, self.best_value)

    def main(self) -> list:
        number_of_iterations = 0
        while self.colors_number < self.upper_bound:
            for i in range(self.max_number_of_iterations):
                if i % 10 == 0:
                    for vertex_nr in self.vertexes_sorted:
                        if vertex_nr in self.tabu_vertexes: continue
                        self.improve_solution(vertex_nr)
                        break
                if i % 10 == 0:
                    self.vertexes_sorted = [x for x in range(self.size)]
                    self.vertexes_sorted.sort(reverse=True, key=self.vertex_conflicts.__getitem__)

                neighbours = self.generate_neighbours()
                solution = min(neighbours, key=operator.attrgetter('delta_value'))
                if solution.delta_value <= 0: # akceptujemy tylko polepszanie
                    self.apply_solution(solution)
                self.tabu_vertexes.append(solution.move[0])

                # zakładamy, że w końcu coś znalazł
                if self.all_conflicts == 0:
                    # print(self.coloring, self.value, self.colors_number)
                    # print("ilość iteracji:", number_of_iterations)
                    # print(self.all_conflicts, self.vertex_conflicts, self.best_value)
                    return [self.current_solution, self.colors_number]
                number_of_iterations += 1

            self.colors_number += 1
            print(self.colors_number, self.best_value)
        print("rozwiązanie zachłanne. Najlepsze wygenerowane przez tabu:", self.best_value)
        return [self.graph.coloring, self.graph.colors]
