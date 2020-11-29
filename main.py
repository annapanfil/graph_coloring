import random
from math import floor
import pandas as pd
# import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import re
import argparse


class Graph:
    def __init__(self):  # rozmiar = random.randint(3,7) - drugi arg
        self.name = "LOSOWY"
        self.size = 0  # ile wierzchołków w grafie
        self.colors = 1  # ile kolorów jest użytychjak na razie
        self.incidence_list = []  # każda podlista to zbiór sąsiadów danego wierzchołka
        self.coloring = []  # = [0 for _ in range(self.rozmiar)]   # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza, że wierzchołek jest jeszcze nie pokolorowany

    def generate_graph(self, size: int, saturation=50, type='r'):  # petle_wlasne = False
        # GENERATOR GRAFÓW o ilości wierzchołków size i nasyceniu krawędziami[%] 'saturation'
        type.lower()
        if type == 'c':
            self.name = "zagęszczony"  # condensed
        elif type == 'e':
            self.name = "równomierny"  # even
        elif type == 'r':
            self.name = "losowy"  # random
        else:
            raise ValueError("Nieznany typ grafu")

        self.size = size
        edges = round(size * (size - 1) / 2 * saturation / 100)
        incidence_list = [[] for _ in range(size)]

        # miesza wierzchołki, żeby rozkład był bardziej losowy
        vertexes = [i for i in range(size)]
        random.shuffle(vertexes)
        repeat = False

        # przy równomiernym rozkładzie najpierw daje każdemu wierzchołkowi minimalną liczbę krawędzi, później rozdziela pozostałe
        if type == 'e': edges_per_v = floor(edges * 2 / size)

        while edges > 0:
            vertex_no = 1
            for v0 in vertexes:
                # w zagęszczonym przydziela każdemu wierzchołkowi maksymalną liczbę krawędzi
                if type == 'c':
                    edges_from_v = size - vertex_no
                elif type == 'e':
                    edges_from_v = edges_per_v - len(incidence_list[v0])
                # losowy działa losowo
                else:
                    edges_from_v = random.randint(0, size - vertex_no)

                possible_v1 = vertexes[vertex_no:]  # bierzemy pod uwagę tylko "późniejsze" wierzchołki
                if type != 'c': random.shuffle(possible_v1)  # przy 'c' i tak łączymy z wszystkimi możliwymi wierzchołkami

                for i in range(edges_from_v):
                    # print("edges", edges, "i", i ,"v0", v0, "edges_per_v", edges_from_v, "v1", possible_v1, "długosc", len(possible_v1))
                    if (type == 'e' and len(possible_v1) < i + 1):
                        # jeżeli skończyły nam się "późniejsze" wierzchołki, szukamy wierzchołka, który ma dobrą liczbę krawędzi i dokładamy mu jedną
                        j = 0
                        while len(incidence_list[vertexes[j]]) > edges_per_v:
                            j += 1
                        v1 = vertexes[j]
                    elif repeat:  # jeżeli idziemy kolejny raz, musimy sprawdzić, czy już nie ma takiej krawędzi
                        if possible_v1[i] in incidence_list[v0]: continue
                    else:
                        v1 = possible_v1[i]

                    # dodanie wierzchołków do listy incydencji
                    incidence_list[v0].append(v1)
                    incidence_list[v1].append(v0)
                    edges -= 1
                    if edges == 0:
                        self.incidence_list = incidence_list
                        self.coloring = [0 for _ in range(self.size)]
                        return 0  # kończy, gdy wykorzystał wszystkie krawędzie
                vertex_no += 1
            if type == 'r': repeat = True
            if type == 'e': edges_per_v += 1

    def show_incidence_list(self):
        print("LISTA INCYDENCJI")
        for row in range(len(self.incidence_list)):
            print(row + 1, ".", end=" ")
            for col in range(len(self.incidence_list[row])):
                print(self.incidence_list[row][col] + 1, end=" ")
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

    def list_of_edges(self):
        v0 = []
        v1 = []
        for i in range(0, len(self.incidence_list)):
            for neighbour in self.incidence_list[i]:
                if i < neighbour:
                    v0.append(i + 1)
                    v1.append(neighbour + 1)
        return v0, v1

    def visual(self):
        # SHOW GRAPH VISUAL REPRESENTATION
        v0, v1 = self.list_of_edges()
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
        v0, v1 = self.list_of_edges()
        print()
        # nazwa_pliku: str=input("Podaj nazwe pliku do zapisu grafu "+ self.nazwa + ": ")
        with open(filename, "w") as file:
            file.write(str(self.size) + "\n")
            for i in range(len(v0)): file.write(str(v0[i]) + " " + str(v1[i]) + "\n")
            print("Zapisano do pliku " + filename)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="import from file")
    parser.add_argument("-v", "--vertexes", type=int, help="number of vertexes")
    parser.add_argument("-s", "--saturation", type=int, help="saturation in %%")
    parser.add_argument("-t", "--type", help="c – condensed, e – even, r – random")
    parser.add_argument("-d", "--debug", action='store_true', help="debug mode")
    parser.add_argument("-e", "--export", help="export to file")
    filename = parser.parse_args().file
    debug = parser.parse_args().debug
    export = parser.parse_args().export

    if filename: return [debug, export, filename, None]

    vertexes = parser.parse_args().vertexes
    saturation = parser.parse_args().saturation
    type = parser.parse_args().type

    generator_list = None
    if vertexes: generator_list = [vertexes]
    if saturation:
        generator_list.append(saturation)
        if type: generator_list.append(type)

    return [debug, export, None, generator_list]


def main():
    verbose, export, filename, generator_list = parse()
    # print(verbose, filename, generator_list)

    g = Graph()

    if filename:
        try:
            g.import_from_file(filename)
        except FileNotFoundError:
            print("Nie można otworzyć pliku")
            return 0
    elif generator_list:
        try:
            g.generate_graph(*generator_list)
        except ValueError as msg:
            print("Nie można wygenerować grafu (", msg, ')')
            return 0
    else:
        print("Nie podano parametrów")
        return 0

    if verbose: g.show_incidence_list()
    g.graph_coloring_greedy()
    g.show_coloring(verbose)
    g.visual()
    if export: g.export(export)


if __name__ == '__main__':
    main()
