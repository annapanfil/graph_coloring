import random
from math import  floor


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


if __name__ == '__main__':
    g = Graph()
    g.generate_graph(50, 50, 'r')
    print([len(x) for x in g.incidence_list])
    g.generate_graph(50, 50, 'c')
    print([len(x) for x in g.incidence_list])
    g.generate_graph(50, 50, 'e')
    print([len(x) for x in g.incidence_list])
