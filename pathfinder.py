from node import Node


class ContinueChildren(Exception):
    pass


class PathFinder():

    @staticmethod
    def astar(maze, start, end, flag):
        """Returns a list of positions/tuples as path from the given start to the given end, list of action performed for reaching
            a position in path and list of cost for reaching a position in path"""

        # initialize node_identifier_count for maintaining unique identifier for each node
        # initialize node_print_count for printing current node, children, open and closed nodes details in console
        # during each iteration but until it exceeds flag count
        node_identifier_count = 0
        node_print_count = 1

        # Create start and goal/end node
        start_node = Node(None, start, 'S', 'N' + str(node_identifier_count), 0)
        node_identifier_count = node_identifier_count + 1
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed nodes list
        open_nodes = []
        closed_nodes = []

        # Add the start node
        open_nodes.append(start_node)

        # Loop until you find the end
        while len(open_nodes) > 0:

            # Get the current node
            current_node = open_nodes[0]
            current_index = 0
            for index, item in enumerate(open_nodes):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current node off open list, add to closed list
            open_nodes.pop(current_index)
            closed_nodes.append(current_node)

            if flag >= node_print_count:
                print(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                flow = []
                flow_cost = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    flow.append(current.flow)
                    flow_cost.append(current.flow_cost)
                    current = current.parent
                return path[::-1], flow[::-1], flow_cost[::-1]  # Return reversed lists

            # Generate children
            children = []
            new_positions = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0), 'LU': (-1, -1), 'RU': (-1, 1),
                             'LD': (1, -1), 'RD': (1, 1)}
            available_positions = new_positions.copy()
            for key, value in new_positions.items():
                node_position = (current_node.position[0] + value[0], current_node.position[1] + value[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    available_positions.pop(key, None)
                    continue

                # Make sure walkable position
                if maze[node_position[0]][node_position[1]] != 0:
                    available_positions.pop(key, None)
                    if key == 'L':
                        available_positions.pop('LU', None)
                        available_positions.pop('LD', None)
                    elif key == 'U':
                        available_positions.pop('LU', None)
                        available_positions.pop('RU', None)
                    elif key == 'R':
                        available_positions.pop('RU', None)
                        available_positions.pop('RD', None)
                    elif key == 'D':
                        available_positions.pop('RD', None)
                        available_positions.pop('LD', None)

            # Create new nodes
            for key, value in available_positions.items():
                node_position = (current_node.position[0] + value[0], current_node.position[1] + value[1])
                cost = calculate_cost(key)
                new_node = Node(current_node, node_position, key, 'N' + str(node_identifier_count), cost)
                node_identifier_count = node_identifier_count + 1
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                try:
                    for closed_child in closed_nodes:
                        if child == closed_child:
                            raise ContinueChildren
                except ContinueChildren:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                try:
                    for open_node in open_nodes:
                        if child == open_node and child.g > open_node.g:
                            raise ContinueChildren
                except ContinueChildren:
                    continue

                # Add the child to the open list
                open_nodes.append(child)

            if flag >= node_print_count:
                print('Children: ' + str(children))
                print('OPEN: ' + str(open_nodes))
                print('Closed: ' + str(closed_nodes))
                print()

            node_print_count = node_print_count + 1


def calculate_cost(action):
    cost = 0
    if (action == 'R') or (action == 'L') or (action == 'U') or (action == 'D'):
        cost = cost + 2
    elif (action == 'LU') or (action == 'RU') or (action == 'LD') or (action == 'RD'):
        cost = cost + 1
    return cost
