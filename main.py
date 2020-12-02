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
    filename = parser.parse_args().file
    debug = parser.parse_args().debug
    export = parser.parse_args().export

    if filename: return [debug, export, filename, None]

    vertexes = parser.parse_args().vertexes
    saturation = parser.parse_args().saturation
    graph_type = parser.parse_args().type

    generator_list = None
    if vertexes: generator_list = [vertexes]
    if saturation:
        generator_list.append(saturation)
        if graph_type: generator_list.append(graph_type)

    return [debug, export, None, generator_list]


def main():
    # debug, export, filename, generator_list = parse()

    graph = Graph()
    graph.import_from_file("simple")

    tabu = Tabu(g)
    tabu.main()

    # GENEROWANIE GRAFU WG FLAG
    # if filename:
    #     try:
    #         graph.import_from_file(filename)
    #     except FileNotFoundError:
    #         print("Nie można otworzyć pliku")
    #         return 0
    # elif generator_list:
    #     try:
    #         graph.generate_graph(*generator_list)
    #     except ValueError as msg:
    #         print("Nie można wygenerować grafu (", msg, ')')
    #         return 0
    # else:
    #     print("Nie podano parametrów")
    #     return 0
    #
    # if debug: graph.show_incidence_list()
    # graph.graph_coloring_greedy()
    # graph.show_coloring(debug)
    # graph.visual()
    # if export: graph.export(export)
