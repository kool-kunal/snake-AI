# from Queue import PriorityQueue


def dist(x, y, px, py):
    return abs(x-px) + abs(y-py)

def getf(n):
    return n.f

class node:
    def __init__(self, x, y, parent=None, goal=None):
        if parent:
            self.parent = parent
        else:
            self.parent = None
        self.pos = [x, y]
        if goal:
            self.g = dist(x, y, parent.pos[0], parent.pos[1]) + parent.g
            self.h = dist(x, y, goal.pos[0], goal.pos[1])
            self.f = self.g + self.h
        else:
            self.g = 0
            self.h = 0
            self.f = 0


class search:
    def __init__(self, hx, hy, fx, fy, obstacle):
        self.start = node(x=hx, y=hy, parent=None, goal=None)
        self.target = node(x=fx, y=fy, parent=None, goal=None)
        self.obstacles = []
        self.open = []
        self.closed = []

        for i in obstacle:
            self.obstacles.append(i)
        for i in range(0, 500, 10):
            self.obstacles.append([i, 0])
            self.obstacles.append([0, i])
            self.obstacles.append([i, 500])
            self.obstacles.append([500, i])

    def neighbours(self, p):
        leftn = node(x=p.pos[0]-10, y=p.pos[1], parent=p, goal=self.target)
        rightn = node(x=p.pos[0]+10, y=p.pos[1], parent=p, goal=self.target)
        downn = node(x=p.pos[0], y=p.pos[1]+10, parent=p, goal=self.target)
        upn = node(x=p.pos[0], y=p.pos[1]-10, parent=p, goal=self.target)
        neigh = []
        neigh.append(leftn)
        neigh.append(rightn)
        neigh.append(downn)
        neigh.append(upn)

        for n in neigh:
            if n.pos == self.target.pos:
                self.target.parent = p
                return None

            for i in self.obstacles:
                if n.pos == i:
                    neigh.remove(n)
                    break

            for i in self.closed:
                if n.pos == i.pos:
                    if n in neigh:
                        neigh.remove(n)
                        break

            for i in self.open:
                if n.pos == i.pos:
                    newg = dist(n.pos[0],n.pos[1],p.pos[0],p.pos[1]) + p.g
                    if i.g > newg:
                        i.g = newg
                        i.parent = p
                    if n in neigh:
                        neigh.remove(n)

        return neigh

    def findPath(self):
        children = self.neighbours(self.start)
        if children == None:
            return 1
        for i in children:
            self.open.append(i)
        self.closed.append(self.start)
        # print("parent: ", end="")
        # print([self.start.pos,self.start.f])
        # print("children: ", end="")
        # for i in children:
        #     print([i.pos, i.f], end=" ")
        # print()
        # print("open: ", end="")
        # for i in self.open:
        #     print([i.pos,i.f], end=" ")
        # print()



        while len(self.open)>0:
            mine = min(self.open, key = getf)
            # print(mine.pos)
            self.open.remove(mine)
            self.closed.append(mine)
            children = self.neighbours(mine)
            if children == None:
                return 1
            if self.target in children:
                break
            for i in children:
                self.open.append(i)
            # print("parent: ", end="")
            # print([mine.pos,mine.f])
            # print("children: ", end="")
            # for i in children:
            #     print([i.pos,i.f], end=" ")
            # print()
            # print("open: ", end="")
            # for i in self.open:
            #     print([i.pos,i.f], end=" ")
            # print()
        return 0

    def getPath(self):
        self.findPath()
        path = []
        run = self.target
        while run is not self.start:
            path.append(run.pos)
            run = run.parent
        path.append(self.start.pos)
        print(path)
        return path
