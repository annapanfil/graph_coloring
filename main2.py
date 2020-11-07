import random

class Graf():
    def __init__(self):             #rozmiar = random.randint(3,7) - drugi arg
        self.nazwa = "LOSOWY"
        self.rozmiar = 0     # ile wierzchołków w grafie
        self.kolory = 1             # ile kolorów jest użytych jak na razie
        self.sasiedzi = []          # każda podlista to zbiór sąsiadów danego wierzchołka
        self.kolorowanie = [0 for _ in range(self.rozmiar)]   # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza, że wierzchołek jest jeszcze nie pokolorowany

    def generuj_krawedzie(self):
        for i in range(self.rozmiar):
            self.sasiedzi.append([])
        for i in range(self.rozmiar):
            for j in range(i+1, self.rozmiar):
                czy_krawedz = random.randint(0,1)
                if czy_krawedz == 1:
                    self.sasiedzi[i].append(j+1)
                    self.sasiedzi[j].append(i+1)

    def pokaz_liste_incydencji(self):
        print("LISTA INCYDENCJI")
        for row in range(len(self.sasiedzi)):
            print(row+1, ".", end=" ")
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
                if self.kolorowanie[sasiad-1] == kolor:
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
    #g.generuj_krawedzie()
    g.wczytaj_z_pliku()
    g.pokaz_liste_incydencji()
    g.koloruj_graf()
    g.pokaz_kolorowanie()

if __name__ == '__main__':
    main()