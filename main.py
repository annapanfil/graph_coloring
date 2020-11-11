import random
from math import floor
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Graf():
    def __init__(self):             # rozmiar = random.randint(3,7) - drugi arg
        self.nazwa = "LOSOWY"
        self.rozmiar = 0            # ile wierzchołków w grafie
        self.kolory = 1             # ile kolorów jest użytychjak na razie
        self.sasiedzi = []          # każda podlista to zbiór sąsiadów danego wierzchołka
        self.kolorowanie = [] #= [0 for _ in range(self.rozmiar)]   # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza, że wierzchołek jest jeszcze nie pokolorowany

    def generuj_graf(self, v: int, nasycenie = 50, typ = 'l'): # petle_wlasne = False
        ### GENERATOR GRAFÓW o ilości wierzchołków v i nasyceniu krawędziami[%] 'nasycenie' ###

        typ.lower()
        if typ == 'z': self.nazwa = "zagęszczony"
        elif typ == 'r': self.nazwa = "równomierny"
        elif typ == 'l': self.nazwa = "losowy"
        else: raise ValueError("Nieznany typ grafu")

        self.rozmiar = v
        e = round(v*(v-1)/2 * nasycenie/100)
        lista_incydencji = [[] for _ in range(v)]

        # miesza wierzchołki, żeby rozkład był bardziej losowy
        wierzcholki = [i for i in range(v)]
        random.shuffle(wierzcholki)
        powtorka = False

        # przy równomiernym rozkładzie najpierw daje każdemu wierzchołkowi minimalną liczbę krawędzi, później rozdziela pozostałe
        if typ == 'r': krawedzi = floor(e*2/v)

        while e > 0:
            nr_wierzcholka = 1
            for v0 in wierzcholki:
                # w zagęszczonym przydziela każdemu wierzchołkowi maksymalną liczbę krawędzi
                if typ == 'z': krawedzi_z_wierzcholka = v-nr_wierzcholka
                elif typ == 'r': krawedzi_z_wierzcholka = krawedzi - len(lista_incydencji[v0])
                # losowy działa losowo
                else: krawedzi_z_wierzcholka = random.randint(0,v-nr_wierzcholka)

                mozliwe_v1 = wierzcholki[nr_wierzcholka:] # bierzemy pod uwagę tylko "późniejsze" wierzchołki
                if typ != 'z': random.shuffle(mozliwe_v1) # przy 'z' i tak łączymy z wszystkimi możliwymi wierzchołkami

                for i in range(krawedzi_z_wierzcholka):
                    # print("e", e, "i", i ,"v0", v0, "krawedzi", krawedzi_z_wierzcholka, "v1", mozliwe_v1, "długosc", len(mozliwe_v1))
                    if (typ == 'r' and len(mozliwe_v1)<i+1):
                        # jeżeli skończyły nam się "późniejsze" wierzchołki, szukamy wierzchołka, który ma dobrą liczbę krawędzi i dokładamy mu jedną
                        j = 0
                        while(len(lista_incydencji[wierzcholki[j]]) > krawedzi):
                            j+=1
                        v1 = wierzcholki[j]
                    elif powtorka:  # jeżeli idziemy kolejny raz, musimy sprawdzić, czy już nie ma takiej krawędzi
                        if mozliwe_v1[i] in lista_incydencji[v0]: continue
                    else:
                        v1 = mozliwe_v1[i]

                    # dodanie wierzchołków do listy incydencji
                    lista_incydencji[v0].append(v1)
                    lista_incydencji[v1].append(v0)
                    e-=1
                    if e == 0:
                        self.sasiedzi = lista_incydencji
                        self.kolorowanie = [0 for _ in range(self.rozmiar)]
                        return 0    # kończy, gdy wykorzystał wszystkie krawędzie
                nr_wierzcholka += 1
            if typ == 'l': powtorka = True
            if typ == "r": krawedzi += 1

    def pokaz_liste_incydencji(self):
        print("LISTA INCYDENCJI")
        for row in range(len(self.sasiedzi)):
            print(row+1, ".", end=" ")
            for col in range(len(self.sasiedzi[row])):
                print(self.sasiedzi[row][col]+1, end=" ")
            print()
        print()

    def pokaz_kolorowanie(self):
        print("KOLOROWANIE")
        for i in range(self.rozmiar):
            print(i+1, ".", self.kolorowanie[i])

        print("Dla grafu", self.nazwa , "użyto", self.kolory, "kolorów.\n")

    def koloruj_wierzcholek(self, v: int):
        for kolor in range(1, self.kolory+1):
            uzyty = False
            for sasiad in self.sasiedzi[v]:
                if self.kolorowanie[sasiad] == kolor:
                    uzyty = True
                    break
            if uzyty == False:
                self.kolorowanie[v] = kolor
                return

        self.kolory += 1
        self.kolorowanie[v] = self.kolory
        return

    def koloruj_graf(self):
        for v in range(self.rozmiar):
            self.koloruj_wierzcholek(v)

    def wczytaj_z_pliku(self):
        # WCZTYWANIE Z PLIKU
        error = True
        while(error):
            print("Podaj nazwe pliku z ktorego pobierzemy dane: ")
            nazwa_pliku: str=input()
            self.nazwa = nazwa_pliku
            try:
                file = open(nazwa_pliku, "r")
                error = False
            except: print("Nie można otworzyć pliku")

        self.rozmiar=int(file.readline())                    #wczytujemy z pliku ilosc wierzcholkow

        self.sasiedzi = [[]for _ in range(self.rozmiar)] # wczytujemy dane z pliku
        # print("rozmiar: ", self.rozmiar, "sasiedzi: ", self.sasiedzi)
        for line in file:
            a,b = map(int, line.split())
            #print("a: ", a, " b: ", b)
            if(a<b):
                self.sasiedzi[a-1].append(b-1)
                self.sasiedzi[b-1].append(a-1)
        self.kolorowanie = [0 for _ in range(self.rozmiar)]     # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza,
        file.close()                                            # że wierzchołek jest jeszcze nie pokolorowany

    def l_krawedzi(self):
        v0 = []
        v1 = []
        for i in range(0, len(self.sasiedzi)):
            for sasiad in self.sasiedzi[i]:
                if(i<sasiad):
                    v0.append(i+1)
                    v1.append(sasiad+1)
        return v0, v1

    def visual(self):
        # Build a dataframe with your connections
        v0, v1 = self.l_krawedzi()
        df = pd.DataFrame({'from': v0, 'to': v1})

        # And a data frame with characteristics for your nodes
        carac = pd.DataFrame({'ID': [i+1 for i in range(self.rozmiar)] , 'myvalue': self.kolorowanie})

        # Build your graph
        G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())

        # The order of the node for networkX is the following order:
        G.nodes()
        # Thus, we cannot give directly the 'myvalue' column to netowrkX, we need to arrange the order!

        # Here is the tricky part: I need to reorder carac to assign the good color to each node
        carac = carac.set_index('ID')
        carac = carac.reindex(G.nodes())

        # And I need to transform my categorical column in a numerical value: group1->1, group2->2...
        carac['myvalue'] = pd.Categorical(carac['myvalue'])
        carac['myvalue'].cat.codes

        # Custom the nodes:
        nx.draw(G, with_labels=True, node_color=carac['myvalue'].cat.codes, cmap=plt.cm.Set1, node_size=1500)
        plt.show()

def main():
    g = Graf()
    try:
        g.generuj_graf(6)
    except ValueError as msg:
        print("Nie można wygenerować grafu (", msg, ')')
        return 0
    # g.wczytaj_z_pliku()
    g.pokaz_liste_incydencji()
    g.koloruj_graf()
    g.pokaz_kolorowanie()
    g.visual()

if __name__ == '__main__':
    main()
