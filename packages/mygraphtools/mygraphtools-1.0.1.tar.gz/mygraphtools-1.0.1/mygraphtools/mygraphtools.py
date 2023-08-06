from functools import reduce


class UnionFind():
    def __init__(self, vertices):
        self.boss = [x for x in range(vertices)]
        self.size = [1 for x in range(vertices)]

    def find(self, vertex):
        copyV = vertex
        while copyV != self.boss[copyV]:
            copyV = self.boss[copyV]
        return copyV

    def union(self, vertexV, vertexW):
        if self.size[vertexV] < self.size[vertexW]:
            self.boss[vertexV] = vertexW
            self.size[vertexW] += self.size[vertexV]
        else:
            self.boss[vertexW] = vertexV
            self.size[vertexV] += self.size[vertexW]


class Graph():

    def __init__(self, directed,  weighted):
        self.weighted = weighted
        self.directed = directed
        self.edges = []
        self.vertices = []
        if weighted:
            self.mst = []
            self.mstcost = 0

    def __addvertice(self, args):
        for vertex in args[:2]:
            if not vertex in self.vertices:
                self.vertices.append(vertex)

    def __edgeAlreadyExist(self, edge):
        vertexV, vertexW = edge[0], edge[1]
        for edge in self.edges:
            if vertexV == edge[0] and vertexW == edge[1]:
                if self.directed:
                    return True
            elif not self.directed:
                if vertexV == edge[1] and vertexW == edge[0]:
                    return True
        return False

    def addedge(self, *args):
        if self.weighted and len(args) != 3 or not self.weighted and len(args) != 2:
            print('Failed to add edge: invalid arguments')
            return
        else:
            if self.__edgeAlreadyExist(args):
                print('The edge', args, 'already exists')
                return
            elif self.weighted and len(args) == 3:
                self.edges.append(args)
            else:
                self.edges.append(args)
        self.__addvertice(args)

    def cost(self):
        if not self.weighted:
            return 0
        else:
            def adder(elem, elem_): return elem + elem_
            costs = list(map(lambda edge: edge[-1], self.edges))
            return reduce(adder, costs)

    def numedges(self):
        return len(self.edges)

    def numvertices(self):
        return len(self.vertices)

    def __freeMST(self):
        self.mst = []
        self.mstCost = 0

    def __sortEdgesByCost(self):
        self.edges.sort(key=lambda edge: edge[-1])

    def adjacentvertices(self, vertex):
        adjacencyList = []
        for edge in self.edges:
            if edge[0] == vertex:
                adjacencyList.append(edge[1])
            elif not self.directed:
                if edge[1] == vertex:
                    adjacencyList.append(edge[0])
        return adjacencyList

    def adjacentedges(self, vertex):
        adjacencyList = []
        for edge in self.edges:
            if not self.directed:
                if vertex in edge:
                    adjacencyList.append(edge)
            else:
                if vertex == edge[0]:
                    adjacencyList.append(edge)
        return adjacencyList

    def degree(self, vertex):
        pass

    def calculatemst(self):
        if not self.weighted or self.directed:
            return []
        else:
            self.__freeMST()
            UF = UnionFind(self.numvertices())
            self.__sortEdgesByCost()

            for edge in self.edges:
                vertexV = UF.find(edge[0])
                vertexW = UF.find(edge[1])
                if vertexV != vertexW:
                    UF.union(vertexV, vertexW)
                    self.mst.append(edge)
                    self.mstcost += edge[-1]
        return self.mst
