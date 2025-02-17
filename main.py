from usage import QueueFrontier, Node
from PIL import Image, ImageDraw


class Maze:
    def __init__(self, filename):
        self.goal = None
        self.start = None
        self.wall = None
        self.width = None
        self.height = None
        self.explored = 0
        self.solution = None
        self.visited = set()
        self.data = self.fetchData(filename)

    def fetchData(self, filename):
        with open(filename) as f:
            data = f.read()

        if data.count("A") != 1:
            raise Exception("Only one starting point expected")

        if data.count("B") != 1:
            raise Exception("Only one goal point expected")

        data = data.splitlines()
        self.height = len(data)
        self.width = max(len(i) for i in data)
        self.wall = []
        for i in range(self.height):
            row = []
            try:
                for j in range(self.width):
                    if data[i][j] == " ":
                        row.append(False)
                    elif data[i][j] == "A":
                        row.append(False)
                        self.start=(i, j)
                    elif data[i][j] == "B":
                        row.append(False)
                        self.goal = (i, j)
                    else:
                        row.append(True)
            except IndexError:
                row.append(False)
            self.wall.append(row)
        return data

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.wall):
            for j, col in enumerate(row):
                if self.wall[i][j]:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def solve(self):
        node = Node(state=self.start)
        frontier = QueueFrontier()
        frontier.add(node)
        while True:
            if frontier.isEmpty():
                raise Exception("No Solution Available")

            node = frontier.remove()
            self.explored += 1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            self.visited.add(node.state)
            for action, state in self.neighbours(node.state):
                child = Node(action = action, state=state, parent=node)
                frontier.add(child)



    def neighbours(self, state):
        r, c = state
        actions = (
            ("up", (r-1, c)),
            ("down", (r+1, c)),
            ("right", (r, c+1)),
            ("left", (r, c-1)),
        )
        possible = []
        for action, (i, j) in actions:
            if 0 <= i < self.height and 0 <= j < self.width and not self.wall[i][j] and (i, j) not in self.visited:
                possible.append((action, (i, j)))
        return possible

    def outputImage(self, filename):
        size=40
        border = 10
        img = Image.new("RGBA", (size*self.height, size*self.width), "black")

        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.wall):
            for j, col in enumerate(row):
                if self.wall[i][j]:
                    fil = (50, 50, 50)
                elif (i, j) == self.start:
                    fil = (0, 255, 0)
                elif (i, j) == self.goal:
                    fil = (0, 0, 255)
                elif solution is not None and (i, j) in solution:
                    fil = (255, 255, 0)
                else:
                    fil = (255, 255, 255)
                draw.rectangle(
                    ([(j*size + border, i*size + border), ((j+1)*size - border, (i+1)*size - border)]), fill = fil
                )
        img.save("bfs"+filename+'.png')

name = "maze1"
m = Maze(name+'.txt')

m.print()
print("Solving---")
m.solve()
print("No, of explored state: ", m.explored, "\n")
m.print()
m.outputImage(name)
