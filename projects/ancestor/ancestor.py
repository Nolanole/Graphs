class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = {'parents': set(), 'children': set()}

    def add_edges(self, v1, v2):
        """
        Add edges to the graph: v1 = parent, v2 = child
        """
        if v1 not in self.vertices:
            self.add_vertex(v1)
        if v2 not in self.vertices:
            self.add_vertex(v2)
        self.vertices[v1]['children'].add(v2)
        self.vertices[v2]['parents'].add(v1)
    
    def create_graph_from_tuples(self, parent_child_tuples):
        for tup in parent_child_tuples:
            self.add_edges(tup[0], tup[1])

    def get_parents(self, vertex_id):
        """
        Get all parents of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]['parents']
        else:
            print('error- vertex does not exist')


def earliest_ancestor(ancestors, starting_node):
    #construct the graph: each vertex has set of parents and children
    g = Graph()
    g.create_graph_from_tuples(ancestors)

    #if starting node has no parents, return -1:
    if len(g.get_parents(starting_node)) == 0:
        return -1
    
    #initialize longest_path w/ just the starting node
    longest_path = [starting_node]
    #create a set to store the visited vertices
    visited = set()
    #create a stack:
    s = Stack()
    #push a path to the starting node
    s.push([starting_node])
    #while the stack is not empty:
    while s.size() > 0:
        #pop the latest path and assign to var
        path = s.pop()
        #grab the last node from the path:
        v = path[-1]
        #if the node has not yet been visited:
        if v not in visited:
            #mark it as visited
            visited.add(v)
            #check the node for parents:
            parents = g.get_parents(v)
            #if node has no parents- reached the full depth: check if the len of this path is >= prev longest path
            if len(parents) == 0:
                if len(path) > len(longest_path):
                    longest_path = path[:]
                if len(path) == len(longest_path):
                    #compare which earliest ancestor ha slowest numeric id:
                    if v < longest_path[-1]:
                        longest_path = path[:]
            # push A PATH TO all it's parents
            else:
                for parent in parents:
                    # MAKE A COPY OF THE PATH
                    new_path = path[:] + [parent]
                    # push THE COPY
                    s.push(new_path)
    #finished traversing all paths, return the earliest ancestor (the last node in the longest path)
    return longest_path[-1]

