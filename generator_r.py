import random

class Graph:
    def __init__(self):  # rozmiar = random.randint(3,7) - drugi arg
        self.name = "LOSOWY"
        self.size = 0  # ile wierzchołków w grafie
        self.colors = 1  # ile kolorów jest użytychjak na razie
        self.incidence_list = []  # każda podlista to zbiór sąsiadów danego wierzchołka
        self.coloring = []  # = [0 for _ in range(self.rozmiar)]   # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza, że wierzchołek jest jeszcze nie pokolorowany

    def generate_graph_r(self, size: int, saturation=50, type='r'):  # petle_wlasne = False
        # GENERATOR GRAFÓW o ilości wierzchołków size i nasyceniu krawędziami[%] 'saturation'
        type.lower()

        self.name = "losowy"  # random
        self.size = size
        edges = round(size * (size - 1) / 2 * saturation / 100)
        incidence_list = [[] for _ in range(size)]

        # miesza wierzchołki, żeby rozkład był bardziej losowy
        vertexes = [i for i in range(size)]
        random.shuffle(vertexes)
        repeat = False

        while edges > 0:
            for vertex_no in range(len(vertexes)):
                v0 = vertexes[vertex_no]
                # bierzemy pod uwagę tylko "późniejsze" wierzchołki, których jeszcze nie ma w liście incydencji
                possible_v1 = vertexes[vertex_no+1:]
                if repeat: possible_v1 = [x for x in possible_v1 if x not in incidence_list[v0]]
                random.shuffle(possible_v1)

                edges_from_v = random.randint(0, len(possible_v1))

                for i in range(edges_from_v):
                    # print("edges", edges, "i", i ,"v0", v0, "edges_per_v", edges_from_v, "v1", possible_v1, "długosc", len(possible_v1))
                    v1 = possible_v1[i]
                    # dodanie wierzchołków do listy incydencji
                    incidence_list[v0].append(v1)
                    incidence_list[v1].append(v0)
                    edges -= 1
                    if edges == 0:
                        self.incidence_list = incidence_list
                        self.coloring = [0 for _ in range(self.size)]
                        return 0  # kończy, gdy wykorzystał wszystkie krawędzie
            repeat = True


if __name__ == '__main__':
    g = Graph()
    g.generate_graph_r(50, 100)
    print([len(x) for x in g.incidence_list])
