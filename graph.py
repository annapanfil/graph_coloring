import random
from math import floor
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re


class Graph:
    def __init__(self):  # rozmiar = random.randint(3,7) - drugi arg
        self.name = "bez nazwy"
        self.size = 0  # ile wierzchołków w grafie
        self.colors = 1  # ile kolorów jest użytychjak na razie
        self.incidence_list = []  # każda podlista to zbiór sąsiadów danego wierzchołka
        self.coloring = []  # = [0 for _ in range(self.rozmiar)]   # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza, że wierzchołek jest jeszcze nie pokolorowany

    def generate_graph_r(self, size: int, edges: int):
        # GENERATOR GRAFÓW losowych

        # miesza wierzchołki, żeby rozkład był bardziej losowy
        vertexes = [i for i in range(size)]
        random.shuffle(vertexes)
        repeat = False

        while edges > 0:
            for vertex_no in range(len(vertexes)):
                v0 = vertexes[vertex_no]
                # bierzemy pod uwagę tylko "późniejsze" wierzchołki, których jeszcze nie ma w liście incydencji
                possible_v1 = vertexes[vertex_no+1:]
                if repeat: possible_v1 = [x for x in possible_v1 if x not in self.incidence_list[v0]]
                random.shuffle(possible_v1)

                edges_from_v = random.randint(0, len(possible_v1))

                for i in range(edges_from_v):
                    # dodanie wierzchołków do listy incydencji
                    v1 = possible_v1[i]
                    self.incidence_list[v0].append(v1)
                    self.incidence_list[v1].append(v0)
                    edges -= 1
                    if edges == 0:
                        return 0  # kończy, gdy wykorzystał wszystkie krawędzie
            repeat = True

    def generate_graph_c(self, size: int, edges: int):
        # GENERATOR GRAFÓW zagęszczonych

        # miesza wierzchołki, żeby rozkład był bardziej losowy
        vertexes = [i for i in range(size)]
        random.shuffle(vertexes)

        for i in range(len(vertexes)):
            # przydziela każdemu wierzchołkowi maksymalną liczbę krawędzi
            v0 = vertexes[i]
            for v1 in vertexes[i+1:]:
                self.incidence_list[v0].append(v1)
                self.incidence_list[v1].append(v0)
                edges -= 1
                if edges == 0:
                    return 0  # kończy, gdy wykorzystał wszystkie krawędzie

    def generate_graph_e(self, size: int, edges: int):
        # GENERATOR GRAFÓW równomiernych

        # miesza wierzchołki, żeby rozkład był bardziej losowy
        vertexes = [i for i in range(size)]
        random.shuffle(vertexes)

        # najpierw daje każdemu wierzchołkowi minimalną liczbę krawędzi, później rozdziela pozostałe
        edges_per_v = floor(edges * 2 / size)

        while edges > 0:
            vertex_no = 1
            for v0 in vertexes:
                edges_from_v = edges_per_v - len(self.incidence_list[v0])

                possible_v1 = vertexes[vertex_no:]  # bierzemy pod uwagę tylko "późniejsze" wierzchołki
                random.shuffle(possible_v1)

                for i in range(edges_from_v):
                    if len(possible_v1) < i + 1:
                        # jeżeli skończyły nam się "późniejsze" wierzchołki, szukamy wierzchołka,
                        # który ma dobrą liczbę krawędzi i dokładamy mu jedną
                        j = 0
                        while len(self.incidence_list[vertexes[j]]) > edges_per_v:
                            j += 1
                        v1 = vertexes[j]
                    else:
                        # dodanie wierzchołków do listy incydencji
                        v1 = possible_v1[i]
                    self.incidence_list[v0].append(v1)
                    self.incidence_list[v1].append(v0)
                    edges -= 1
                    if edges == 0:
                        return 0  # kończy, gdy wykorzystał wszystkie krawędzie
                vertex_no += 1
            edges_per_v += 1

    def generate_graph(self, size: int, saturation=50, graph_type='r'):  # petle_wlasne = False
        # GENERATOR GRAFÓW o ilości wierzchołków size i nasyceniu krawędziami[%] 'saturation'
        graph_type.lower()
        if graph_type not in {'c', 'e', 'r'}:
            raise ValueError("Nieznany typ grafu")

        self.size = size
        self.incidence_list = [[] for _ in range(size)]
        self.coloring = [0 for _ in range(self.size)]
        edges = round(size * (size - 1) / 2 * saturation / 100)

        if graph_type == 'c':              # condensed
            self.name = "zagęszczony"
            self.generate_graph_c(size, edges)
        elif graph_type == 'e':            # even
            self.name = "równomierny"
            self.generate_graph_e(size, edges)
        elif graph_type == 'r':            # random
            self.name = "losowy"
            self.generate_graph_r(size, edges)

    def show_incidence_list(self, start=1):
        print("LISTA INCYDENCJI")
        for row in range(len(self.incidence_list)):
            print(row + start, ".", end=" ")
            for col in range(len(self.incidence_list[row])):
                print(self.incidence_list[row][col] + start, end=" ")
            print()
        print()

    def show_coloring(self, long=False):
        if long:
            print("KOLOROWANIE")
            for i in range(self.size):
                print(i + 1, ".", self.coloring[i])

        print("Dla grafu", self.name, "użyto", self.colors, "kolorów.")

    def vertex_color(self, v: int):
        for color in range(1, self.colors + 1):
            used = False
            for neighbour in self.incidence_list[v]:
                if self.coloring[neighbour] == color:
                    used = True
                    break
            if not used:
                self.coloring[v] = color
                return

        self.colors += 1
        self.coloring[v] = self.colors
        return

    def graph_coloring_greedy(self):
        for v in range(self.size):
            self.vertex_color(v)

    def import_from_file(self, filename: str):
        # WCZTYWANIE Z PLIKU
        with open(filename, "r") as file:
            self.size = int(file.readline())  # wczytujemy z pliku ilosc wierzcholkow
            self.name = filename
            self.incidence_list = [[] for _ in range(self.size)]  # wczytujemy dane z pliku
            # print("rozmiar: ", self.size, "sasiedzi: ", self.incidence_list)
            for line in file:
                if re.match("[0-9]* [0-9]*", line):
                    a, b = map(int, line.split())
                    # print("a: ", a, " b: ", b)
                    if a < b:
                        self.incidence_list[a - 1].append(b - 1)
                        self.incidence_list[b - 1].append(a - 1)
            self.coloring = [0 for _ in
                             range(self.size)]  # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza,
                                                # że wierzchołek jest jeszcze nie pokolorowany

    def list_of_edges_two_lists(self):
        v0 = []
        v1 = []
        for i in range(0, len(self.incidence_list)):
            for neighbour in self.incidence_list[i]:
                if i < neighbour:
                    v0.append(i + 1)
                    v1.append(neighbour + 1)
        return v0, v1

    def list_of_edges_pairs(self):
        edges = []
        for i in range(0, len(self.incidence_list)):
            for neighbour in self.incidence_list[i]:
                if i < neighbour:
                    edges.append((i, neighbour))
        return edges

    def visual(self):
        # SHOW GRAPH VISUAL REPRESENTATION
        v0, v1 = self.list_of_edges_two_lists()
        df = pd.DataFrame({'from': v0, 'to': v1})  # connections
        carac = pd.DataFrame(
            {'ID': [i + 1 for i in range(self.size)], 'myvalue': self.coloring})  # characteristics for nodes
        graph = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())  # graph
        # reorder carac to assign the good color to each node
        carac = carac.set_index('ID')
        carac = carac.reindex(graph.nodes())

        # transform categorical column in a numerical value: group1->1, group2->2...
        carac['myvalue'] = pd.Categorical(carac['myvalue'])
        # carac['myvalue'].cat.codes

        # show
        nx.draw(graph, with_labels=True, node_color=carac['myvalue'].cat.codes, cmap=plt.cm.Set1, node_size=1500)
        plt.show()

    def export(self, filename: str):
        # ZAPIS DO PLIKU
        v0, v1 = self.list_of_edges_two_lists()
        print()
        # nazwa_pliku: str=input("Podaj nazwe pliku do zapisu grafu "+ self.nazwa + ": ")
        with open(filename, "w") as file:
            file.write(str(self.size) + "\n")
            for i in range(len(v0)): file.write(str(v0[i]) + " " + str(v1[i]) + "\n")
            print("Zapisano do pliku " + filename)

