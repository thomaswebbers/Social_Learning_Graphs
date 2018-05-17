#This code prints plots a graph of the fitness inside a single robot
import matplotlib.pyplot as plt
import ast
import collections
import os
import Robot_data
import statistics
import sys
from robot_data_lists import *

#global variables of the system arguments
number_of_robots = None
number_of_controllers = None
number_of_generations = None
number_of_controllers_per_robot = 0


#main function
def main():
    check_argument_count()
    directory = "./Data_Directory"
    fitness_list = []
    node_list = []
    edge_list = []
    species_list = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            #print(os.path.join("./Data_Directory", file))
            file_name = os.path.join(directory, file)

            tuple_data = get_data_tuples(file_name)
            fitness_list.append(tuple_data.fitness_data)
            node_list.append(tuple_data.node_data)
            edge_list.append(tuple_data.edge_data)
            species_list.append(tuple_data.species_data)

    #print(fitness_list[0][0])
    plot_all_robots(fitness_list,node_list,edge_list,species_list)


def check_argument_count():
    if(len(sys.argv) == 4):
        initialise_global_variables()
    else:
        print("Incorrect number of arguments.")
        print("Try format: robot_median_generic.py <number of robots> <number of controllers> <number of generations>")
        sys.exit()

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


#gets all data tuples
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

    #closes the file
    close_file(file)

    robot_values =  robot_data_lists(fitness_controllers, node_controllers, edge_controllers, species_controllers)
    #print(robot_values.fitness_data[0])

    return robot_values


#plots the data from all robots combined
def plot_all_robots(fitness_values, node_values, edge_values, species_values):
    #data_values
    fitness_median_values = []
    node_median_values = []
    edge_median_values = []
    species_median_values = []

    print("TIME")
    print(len(fitness_values))
    print("FOR")
    print(len(fitness_values[0]))
    print("A GIANT")
    print(len(fitness_values[0][0]))
    print("SHORTCUT")



    for gen_number in range(0, number_of_generations):
        fitness_of_gen = []
        nodes_of_gen = []
        edges_of_gen = []
        species_of_gen = []
        for robot_count in range(0, number_of_robots):
            for controller in range(0, number_of_controllers_per_robot):
                #inside robot j the controller k of that robot at generation i
                fitness_of_gen.append(fitness_values[robot_count][gen_number][controller])
                nodes_of_gen.append(node_values[robot_count][gen_number][controller])
                edges_of_gen.append(edge_values[robot_count][gen_number][controller])
                species_of_gen.append(species_values[robot_count][gen_number][controller])

        median_fitness_of_gen = statistics.median(fitness_of_gen)
        median_nodes_of_gen = statistics.median(nodes_of_gen)
        median_edges_of_gen = statistics.median(edges_of_gen)
        median_species_of_gen = statistics.median(species_of_gen)

        fitness_median_values.append(median_fitness_of_gen)
        node_median_values.append(median_nodes_of_gen)
        edge_median_values.append(median_edges_of_gen)
        species_median_values.append(median_species_of_gen)

    plot_graph(fitness_median_values, "Fitness_median")
    plot_graph(node_median_values, "Nodes_median")
    plot_graph(edge_median_values, "Edges_median")
    plot_graph(species_median_values, "Species_median")


#splits raw data in a list of plottable data(requires a tab seperated data list)
def split_data(lines, num):
    data = []
    for line in lines:
        no_tabs = line.split('\t')
        data.append(no_tabs[num])
    return data


#creates controller data and average data for plotting
def create_controller(data):
    list_of_controllers= []

    for i in range (0, number_of_generations):
        controller_list_one_generation = []
        for j in range(0, number_of_controllers_per_robot):
            temp = ast.literal_eval(data[(i*3)+j])
            controller_list_one_generation.append(temp)

        list_of_controllers.append(controller_list_one_generation)

    return list_of_controllers


#plots value data into 3 controllers
def plot_graph(data_values, graph_type):
    generation = list(range(0, 26))

    label_name = '$y = {}'.format(graph_type)
    figure_name = 'MEDIAN_GENERIC_graph_plot of {}.png'.format(graph_type)
    figure = plt.figure()
    ax = plt.subplot(111)
    ax.plot(generation, data_values, label=label_name)
    plt.title('median of {} '.format(graph_type))
    ax.legend()
    figure.savefig(figure_name)


def close_file(file):
    file.close()



#Calls main function
main()



