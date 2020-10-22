import random

class Graf():
    def __init__(self, rozmiar = random.randint(3,7)):
        self.rozmiar = rozmiar      # ile wierzchołków w grafie
        self.kolory = 1             # ile kolorów jest użytych jak na razie
        self.sasiedzi = []          # każda podlista to zbiór sąsiadów danego wierzchołka
        self.kolorowanie = [0 for _ in range(rozmiar)]   # kolory numerujemy od 1 w górę, 0 na pozycji kolorów oznacza, że wierzchołek jest jeszcze nie pokolorowany

    def generuj_krawedzie(self):
        for i in range(self.rozmiar):
            self.sasiedzi.append([])
        for i in range(self.rozmiar):
            for j in range(i+1, self.rozmiar):
                czy_krawedz = random.randint(0,1)
                if czy_krawedz == 1:
                    self.sasiedzi[i].append(j)
                    self.sasiedzi[j].append(i)

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
            print(i, ".", self.kolorowanie[i])

        print("Użyto", self.kolory, "koloru/ów.\n")

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


def main():
    g = Graf()
    g.generuj_krawedzie()
    g.pokaz_liste_incydencji()
    g.koloruj_graf()
    g.pokaz_kolorowanie()

if __name__ == '__main__':
    main()
