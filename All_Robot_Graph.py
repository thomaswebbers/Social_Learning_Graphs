#This code prints plots a graph of the fitness inside a single robot
import matplotlib.pyplot as plt
import ast
import collections
import os
import Controller_tuple
import Robot_data
import statistics

#main function
def main():
    #Robot_data = collections.namedtuple('data_values', ['fitness_data', 'node_data', 'edge_data', 'species_data'])
    #robot_list = []
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

    print("FOO")
    plot_all_robots(fitness_list,node_list,edge_list,species_list)


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

    #Robot_data = collections.namedtuple('data_values', ['fitness_data', 'node_data', 'edge_data', 'species_data'])
    robot_values = Robot_data.data_container(fitness_controllers, node_controllers, edge_controllers, species_controllers)

    #controller_values.fitness_data
    return robot_values


#plots the data from all robots combined
def plot_all_robots(fitness_values,node_values,edge_values,species_values):
    print("BAR")

    #data_values
    fitness_median_values = []
    node_median_values = []
    edge_median_values = []
    species_median_values = []
    for i in range(0,26):
        fitness_of_gen = []
        for j in range(0,8):
            fitness_of_gen.append(fitness_values[j].controller1[i])
            fitness_of_gen.append(fitness_values[j].controller2[i])
            fitness_of_gen.append(fitness_values[j].controller3[i])
        median_of_gen = statistics.median(fitness_of_gen)
        fitness_median_values.append(median_of_gen)


        nodes_of_gen = []
        for j in range(0,8):
            nodes_of_gen.append(node_values[j].controller1[i])
            nodes_of_gen.append(node_values[j].controller2[i])
            nodes_of_gen.append(node_values[j].controller3[i])
        median_of_gen = statistics.median(nodes_of_gen)
        node_median_values.append(median_of_gen)


        edges_of_gen = []
        for j in range(0,8):
            edges_of_gen.append(edge_values[j].controller1[i])
            edges_of_gen.append(edge_values[j].controller2[i])
            edges_of_gen.append(edge_values[j].controller3[i])
        median_of_gen = statistics.median(edges_of_gen)
        edge_median_values.append(median_of_gen)


        species_of_gen = []
        for j in range(0,8):
            species_of_gen.append(species_values[j].controller1[i])
            species_of_gen.append(species_values[j].controller2[i])
            species_of_gen.append(species_values[j].controller3[i])
        median_of_gen = statistics.median(species_of_gen)
        species_median_values.append(median_of_gen)

    print("BRO?")

    plot_graph(fitness_median_values, "Fitness_median")
    plot_graph(node_median_values, "Nodes_median")
    plot_graph(edge_median_values, "Edges_median")
    plot_graph(species_median_values, "Species_median")


#function open file and reads it in as lines
'''
def open_file():
    file = open("odNEAT_Foraging_ExperimentID8_G_192.168.1.32_30-04-18_09-07_cleanlog.txt", "r")
    file_lines = file.readlines()
    return file_lines
'''


#splits raw data in a list of plottable data(requires a tab seperated data list)
def split_data(lines, num):
    data = []
    for line in lines:
        no_tabs = line.split('\t')
        data.append(no_tabs[num])
    return data


#creates controller data and average data for plotting
def create_controller(data):
    #Controllers = collections.namedtuple('Controllers',['controller1', 'controller2', 'controller3', 'controller_average'])
    controller1 = []
    controller2 = []
    controller3 = []
    controller_average = []


    for i in range (0, 26):
        var1 = ast.literal_eval(data[i*3])
        var2 = ast.literal_eval(data[(i*3) + 1])
        var3 = ast.literal_eval(data[(i*3) + 2])
        average = (var1 + var2 + var3) / 3

        controller1.append(var1)
        controller2.append(var2)
        controller3.append(var3)
        controller_average.append(average)

    #controller_values = Controllers(controller1, controller2, controller3, controller_average)
    controller_values = Controller_tuple.Controllers(controller1, controller2, controller3, controller_average)

    return controller_values


#plots value data into 3 controllers
def plot_graph(data_values, type):
    generation = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

    label_name = '$y = {}'.format(type)
    figure_name = 'MEDIAN_graph_plot of {}.png'.format(type)
    figure = plt.figure()
    ax = plt.subplot(111)
    ax.plot(generation, data_values, label=label_name)
    plt.title('median of {} '.format(type))
    ax.legend()
    figure.savefig(figure_name)


def close_file(file):
    file.close()



#Calls main function
main()



