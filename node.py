class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, action=None, identifier=None, cost=None):
        self.parent = parent
        self.position = position
        self.action = action
        self.identifier = identifier
        self.flow = action
        self.flow_cost = cost
        if parent is not None:
            self.flow = parent.flow + "-" + action
        if parent is not None:
            self.flow_cost = parent.flow_cost + cost
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return "%s:%s %s %d %d %d %d" % (
        self.identifier, self.flow, self.action, self.flow_cost, self.g, self.h, self.f)