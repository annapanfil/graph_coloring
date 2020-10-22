import random

def printList(list):
    # print("\nLIST")
    for row in range(len(list)):
        print(row, ".", end=" ")
        for col in range(len(list[row])):
            print(list[row][col], end=" ")
        print()

rozmiar = random.randint(3,7)         # ile wierzchołków w grafie
kolory = 1                            # mówi ile kolorów jest użytych jak na razie
sasiedzi=[]                           # każda podlista to zbiór sąsiadów danego wierzchołka
for i in range(rozmiar):
    sasiedzi.append([])
for i in range(rozmiar):
    for j in range(i+1, rozmiar):
        czy_krawedz = random.randint(0,1)
        if czy_krawedz == 1: # and j != i:
            sasiedzi[i].append(j)
            sasiedzi[j].append(i)


kolorowanie=[]
for i in range(rozmiar):
    kolorowanie.append([i, 0])        # wierzchołki od numeruję 0, a kolory od 1 w górę, 0 na pozycji kolorów oznacza, że wierzchołek jest jeszcze nie pokolorowany
                                      # można zapisać to w postaci prostej listy bez zagnieżdżania podlist

def koloruj(v):                       # v to numer wierzchołka
    global kolory
    for kolor in range(1, kolory+1):
        uzyty = False
        for sasiad in sasiedzi[v]:
            if kolorowanie[sasiad][1] == kolor:
                uzyty = True
                break
        if uzyty == False:
            kolorowanie[v][1] = kolor
            return
    # if kolorowanie[v][1] == 0: # jak zrobimy returny, to nie powinien tu dojść
    kolory += 1
    kolorowanie[v][1] = kolory
    return



def main():
    print("Wylosowany graf ma ", rozmiar, "wierzchołków.")
    print("Lista incydencji:")
    printList(sasiedzi)
    for v in range(rozmiar):
        koloruj(v)
    print("Kolorowanie:", kolorowanie)
    print("Użyto", kolory, "kolory/ów.")
main()
