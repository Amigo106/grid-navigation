import argparse as ap

import re

import platform

from pathfinder import PathFinder


######## RUNNING THE CODE ####################################################

#   You can run this code from terminal by executing the following command

#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag>

#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0

###############################################################################


def graphsearch(map, flag):

    # get and remove grid size which is first element in map and consider only other input lines
    grid_size = int(map.pop(0).rstrip())

    # call get_grid_rows_start_end_position which derives start, end position as tuples and a list of list of 0s and
    # 1s representing input map, here 1 represents mountain/obstacle
    grid_start_end_position = get_grid_rows_start_end_position(map)

    maze = grid_start_end_position[0]
    start_position = grid_start_end_position[1]
    end_position = grid_start_end_position[2]

    # validate input to check whether it is NxN grid of given size
    valid_input = validate_input(maze, grid_size)

    if not valid_input:
        print('Invalid-Input. Grid size not matching with number of columns or rows.')
        return 'INVALID-INPUT'

    # call astar function which gives solution for shortest path between start and end position
    solution = PathFinder.astar(maze, start_position, end_position, flag)

    if solution is None:
        return "NO-PATH"

    # call get_output_string which converts the solution to required output format
    output_string = get_output_string(map, grid_size, solution)

    return output_string


def validate_input(maze, grid_size):
    for element in maze:
        if len(element) != grid_size:
            return False
    return True


def get_grid_rows_start_end_position(map):
    start_position = ()
    end_position = ()
    grid_rows_list = []

    i = 0
    for line in map:
        line = line.rstrip()
        j = 0
        maze_element = []
        for element in line:
            if element == 'S':
                start_position += (i, j)
                maze_element.append(0)
            elif element == 'G':
                end_position += (i, j)
                maze_element.append(0)
            elif element == 'R':
                maze_element.append(0)
            elif element == 'X':
                maze_element.append(1)
            j = j + 1
        grid_rows_list.append(maze_element)
        i = i + 1

    return grid_rows_list, start_position, end_position


def get_output_string(map, grid_size, solution):
    input_dict = {}
    i = 0
    for line in map:
        line = line.rstrip()
        j = 0
        for element in line:
            input_dict[(i, j)] = element
            j = j + 1
        i = i + 1

    output_string = ''
    path = solution[0]
    flow = solution[1]
    flow_cost = solution[2]
    i = 0
    for position in path:
        j = 1
        for key, value in input_dict.items():
            if key == position and value != 'S' and value != 'G':
                output_string += '*'
            else:
                output_string += value
            if j % grid_size == 0:
                output_string += '\n'
            j += 1
        output_string += '\n'
        output_string += flow[i]
        if i == len(path) - 1:
            output_string += '-G'
        output_string += ' ' + str(flow_cost[i])
        output_string += '\n\n'
        i += 1

    return output_string[:-1]  # remove last \n character


def read_from_file(file_name):

    # read input file as map with each line as an element

    file_handle = open(file_name)

    map = file_handle.readlines()

    return map


def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')

    file_handle.write(solution)


def main():
    # create a parser object

    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline

    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)

    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)

    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)

    # get all the arguments

    arguments = parser.parse_args()

    ##############################################################################

    # these print statements are here to check if the arguments are correct.

    #    print("The input_file_name is " + arguments.input_file_name)

    #    print("The output_file_name is " + arguments.output_file_name)

    #    print("The flag is " + str(arguments.flag))

    #    print("The procedure_name is " + arguments.procedure_name)

    ##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("\\")

        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("\\")

        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")

            return -1

    else:

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("/")

        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("/")

        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")

            return -1

    flag = arguments.flag

    # procedure_name = arguments.procedure_name

    try:

        # call read_from_file which reads input file as map with each line as an element
        map = read_from_file(input_file_name)

    except FileNotFoundError:

        print("input file is not present")

        return -1

    # call graphsearch which have implementation to find solution in required format for given input
    solution_string = graphsearch(map, flag)

    write_flag = 1

    if write_flag == 1:
        # write solution to output file
        write_to_file(output_file_name, solution_string)


if __name__ == "__main__":
    main()

