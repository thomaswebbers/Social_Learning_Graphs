# This code prints plots a graph of the fitness inside a single robot
import matplotlib.pyplot as plt
import ast
import collections
import os
import Robot_data
import statistics
import sys
import re
from robot_data_lists import *
from scipy import stats
import numpy as np
from collections import Counter



# global variables of the system arguments
number_of_robots = None
number_of_controllers = None
number_of_generations = None
number_of_controllers_per_robot = None
number_of_runs = None
directory = None


# main function
def main():
    check_argument_count()
    #plot_simple_graphs()
    plot_quantifying_selection_pressure()


def plot_quantifying_selection_pressure():
    main_directory = directory

    for run in sorted_nicely(os.listdir(main_directory)):
        folder_name = run
        if not (run.startswith(".")):
            file_line_list = get_all_file_lines(main_directory, run)
            qsp_lines = get_qsp_lines(file_line_list)
            qsp_data_values = compute_qsp_data(qsp_lines)
            qsp_data = (qsp_data_values)
            plot_qsp(qsp_data, folder_name)



def get_all_file_lines(main_directory, run):
    list_of_lines = []

    inner_directory = os.path.join(main_directory, run)
    for file in os.listdir(inner_directory):
        if file.endswith(".txt"):
            file_name = os.path.join(inner_directory, file)
            file = open(file_name, "r")
            file_lines = file.readlines()
            for line in file_lines:
                no_tabs = line.split('\t')
                if(int(no_tabs[0]) > number_of_generations):
                    break
                list_of_lines.append(no_tabs)

    #print(len(list_of_lines))
    return list_of_lines


#todo return correct number of lines
#returns al ist of data lines sorted by generation
def get_qsp_lines(file_lines):
    list_of_lines_per_gen = []
    for generation in range(1, number_of_generations+1):
        list_of_lines_one_gen = []
        line_index = 0
        while line_index < len(file_lines):
            generation_value = int(file_lines[line_index][0])
            if generation_value == generation:
                data_line = file_lines.pop(line_index)
                list_of_lines_one_gen.append(data_line)
                line_index = 0
            else:
                line_index+=1
        list_of_lines_per_gen.append(list_of_lines_one_gen)
        #print(len(list_of_lines_one_gen))
    return list_of_lines_per_gen


#computes qunatifying selection points to plot
def compute_qsp_data(qsp_lines):
    kendall_tau_list = []
    for generation in range (0, number_of_generations-1):

        all_id_data = get_index_data(qsp_lines[generation], 6)
        all_unique_id_data = list(set(all_id_data))
        counted_id_data = collections.Counter(all_unique_id_data)
        for x in counted_id_data:
            counted_id_data[x] = 0

        no_parents_data = no_parents(qsp_lines[generation])
        counted_parents_1 = collections.Counter(get_index_data(qsp_lines[generation+1], 7))
        counted_parents_2 = collections.Counter(get_index_data(qsp_lines[generation+1], 8))

        counted_total = counted_id_data

        counted_total.update(counted_parents_1)
        counted_total.update(counted_parents_2)
        counted_total.update(no_parents_data)

        counted_clean = remove_junk_from_list(counted_total)


        fitness_dictionary = get_fitness_dictionary(qsp_lines[generation])
        #print(len(fitness_dictionary))
        occurence_dictionary = get_occurence_dictionary(counted_clean.items())
        #print(len(occurence_dictionary))


        kendall_tau_one_gen = compute_kendall_tau(fitness_dictionary, occurence_dictionary)
        kendall_tau_list.append(kendall_tau_one_gen)
    return kendall_tau_list


#removes specified value from list
def remove_junk_from_list(the_list):
    del the_list['-1']
    del the_list['-2']
    #for value in the_list:
        #if int(value) != val:
            #list_of_stuff.append(value)
    return the_list


#computes Kendall Tau for one generation and returns result
def compute_kendall_tau(fitness_dictionary, occurence_dictionary):
    fitness_all_controllers = []
    occurence_all_controllers = []
    for key in fitness_dictionary:
        fitness_all_controllers.append(fitness_dictionary[key])
        occurence_all_controllers.append(occurence_dictionary[key])

    kendall_tau, p_value = stats.kendalltau(fitness_all_controllers, occurence_all_controllers)
    return kendall_tau


#plots the simple graphs of fitness, nodes, edges and species
def plot_simple_graphs():
    main_directory = directory

    fitness_list_runs = []
    node_list_runs = []
    edge_list_runs = []
    species_list_runs = []

    number = 0
    for run in sorted_nicely(os.listdir(main_directory)):
        fitness_list = []
        node_list = []
        edge_list = []
        species_list = []

        folder_name = run

        if not (run.startswith(".")):
            # print(folder_name + "FOLDER_NAME")
            inner_directory = os.path.join(main_directory, run)
            for file in os.listdir(inner_directory):
                if file.endswith(".txt"):
                    #print(folder_name + " FOLDER_NAME")
                    #print("\n" + file)
                    file_name = os.path.join(inner_directory, file)

                    tuple_data = get_data_tuples(file_name)
                    fitness_list.append(tuple_data.fitness_data)
                    node_list.append(tuple_data.node_data)
                    edge_list.append(tuple_data.edge_data)
                    species_list.append(tuple_data.species_data)



            fitness_list_runs.append(fitness_list)
            node_list_runs.append(node_list)
            edge_list_runs.append(edge_list)
            species_list_runs.append(species_list)


    #plot_all_graphs(fitness_list_runs, node_list_runs, edge_list_runs, species_list_runs)



# returns a alphanumerical list
def sorted_nicely(l):
    """ Sorts the given iterable in the way that is expected.

    Required arguments:
    l -- The iterable to be sorted.

    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


# checks wether the correct number of arguments has been passed
def check_argument_count():
    if (len(sys.argv) == 6):
        initialise_global_variables()
    else:
        print("ERROR: Incorrect number of arguments.")
        print(
            "Try format: collection_of_runs.py <number of robots> <number of controllers> <number of generations> <number of runs> <data_directory>")
        sys.exit()


#initialises the global variables
def initialise_global_variables():
    # global variables of the system arguments
    global number_of_robots
    number_of_robots = int(sys.argv[1])
    global number_of_controllers
    number_of_controllers = int(sys.argv[2])
    global number_of_generations
    number_of_generations = int(sys.argv[3])
    global number_of_controllers_per_robot
    number_of_controllers_per_robot = int(number_of_controllers / number_of_robots)
    global number_of_runs
    number_of_runs = int(sys.argv[4])
    global directory
    directory = sys.argv[5]


# gets all data tuples
def get_data_tuples(name):
    all_data = []
    # opens and reads file
    file = open(name, "r")
    file_lines = file.readlines()

    # splits data
    all_fitness_data = split_data(file_lines, 2)
    all_node_data = split_data(file_lines, 3)
    all_edge_data = split_data(file_lines, 4)
    all_species_data = split_data(file_lines, 5)


    # transforms string data to values
    fitness_controllers = create_controller(all_fitness_data)
    node_controllers = create_controller(all_node_data)
    edge_controllers = create_controller(all_edge_data)
    species_controllers = create_controller(all_species_data)

    # closes the file
    close_file(file)

    #robot_values = robot_data_lists(fitness_controllers, node_controllers, edge_controllers, species_controllers)
    robot_values = robot_data_lists(fitness_controllers, node_controllers, edge_controllers, species_controllers)

    return robot_values


#takes one generation of a run and returns all its data on the given index in a list
def get_index_data(run_data, index):
    data_length = len(run_data)
    index_data = []
    for line in range(0, data_length):
        index_data.append(run_data[line][index])
    #print(index_data)

    return index_data


# splits raw data in a list of plottable data(requires a tab seperated data list)
def split_data(lines, num):
    data = []
    for line in lines:
        no_tabs = line.split('\t')
        data.append(no_tabs[num])
    return data


#returns a collection of ID's with no parents who have occurence of 2
def no_parents(lines):
    data = []
    for line in lines:
        if line[7] == "-1" and line[8] == "-1" and line[0] != "1":
            data.append(line[6])
    collection = collections.Counter(data)
    #adds 1 to occurence
    for x in collection:
        collection[x] = collection[x] + 1
    return collection


#returns a dictionary of fitness values and ID's as keys
def get_fitness_dictionary(lines):
    dictionary = {}
    for line in lines:
        key = line[6]
        value = line[2]
        dictionary[key] = value
    #print(len(dictionary))
    return dictionary


#returns a dictionary of occurence values
def get_occurence_dictionary(items):
    dictionary = {}
    for item in items:
        key = item[0]
        value = item[1]
        dictionary[key] = value
    return dictionary


# creates controller data  for plotting
def create_controller(data):
    list_of_controllers = []

    for i in range(0, number_of_generations):
        controller_list_one_generation = []
        for j in range(0, number_of_controllers_per_robot):
            temp = ast.literal_eval(data[(i * 3) + j])
            controller_list_one_generation.append(temp)

        list_of_controllers.append(controller_list_one_generation)

    return list_of_controllers



# plots the data from all robots combined
def plot_all_graphs(fitness_values, node_values, edge_values, species_values):
    # data_values

    # first quartile
    fitness_first_quartile_values = []
    nodes_first_quartile_values = []
    edges_first_quartile_values = []
    species_first_quartile_values = []

    # median
    fitness_median_values = []
    nodes_median_values = []
    edges_median_values = []
    species_median_values = []

    # third quartile
    fitness_third_quartile_values = []
    nodes_third_quartile_values = []
    edges_third_quartile_values = []
    species_third_quartile_values = []

    print("TIME")
    print(len(fitness_values))
    print("FOR")
    print(len(fitness_values[0]))
    print("A GIANT")
    print(len(fitness_values[0][0]))
    print("SHORTCUT")
    print(len(fitness_values[0][0][0]))
    print("Like damn this helped")

    for gen_number in range(0, number_of_generations):
        fitness_of_gen = []
        nodes_of_gen = []
        edges_of_gen = []
        species_of_gen = []
        for run_number in range(0, number_of_runs):
            for robot_count in range(0, number_of_robots):
                for controller in range(0, number_of_controllers_per_robot):
                    # inside robot j the controller k of that robot at generation i
                    fitness_of_gen.append(fitness_values[run_number][robot_count][gen_number][controller])
                    nodes_of_gen.append(node_values[run_number][robot_count][gen_number][controller])
                    edges_of_gen.append(edge_values[run_number][robot_count][gen_number][controller])
                    species_of_gen.append(species_values[run_number][robot_count][gen_number][controller])

        # First quartile
        first_quartile_fitness_gen = np.percentile(fitness_of_gen, 25)
        first_quartile_nodes_gen = np.percentile(nodes_of_gen, 25)
        first_quartile_edges_gen = np.percentile(edges_of_gen, 25)
        first_quartile_species_gen = np.percentile(species_of_gen, 25)

        fitness_first_quartile_values.append(first_quartile_fitness_gen)
        nodes_first_quartile_values.append(first_quartile_nodes_gen)
        edges_first_quartile_values.append(first_quartile_edges_gen)
        species_first_quartile_values.append(first_quartile_species_gen)

        # median
        median_fitness_of_gen = statistics.median(fitness_of_gen)
        median_nodes_of_gen = statistics.median(nodes_of_gen)
        median_edges_of_gen = statistics.median(edges_of_gen)
        median_species_of_gen = statistics.median(species_of_gen)

        fitness_median_values.append(median_fitness_of_gen)
        nodes_median_values.append(median_nodes_of_gen)
        edges_median_values.append(median_edges_of_gen)
        species_median_values.append(median_species_of_gen)

        # third quartile
        third_quartile_fitness_gen = np.percentile(fitness_of_gen, 75)
        third_quartile_nodes_gen = np.percentile(nodes_of_gen, 75)
        third_quartile_edges_gen = np.percentile(edges_of_gen, 75)
        third_quartile_species_gen = np.percentile(species_of_gen, 75)

        fitness_third_quartile_values.append(third_quartile_fitness_gen)
        nodes_third_quartile_values.append(third_quartile_nodes_gen)
        edges_third_quartile_values.append(third_quartile_edges_gen)
        species_third_quartile_values.append(third_quartile_species_gen)

    plot_graph(fitness_first_quartile_values, fitness_median_values, fitness_third_quartile_values, "Fitness ")
    plot_graph(nodes_first_quartile_values, nodes_median_values, nodes_third_quartile_values, "Nodes ")
    plot_graph(edges_first_quartile_values, edges_median_values, edges_third_quartile_values, "Edges ")
    plot_graph(species_first_quartile_values, species_median_values, species_third_quartile_values, "Species ")


# plots value data into 3 controllers
def plot_graph(data_first_quartile, data_median, data_third_quartile, graph_type):
    generation = list(range(0, number_of_generations))

    print(graph_type + " GRAPH TYPE")

    label_name_Q1 = '$y = {} Q1'.format(graph_type)
    label_name = '$y = {} median'.format(graph_type)
    label_name_Q3 = '$y = {} Q3'.format(graph_type)

    figure_name = 'Amazing_plot of {} of {} robots of all {} runs(quartile) .png'.format(graph_type, number_of_robots,
                                                                                         number_of_runs)
    figure = plt.figure()
    ax = plt.subplot(111)

    # only needed for fitness
    if graph_type == "Fitness ":
        axes = plt.gca()
        axes.set_ylim([0, 400])
    ax.plot(generation, data_first_quartile, label=label_name_Q1)
    ax.plot(generation, data_median, label=label_name)
    ax.plot(generation, data_third_quartile, label=label_name_Q3)
    plt.title('median of {} '.format(graph_type))
    ax.legend(loc="upper left")
    figure.savefig(figure_name)
    plt.close


def plot_qsp(qsp_data, folder_name):
    generation = list(range(0, number_of_generations-1))
    figure_name = 'QSP(full) of {} .png'.format(folder_name)

    figure = plt.figure()
    ax = plt.subplot(111)

    ax.plot(generation, qsp_data, label = " Quantifying Selection Pressure")
    plt.title('Qsp of {} '.format(folder_name))
    ax.legend(loc="upper left")
    figure.savefig(figure_name)
    plt.close()

'''
def plot_barchart(parents, run_number):
    summed_parents = sum(parents, collections.Counter())

    labels, values = zip(*summed_parents.items())

    indexes = np.arange(len(labels))
    width = 1

    #fig, ax1 = plt.subplots(1)
    fig, ax1 = plt.subplots(1, figsize=(12, 6))

    plt.title('Quantifying selection pressure {}'.format(run_number))

    plt.grid(b=True)
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.xticks(rotation=90, fontsize = 6)

    figure_name = ('Barchart {}.png'.format(run_number))
    fig.savefig(figure_name)

'''



def close_file(file):
    file.close()


# Calls main function
main()

