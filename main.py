from graph import Graph
from tabu import Tabu
import argparse
import time

def tester():
    repeats = 5
    graphs_to_test = ["queen6.txt", "anna.col", "david.col", "miles250.txt", "le450_5a.txt", "gc500.txt", "gc_1000_300013.txt"]
    for filename in graphs_to_test:
        colors_avg = 0
        time_avg = 0
        for i in range(repeats):
            colors_curr, time_curr = main([False, False, False, "instances/"+filename, None, False])
            colors_avg += colors_curr
            time_avg += time_curr
        colors_avg /= repeats
        time_avg /= repeats
        print(f"\033[36m{filename} {colors_avg:.3f} {time_avg:.3f}\033[0m")


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="import from file")
    parser.add_argument("-v", "--vertexes", type=int, help="number of vertexes")
    parser.add_argument("-s", "--saturation", type=int, help="saturation in %%")
    parser.add_argument("-t", "--type", help="c – condensed, e – even, r – random")
    parser.add_argument("-d", "--debug", action='store_true', help="debug mode")
    parser.add_argument("-e", "--export", help="export to file")
    parser.add_argument("-g", "--greedy", action='store_true', help="use greedy instead of tabu")
    parser.add_argument("-i", "--image", action='store_true', help="show image of the coloured graph")
    filename = parser.parse_args().file
    debug = parser.parse_args().debug
    export = parser.parse_args().export
    greedy = parser.parse_args().greedy
    image = parser.parse_args().image

    if filename: return [image, debug, export, filename, None, greedy]

    vertexes = parser.parse_args().vertexes
    saturation = parser.parse_args().saturation
    graph_type = parser.parse_args().type

    generator_list = None
    if vertexes: generator_list = [vertexes]
    if saturation:
        generator_list.append(saturation)
        if graph_type: generator_list.append(graph_type)

    return [image, debug, export, None, generator_list, greedy]

def measure_time(function):
    start = time.clock()
    result = function()
    end = time.clock()
    duration = end - start
    return (duration, result)

def main(args):
    image, debug, export, filename, generator_list, greedy = args

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
    duration = 0
    if greedy:
        graph.graph_coloring_greedy()
    else:
        tabu = Tabu(graph)
        duration, result = measure_time(tabu.main)
        graph.coloring, graph.colors = result

    # graph.show_coloring(debug)
    if image: graph.visual()
    if export: graph.export(export)

    return graph.colors, duration


if __name__ == '__main__':
    # main(parse())
    tester()
