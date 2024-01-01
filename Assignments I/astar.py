class Graph:

    def __init__(self, directed=False):
        self._outgoing = {}
        # If the graph is undirected, 'self._outgoing'
        # is the universal storage.
        self._incoming = {} if directed else self._outgoing

    # If the graph is directed, the 'self._incoming' 
    # dictionary differs from the 'self._outgoing'.
    def is_directed(self):
        return self._incoming is not self._outgoing

    # The function returns a generator of incoming
    # or outgoing (default) edges of a vertex.
    def adjacent_edges(self, vertex, outgoing=True):
        # References the corresponding outer dictionary
        # (dictionary of dictionaries)
        adj_edges = self._outgoing if outgoing else self._incoming

        # Access each of the edges for this endpoint vertex.
        for edge in adj_edges[vertex].values():
            yield edge

    def add_vertex(self, entity=None, h=None, cost=None):
        # Constructs a new vertex from the entity.
        vertex = self.Vertex(entity, h, cost)
        # The vertex becomes a key in the outer dictionary,
        # but the value is an internal dictionary (as we model
        # both dimensions for each edge: origin and destination).
        # e.g. {vertex_1a:{vertex_b:edge_a_b}, vertex_b:{vertex_c:edge_b_c}}.
        self._outgoing[vertex] = {}
        if self.is_directed():
            self._incoming[vertex] = {}

    def add_edge(self, origin, destination, weight=None):
        # Constructs a new edge from the vertices.
        edge = self.Edge(origin, destination, weight)
        # Adds the edge to the dictionary (dictionaries are
        # the same if the graph is undirected). The outer key
        # represents the origin, i.e. the component 'a' of
        # the edge-defining pair (a, b). The inner key stands
        # for the component 'b' of the edge-defining pair (a, b).
        self._outgoing[origin][destination] = edge
        # Even if the graph is undirected, each edge has to
        # be added twice, i.e. once for each of its endpoints.
        self._incoming[destination][origin] = edge

    def vertices(self):
        return self._outgoing.keys()

    def edges(self):
        # All the edges are collected into a set.
        result = set()
        for inner_dict in self._outgoing.values():
            result.update(inner_dict.values())
        return result

    class Vertex:
        __slots__ = '_entity', '_h', '_cost'

        def __init__(self, entity, h=None, cost=None):
            self.entity = entity
            self.h = h
            self.cost = cost

        # The real-world entity is represented by the Vertex object.
        @property
        def entity(self):
            return self._entity

        @entity.setter
        def entity(self, entity):
            self._entity = entity

        # The real-world entity has a heuristic value of 'h'.
        @property
        def h(self):
            return self._h

        @h.setter
        def h(self, h):
            self._h = h

        # The real-world entity has a cost of 'cost'.
        @property
        def cost(self):
            return self._cost

        @cost.setter
        def cost(self, cost):
            self._cost = cost

        # We have to implement __hash__ to use the object as a dictionary key.
        def __hash__(self):
            return hash(id(self))

        def __lt__(self, other):
            if self.cost is None:
                return False
            elif other.cost is None:
                return True
            else:
                return self.cost < other.cost

    class Edge:
        __slots__ = '_origin', '_destination', '_weight'

        def __init__(self, origin, destination, weight=None):
            self._origin = origin
            self._destination = destination
            self.weight = weight

        def endpoints(self):
            return self._origin, self._destination

        # Returns the other component of the edge-defining pair (a, b)
        # for a given component a or b, respectively.
        def opposite(self, vertex):
            return self._destination if self._origin is vertex \
                else self._origin

        # Returns the weight of the edge.
        @property
        def weight(self):
            return self._weight

        # Sets the weight of the edge
        @weight.setter
        def weight(self, weight):
            self._weight = weight

        def __hash__(self):
            return hash((self._origin, self._destination))