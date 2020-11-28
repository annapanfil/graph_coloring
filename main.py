import random
from math import floor
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import re
import argparse

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

    def pokaz_kolorowanie(self, long = False):
        if long:
            print("KOLOROWANIE")
            for i in range(self.rozmiar):
                print(i+1, ".", self.kolorowanie[i])

        print("Dla grafu", self.nazwa , "użyto", self.kolory, "kolorów.")

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

    def wczytaj_z_pliku(self, filename: str):
        # WCZTYWANIE Z PLIKU
        with open(filename, "r") as file:
            self.rozmiar=int(file.readline())                #wczytujemy z pliku ilosc wierzcholkow

            self.sasiedzi = [[]for _ in range(self.rozmiar)] # wczytujemy dane z pliku
            # print("rozmiar: ", self.rozmiar, "sasiedzi: ", self.sasiedzi)
            for line in file:
                if re.match("[0-9]* [0-9]*", line):
                    a,b = map(int, line.split())
                    #print("a: ", a, " b: ", b)
                    if(a<b):
                        self.sasiedzi[a-1].append(b-1)
                        self.sasiedzi[b-1].append(a-1)
            self.kolorowanie = [0 for _ in range(self.rozmiar)]     # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza,
                                                                    # że wierzchołek jest jeszcze nie pokolorowany

    def lista_krawedzi(self):
        v0 = []
        v1 = []
        for i in range(0, len(self.sasiedzi)):
            for sasiad in self.sasiedzi[i]:
                if(i<sasiad):
                    v0.append(i+1)
                    v1.append(sasiad+1)
        return v0, v1

    def visual(self):
        # SHOW GRAPH VISUAL REPRESENTATION
        v0, v1 = self.lista_krawedzi()
        df = pd.DataFrame({'from': v0, 'to': v1}) # connections
        carac = pd.DataFrame({'ID': [i+1 for i in range(self.rozmiar)] , 'myvalue': self.kolorowanie}) # characteristics for nodes
        G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph()) # graph
        # reorder carac to assign the good color to each node
        carac = carac.set_index('ID')
        carac = carac.reindex(G.nodes())

        # transform categorical column in a numerical value: group1->1, group2->2...
        carac['myvalue'] = pd.Categorical(carac['myvalue'])
        carac['myvalue'].cat.codes

        # show
        nx.draw(G, with_labels=True, node_color=carac['myvalue'].cat.codes, cmap=plt.cm.Set1, node_size=1500)
        plt.show()

    def export(self, filename: str):
        # ZAPIS DO PLIKU
        v0, v1 = self.lista_krawedzi()
        print()
        # nazwa_pliku: str=input("Podaj nazwe pliku do zapisu grafu "+ self.nazwa + ": ")
        with open(filename, "w") as file:
            file.write(str(self.rozmiar)+"\n")
            for i in range(len(v0)): file.write(str(v0[i])+ " "+ str(v1[i])+"\n")
            print("Zapisano do pliku " + filename)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="import from file")
    parser.add_argument("-v", "--vertexes", type=int, help="number of vertexes")
    parser.add_argument("-s", "--saturation", type=int, help="saturation in %%")
    parser.add_argument("-t", "--type", help="z – zagęszczony, r – równomierny, l – losowy")
    parser.add_argument("-d", "--debug", action='store_true', help = "debug mode")
    parser.add_argument("-e", "--export", help="export to file")
    filename = parser.parse_args().file
    verbose = parser.parse_args().long
    export = parser.parse_args().export

    if filename: return [verbose, export, filename, None]

    vertexes = parser.parse_args().vertexes
    saturation = parser.parse_args().saturation
    type = parser.parse_args().type

    generator_list = None
    if vertexes: generator_list = [vertexes]
    if saturation:
        generator_list.append(saturation)
        if type: generator_list.append(type)

    return [verbose, export, None, generator_list]



def main():
    verbose, export, filename, generator_list = parse();
    # print(verbose, filename, generator_list)

    g = Graf()

    if filename:
        try:
            g.wczytaj_z_pliku(filename)
        except FileNotFoundError as msg:
            print("Nie można otworzyć pliku")
            return 0
    elif generator_list:
        try:
            g.generuj_graf(*generator_list)
        except ValueError as msg:
            print("Nie można wygenerować grafu (", msg, ')')
            return 0
    else:
        print("Nie podano parametrów")
        return 0

    if verbose: g.pokaz_liste_incydencji()
    g.koloruj_graf()
    g.pokaz_kolorowanie(verbose)
    g.visual()
    if export: g.export(export)

if __name__ == '__main__':
    main()
