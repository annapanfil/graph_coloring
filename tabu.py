import operator
from graph import Graph
from collections import deque
import random
from math import ceil, floor


class Solution:
    def __init__(self, incidence_list: list, coloring: list, move: tuple, delta_value=None):
        self.move = move  # vertex, new_color    #QUESTION: A może to rozbić na 2?
        self.delta_value = delta_value if delta_value != None else self.delta_objective_function(incidence_list, coloring)

    def delta_objective_function(self, incidence_list: list, coloring: list) -> int:
        """compute change of conflicts number caused by move"""

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

        return conflicts_new_color-conflicts_old_color # less is better

    def __str__(self):
        return "ruch "+str(self.move)+" Δf "+str(self.delta_value)

    def __eq__(self, other): # !!! not exactly equal
        return self.move == other.move


class Tabu:

    def __init__(self, graph: Graph):
        graph.graph_coloring_greedy()                           # approximate solution
        self.graph = graph
        self.size = graph.size
        # print(graph.size)
        self.list_of_edges = graph.list_of_edges_pairs()
        self.upper_bound = graph.colors                         # can't be worse than greedy

        """Parameters to adjust"""
        self.colors_number = max(int(graph.colors/2), graph.colors - 50) # start colors number; WARNING: it changes max_number_of_iterations
        if self.colors_number < 2: self.colors_number = 2
        self.max_neighbours = min(40, self.size)                # max number of generate neighbour solutions
        self.max_number_of_iterations = 0+800                     # first number of iterations before color changing
        self.tabu_vertexes = deque([], maxlen=ceil(self.size/50+30))                # length of tabu list (in tabu we keep vertexes)
        self.coloring = [random.randint(0, self.colors_number - 1) for _ in range(self.size)]    # start coloring – random
        self.all_conflicts, self.vertex_conflicts = self.objective_function()                    # start conflicts number – to minimize
        self.vertexes_sorted = None                                                              # vertexes sorted by conflicts number
        self.best_value = self.all_conflicts                                                     # best objective function calue as far

        # print("początkowe rozwiązanie:", self.coloring)

    def sort_vertexes_by_conflicts(self) -> list:
        self.vertexes_sorted = list(range(self.size))
        self.vertexes_sorted.sort(reverse=True, key=self.vertex_conflicts.__getitem__)


    def first_not_tabu_vertex(self) -> int:
        for vertex_nr in self.vertexes_sorted:
            if vertex_nr in self.tabu_vertexes: continue
            return vertex_nr
        return None # never happens


    def objective_function(self) -> list:
        """Compute current objective function value"""
        vertexes_conflicts = [0 for _ in range(self.size)]
        conflicts = 0
        for edge in self.list_of_edges:
            if self.coloring[edge[0]] == self.coloring[edge[1]]:
                vertexes_conflicts[edge[0]] += 1
                vertexes_conflicts[edge[1]] += 1
                conflicts += 1
        return conflicts, vertexes_conflicts


    def generate_neighbours(self) -> list:  # list of Solution objects
        """Generate new colors for vertexes with most conflicts"""
        neighbours_tuples = set()
        neighbours = []
        neighbours_left = self.max_neighbours

        # create tuples (vertex, color)
        while neighbours_left > 0:
            vertex_nr = self.first_not_tabu_vertex()
            if vertex_nr == None:  # it shouldn't happen
                print("What have you done?!")
                exit(1)
            colors_for_this_vertex = min(self.colors_number - 1, self.max_neighbours)
            neighbours_left -= colors_for_this_vertex
            for color in random.sample(set(range(self.colors_number)), colors_for_this_vertex):
                if color != self.coloring[vertex_nr]:
                    neighbours_tuples.add((vertex_nr, color))

        # create objects based on tuples
        for move in neighbours_tuples:
            neighbours.append(Solution(self.graph.incidence_list, self.coloring, move))

        return neighbours


    def find_best_color(self, vertex):
        """Find color for vertex, which minimize number of conflicts"""
        min_conflicts = 1000000000
        min_color = self.coloring[vertex]
        min_list_of_conflicting_v = []

        for color in range(self.colors_number):
            list_of_conflicting_v = []
            for close_vertex in self.graph.incidence_list[vertex]:
                if color == self.coloring[close_vertex]:
                    list_of_conflicting_v.append(close_vertex)
            if len(list_of_conflicting_v) < min_conflicts:
                min_conflicts = len(list_of_conflicting_v)
                min_color = color
                min_list_of_conflicting_v = list_of_conflicting_v
                if min_conflicts == 0: break

        # Apply this solution
        solution = Solution(None, None, (vertex, min_color), -(self.vertex_conflicts[vertex]-min_conflicts))
        self.apply_solution(solution)

        return min_list_of_conflicting_v


    def improve_solution(self, vertex):
        """Change number of conflicts in vertex to 0"""
        list_of_conflicting_v = self.find_best_color(vertex)

        # if no color can make it, change neighbours
        for close_vertex in list_of_conflicting_v:
            self.find_best_color(close_vertex)


    def apply_solution(self, solution: Solution):
        """Change color of vertex, conflicts number and best value"""
        vertex = solution.move[0]
        new_color = solution.move[1]
        old_color = self.coloring[vertex]
        self.coloring[vertex] = new_color

        # conflicts
        self.all_conflicts += solution.delta_value
        self.vertex_conflicts[vertex] += solution.delta_value

        for close_vertex in self.graph.incidence_list[vertex]:
            if new_color == self.coloring[close_vertex]:
                self.vertex_conflicts[close_vertex] += 1
            if old_color == self.coloring[close_vertex]:  # if they was in the same color, now they aren't
                self.vertex_conflicts[close_vertex] -= 1


        # self.tabu_vertexes.append(solution.move[0])  # automatycznie usuwa 0. el., jak przekroczy długość kolejki
        self.best_value = min(self.all_conflicts, self.best_value)


    def main(self) -> list:
        # parameters to adjust
        iter_before_improve = ceil(self.size/50) if self.size > 200 else self.max_number_of_iterations
        iter_before_sorting = ceil(self.size/50)

        min_colors = self.colors_number

        while self.colors_number < self.upper_bound:
            for i in range(self.max_number_of_iterations):
                if i % iter_before_sorting == 0:
                    self.sort_vertexes_by_conflicts()
                if i % iter_before_improve == 0:
                    self.improve_solution(self.first_not_tabu_vertex())

                # create neighbours and apply the best
                neighbours = self.generate_neighbours()
                solution = min(neighbours, key=operator.attrgetter('delta_value'))
                if solution.delta_value <= 0:               # accept improvement only
                    self.apply_solution(solution)
                self.tabu_vertexes.append(solution.move[0])  #QUESTION: tu czy w apply?

                if self.all_conflicts == 0:
                    return [self.coloring, self.colors_number]     # end successfully
                    #QUESTION: A może od razu wpisywać do self.graph.coloring?

            self.colors_number += 1
            self.max_number_of_iterations = round(4*(self.colors_number-min_colors)+800)
            # print(self.colors_number, self.best_value)
        # print("Rozwiązanie zachłanne. Najmniejsza liczba konfliktów:", self.best_value)
        return [self.graph.coloring, self.graph.colors]     # hit upper bound, return greedy solution
