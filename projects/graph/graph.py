"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            print('error- vertex does not exist')

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            print('error- vertex does not exist')

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        #create a queue
        q = Queue()
        #enqueue the starting vertex
        q.enqueue(starting_vertex)
        #create a set to store the visited vertices
        visited = set()
        #while the queue is not empty...
        while q.size() > 0:
            #dequeue the first vertex
            v = q.dequeue()
            # check if its been visited
            if v not in visited:
            #if it hasnt:
                #mark it as visited
                print(v)
                visited.add(v)
                #enqueue all its neighbors
                for neighbor in self.get_neighbors(v):
                    q.enqueue(neighbor)
        print('\n')

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        #create a stack
        s = Stack()
        #push the starting vertex
        s.push(starting_vertex)
        #create a set to store visited vertices
        visited = set()
        #while the stack is not empty:
        while s.size() > 0:
            #pop the first vertex
            v = s.pop()
            #check if its been visited
            if v not in visited:
            #if it hasnt:
                #mark it as visited
                print(v)
                visited.add(v)
                #push all its neighbors onto the stack
                for neighbor in self.get_neighbors(v):
                    s.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()
        v = starting_vertex
        #check if node has been visited
        #if not:
        if v not in visited:
            #mark as visited
            print(v)
            visited.add(v)
            #call dft recursive on each neighbor
            for neighbor in self.get_neighbors(v):
                self.dft_recursive(neighbor, visited=visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create a queue
        q = Queue()
        # Enqueue A PATH TO the starting vertex
        q.enqueue([starting_vertex])
        # Create a set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            path = q.dequeue()
            # GRAB THE VERTEX FROM THE END OF THE PATH
            v = path[-1]
            # Check if it's been visited
            # If it hasn't...
            if v not in visited:
                # Mark it as visited
                visited.add(v)
                # CHECK IF IT'S THE TARGET
                if v == destination_vertex:
                    # IF SO, RETURN THE PATH
                    return path
                # Enqueue A PATH TO all it's neighbors
                for neighbor in self.get_neighbors(v):
                    # MAKE A COPY OF THE PATH
                    new_path = path[:] + [neighbor]
                    # ENQUEUE THE COPY
                    q.enqueue(new_path)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Create a stack
        s = Stack()
        # push A PATH TO the starting vertex
        s.push([starting_vertex])
        # Create a set to store visited vertices
        visited = set()
        # While the stack is not empty...
        while s.size() > 0:
            # pop the first PATH
            path = s.pop()
            # GRAB THE VERTEX FROM THE END OF THE PATH
            v = path[-1]
            # Check if it's been visited
            # If it hasn't...
            if v not in visited:
                # Mark it as visited
                visited.add(v)
                # CHECK IF IT'S THE TARGET
                if v == destination_vertex:
                    # IF SO, RETURN THE PATH
                    return path
                # push A PATH TO all it's neighbors
                for neighbor in self.get_neighbors(v):
                    # MAKE A COPY OF THE PATH
                    new_path = path[:] + [neighbor]
                    # push THE COPY
                    s.push(new_path)

    def dfs_recursive(self, starting_vertex, destination_vertex, prev_path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if prev_path is None:
            prev_path = []
        #base case: the starting vertex is the vertex we are searching for
        if starting_vertex == destination_vertex:
            return prev_path + [destination_vertex]

        #update current path as prev path + the new vertex
        path = prev_path + [starting_vertex]
        #iterate over each neighbor:
        for neighbor in self.get_neighbors(starting_vertex):
            #make sure we havent already encountered this neighbor on the current path (dont backtrack in an infinite loop)
            if neighbor not in prev_path:
                #recursively search down the graph from this neighbor
                new_path = self.dfs_recursive(neighbor, destination_vertex, path)
                if new_path is not None: #if the search is successful:
                    return new_path
        

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print("Graph vertices")
    print(graph.vertices)
    print('\n')

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    
    '''
    print('Breadth first traversal:')
    graph.bft(1)
    print('\n')

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    print('Depth First traversal')
    graph.dft(1)
    print('\n')
    print('Depth first traversal- recursive')
    graph.dft_recursive(1)
    print('\n')

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print('Breadth first search')
    print(graph.bfs(1, 6))
    print('\n')

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print('Depth first search:')
    print(graph.dfs(1, 6))
    print('\n')
    print('Depth first search, recursive:')
    print(graph.dfs_recursive(1, 6))