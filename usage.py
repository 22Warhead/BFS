from websocket import isEnabledForDebug


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state=state
        self.parent=parent
        self.action=action


class Frontier:
    def __init__(self):
        self.frontier = []


    def isEmpty(self):
        return len(self.frontier) == 0

    def add(self, node):
        self.frontier.append(node)

    def contain(self, state):
        return any(i.state == state for i in self.frontier)

    def remove(self):
        pass

class StackFrontier(Frontier):
    def remove(self):
        if self.isEmpty():
            raise Exception("Empty frontier")

        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node


class QueueFrontier(Frontier):
    def remove(self):
        if self.isEmpty():
            raise Exception("Empty frontier")

        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node
