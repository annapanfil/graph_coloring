import random
from math import floor

class Graf():
    def __init__(self):             #rozmiar = random.randint(3,7) - drugi arg
        self.nazwa = "LOSOWY"
        self.rozmiar = 0            # ile wierzchołków w grafie
        self.kolory = 1             # ile kolorów jest użytychjak na razie
        self.sasiedzi = []          # każda podlista to zbiór sąsiadów danego wierzchołka
        self.kolorowanie = [] #= [0 for _ in range(self.rozmiar)]   # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza, że wierzchołek jest jeszcze nie pokolorowany

    def generuj_graf(self, v: int, nasycenie = 100, typ = 'r'): #petle_wlasne = True
        # typ: z – zagęszczony, l – losowy, r – równomierny
        typ.lower()
        self.rozmiar = v
        e = round(v*(v-1)/2 * nasycenie/100)
        print(e)
        lista_incydencji = [[]for _ in range(v)]

        wierzcholki = [i for i in range(v)]
        random.shuffle(wierzcholki)
        powtorka = False
        if typ == "r": krawedzi = floor(e*2/v)

        print(wierzcholki)
        while e > 0:
            i=1
            for v0 in wierzcholki[:-1]:
                if typ == 'z': krawedzi_z_wierzcholka = v-i
                elif typ == "r":
                    krawedzi_z_wierzcholka = krawedzi - len(lista_incydencji[v0])
                    # krawedzi_z_wierzcholka = ceil(e*2/(v-i+1)) - len(lista_incydencji[v0]) # nieskierowany
                    # if krawedzi_z_wierzcholka > v-i: krawedzi_z_wierzcholka = v-i
                    # if powtorka: krawedzi_z_wierzcholka = ceil(e*2/(v-i+1))
                elif typ == "l" : krawedzi_z_wierzcholka = random.randint(0,v-i)
                else: raise ValueError("Nieznany typ grafu")

                mozliwe_v1 = wierzcholki[i:]
                if type != 'z': random.shuffle(mozliwe_v1)
                print("e", e, "i", i ,"v0", v0, "krawedzi", krawedzi_z_wierzcholka, "v1", mozliwe_v1)

                for j in range(krawedzi_z_wierzcholka):
                    if powtorka or typ == 'r':
                        if mozliwe_v1[j] in lista_incydencji[v0] :
                            break
                    lista_incydencji[v0].append(mozliwe_v1[j])
                    lista_incydencji[mozliwe_v1[j]].append(v0)
                    e-=1
                    if e == 0:
                        self.sasiedzi = lista_incydencji
                        self.kolorowanie = [0 for _ in range(self.rozmiar)]
                        return 0
                i+=1
            powtorka = True
            if typ == "r": krawedzi+=1
            print("powtórka")

    def pokaz_liste_incydencji(self):
        print("LISTA INCYDENCJI")
        for row in range(len(self.sasiedzi)):
            print(row, ".", end=" ")
            for col in range(len(self.sasiedzi[row])):
                print(self.sasiedzi[row][col], end=" ")
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
        #WCZTYWANIE Z PLIKU
        print("Podaj nazwe pliku z ktorego pobierzemy dane: ")          #otwieramy plik
        nazwa_pliku: str=input()
        self.nazwa = nazwa_pliku
        file = open(nazwa_pliku, "r")

        self.rozmiar=int(file.readline())                    #wczytujemy z pliku ilosc wierzcholkow

        for i in range(self.rozmiar):                        #wczytujemy dane z pliku
            self.sasiedzi.append([])
        #print("rozmiar: ", self.rozmiar, "sasiedzi: ", self.sasiedzi)
        for line in file:
            a,b = map(int, line.split())
            #print("a: ", a, " b: ", b)
            if(a<b):
                self.sasiedzi[a-1].append(b)
                self.sasiedzi[b-1].append(a)
        self.kolorowanie = [0 for _ in range(self.rozmiar)]        # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza,
                                                                                    # że wierzchołek jest jeszcze nie pokolorowany


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

if __name__ == '__main__':
    main()
