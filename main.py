from graph import Graph
from tabu import Tabu
import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="import from file")
    parser.add_argument("-v", "--vertexes", type=int, help="number of vertexes")
    parser.add_argument("-s", "--saturation", type=int, help="saturation in %%")
    parser.add_argument("-t", "--type", help="c – condensed, e – even, r – random")
    parser.add_argument("-d", "--debug", action='store_true', help="debug mode")
    parser.add_argument("-e", "--export", help="export to file")
    parser.add_argument("-g", "--greedy", action='store_true', help="use greedy instead of tabu")
    filename = parser.parse_args().file
    debug = parser.parse_args().debug
    export = parser.parse_args().export
    greedy = parser.parse_args().greedy

    if filename: return [debug, export, filename, None, greedy]

    vertexes = parser.parse_args().vertexes
    saturation = parser.parse_args().saturation
    graph_type = parser.parse_args().type

    generator_list = None
    if vertexes: generator_list = [vertexes]
    if saturation:
        generator_list.append(saturation)
        if graph_type: generator_list.append(graph_type)

    return [debug, export, None, generator_list, greedy]


def main():
    debug, export, filename, generator_list, greedy = parse()

    # GENEROWANIE GRAFU WG FLAG
    graph = Graph()
    if filename:
        try:
            graph.import_from_file(filename)
        except FileNotFoundError:
            print("Nie można otworzyć pliku")
            return 0
    elif generator_list:
        try:
            graph.generate_graph(*generator_list)
        except ValueError as msg:
            print("Nie można wygenerować grafu (", msg, ')')
            return 0
    else:
        print("Nie podano parametrów")
        return 0

    if debug: graph.show_incidence_list()

    # KOLOROWANIE
    if greedy:
        graph.graph_coloring_greedy()
    else:
        tabu = Tabu(graph)
        tabu.main()

    graph.show_coloring(debug)
    graph.visual()

    if export: graph.export(export)


if __name__ == '__main__':
    main()
