#This code prints plots a graph of the fitness inside a single robot
import matplotlib.pyplot as plt
import ast
import collections
import os

#main function
def main():
    robot_list = []
    directory = "./Data_Directory"
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            #print(os.path.join("./Data_Directory", file))
            file_name = os.path.join(directory, file)
            robot_number = get_robot_number(file)
            #print(file)
            #print(robot_number)
            plot_one_robot(file_name,robot_number)


#returns the robot number
def get_robot_number(text_file):
    robot_number = print_port_number(text_file)
    return robot_number

#splits file name in a name list
def print_port_number(name):
    name_element = name.split("_")
    name_list = name_element
    robot_number = print_robot_number(name_list[4])
    return robot_number

#uses the port number to find the robotnumber
def print_robot_number(port_number):
    port_elements = port_number.split(".")
    port_list = port_elements
    robot_number = port_list[3]
    return robot_number



#plots one robot
def plot_one_robot(name,robot_number):
    #opens file
    #file_lines = open_file()

    print(name)
    file = open(name, "r")
    file_lines = file.readlines()
    #return file_lines

    #splits data
    fitness_data = split_data(file_lines, 2)
    node_data = split_data(file_lines, 3)
    edge_data = split_data(file_lines, 4)
    species_data = split_data(file_lines, 5)

    #transforms string data to values
    fitness_values = create_controller(fitness_data)
    node_values = create_controller(node_data)
    edge_values = create_controller(edge_data)
    species_values = create_controller(species_data)

    #plot values
    plot_graph(fitness_values, "Fitness_mult", robot_number)
    plot_graph(node_values, "Nodes_mult", robot_number)
    plot_graph(edge_values, "Edges_mult", robot_number)
    plot_graph(species_values, "Species_mult", robot_number)

    close_file(file)



#function open file and reads it in as lines
'''
def open_file():
    file = open("odNEAT_Foraging_ExperimentID8_G_192.168.1.32_30-04-18_09-07_cleanlog.txt", "r")
    file_lines = file.readlines()
    return file_lines
'''


#splits raw data in a list of plottable data
def split_data(lines, num):
    data = []
    for line in lines:
        no_tabs = line.split('\t')
        data.append(no_tabs[num])
    return data


#creates controller data and average data for plotting
def create_controller(data):
    Controllers = collections.namedtuple('Controllers',['controller1', 'controller2', 'controller3', 'controller_average'])
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

    controller_values = Controllers(controller1, controller2, controller3, controller_average)
    return controller_values


#plots value data into 3 controllers
def plot_graph(data_values, type, robot_number):
    generation = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    controller1 = data_values.controller1
    controller2 = data_values.controller2
    controller3 = data_values.controller3
    controller_average = data_values.controller_average
    controller_list = [controller1, controller2, controller3, controller_average]

    number = 1
    for controller in controller_list:
        if number == 4:
            number_or_average = "average"
        else:
            number_or_average = number
        label_name = '$y = {}'.format(type)
        figure_name = 'graph_plot_{}_{}_{}.png'.format(type, number_or_average,robot_number)
        #figure_name ='graph_plot_{}_{}.png'.format(type, number_or_average)
        figure = plt.figure()
        ax = plt.subplot(111)
        ax.plot(generation, controller, label=label_name)
        plt.title('{} of controller {} in robot {}'.format(type, number_or_average,robot_number))
        ax.legend()
        figure.savefig(figure_name)
        #figure.savefig('test.png')
        number = number + 1



def close_file(file):
    file.close()




#Calls main function
main()



