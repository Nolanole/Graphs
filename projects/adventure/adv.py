from room import Room
from player import Player
from world import World
from collections import deque
import time
import random
from ast import literal_eval


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

# player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

def dft(player):
    """
    Print each vertex in depth-first order
    beginning from starting_vertex.
    """
    reverse_direction_map = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

    graph = {}
    starting_room_id = player.current_room.id
    traversal_path = []

    #create a stack
    stack = []
    #add starting room empty dict to the graph
    graph[starting_room_id] = {}

    #get the available exits from the starting room
    exits = player.current_room.get_exits()
    #Fill in the starting_room exit direction values with '?' in the graph
    for exit_dir in exits:
        graph[starting_room_id][exit_dir] = '?'
    #pick random direction and push it onto the stack: 
    stack.append(random.choice(exits))

    #create a set to store fully explored rooms (no '?')
    visited = set()

    #initialize a curr_room var
    curr_room_id = starting_room_id

    #while the stack is not empty:
    while len(stack) > 0: 
        #pop the last direction from the stack
        direction = stack.pop()

        #walk to the room in that direction and update the traversal path
        player.travel(direction)
        traversal_path.append(direction)

        #update curr and prev room vars
        prev_room_id = curr_room_id
        curr_room_id = player.current_room.id

        #if prev_room direction is ?, update with the current room id
        if graph[prev_room_id][direction] == '?':
            graph[prev_room_id][direction] = curr_room_id

        #check if room in graph: if not, add it and initialize empty dict for room exits
        if curr_room_id not in graph:
            graph[curr_room_id] = {}
            exits = player.current_room.get_exits()
            #fill in '?' for each of the room exits
            for exit_dir in exits:
                graph[curr_room_id][exit_dir] = '?'

        #update the graph for the current room to prev room (opposite direction we just walked) 
        if graph[curr_room_id][reverse_direction_map[direction]] == '?':
            graph[curr_room_id][reverse_direction_map[direction]] = prev_room_id       

        #check if its been visited:
        if curr_room_id not in visited:
            #check for any '?' in exits: if None, mark as visited, do bfs to nearest '?'
            exits = graph[curr_room_id]

            if '?' not in set(exits.values()):
                visited.add(curr_room_id)
                #check len of visited == 500
                if len(visited) == 500:
                    # print('All Rooms Found!')
                    return traversal_path, graph
                else: 
                    #BFS call to get path to nearest '?'
                    path = bfs(graph, curr_room_id)
                    
                    #make sure all rooms except the last in the path are in the visited set:
                    for room_id in path[:-1]:
                        visited.add(room_id)

                    #traverse the path to the nearest '?'
                    for room_id in path[1:]: #path[0] is the current room, so start w/ path[1]                    
                        exits = graph[curr_room_id]
                        #figure out which direction to go in order to trace the path to the next room_id
                        for exit_dir in exits:
                            if graph[curr_room_id][exit_dir] == room_id:
                                #go to the next room
                                player.travel(exit_dir)
                                #update the curr_room_id var
                                curr_room_id = player.current_room.id
                                #update the traversal path
                                traversal_path.append(exit_dir)
                                break #exit the current iteration thru room exits

                    #After following the path to nearest room w/ '?':        
                    #randomize which of unexplored exits ('?') to choose next:
                    unexplored_exits = []
                    for exit_dir in graph[curr_room_id]:
                        if graph[curr_room_id][exit_dir] == '?':
                            unexplored_exits.append(exit_dir)
                    stack.append(random.choice(unexplored_exits))
                    #if theres only one exit left, mark off the current room as visited:
                    if len(unexplored_exits) == 1:
                        visited.add(curr_room_id)

            #randomize choice of unexplored exit from current room                    
            else:
                unexplored_exits = []
                for exit_dir in exits:
                    if graph[curr_room_id][exit_dir] == '?':
                        unexplored_exits.append(exit_dir)
                #add the random choice to the stack
                stack.append(random.choice(unexplored_exits)) 
                #if theres only one exit left, mark off the current room as visited:
                if len(unexplored_exits) == 1:
                    visited.add(curr_room_id)                       

def bfs(graph, curr_room_id):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    # Create a queue
    q = deque()
    # Enqueue A PATH TO curr room:
    path = [curr_room_id]
    q.append(path)
    # Create a set to store visited rooms
    visited = set()
    # While the queue is not empty...
    while len(q) > 0:
        # Dequeue the first PATH
        path = q.popleft()
        # GRAB THE room from the end of the path
        curr_room_id = path[-1]
        # Check if it's been visited
        # If it hasn't...
        if curr_room_id not in visited:
            # Mark it as visited
            visited.add(curr_room_id)
            # CHECK IF any neighbors are '?'
            if '?' in graph[curr_room_id].values():
                # IF SO, RETURN THE PATH                
                return path 
            # If no '?' in current room exits: Enqueue A PATH TO all the exits:
            for exit_dir in graph[curr_room_id]:
                # MAKE A COPY OF THE PATH
                # ENQUEUE THE COPY
                new_path = path[:] + [graph[curr_room_id][exit_dir]] 
                q.append(new_path)
    
# TRAVERSAL TEST
def perform_test():
    player = Player(world.starting_room)
    traversal_path, graph = dft(player)

    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(room_graph):
        # print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
        return traversal_path
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

    return traversal_path

### STRETCH GOAL ###
#Iterate until shortest path < 970

shortest_path = []
min_length = 9999999999
n = 1

# for _ in range(n):

print('Starting timer - searching for path <= 957 moves!')
start = time.time()
# count = 0
while min_length > 957:
    traversal_path = perform_test()
    path_length = len(traversal_path)
    if path_length < min_length:
        shortest_path = traversal_path
        min_length = path_length
    # count += 1
    # if count % 1000 == 0:
    #     print(f'After {count} iterations, shortest path found is {min_length} moves.')

#      if _ % 1000 == 0:
#         print(f'After {_} iterations, the shortest path found is {min_length} moves!')

# print(f'After {n} iterations, the shortest path found is {min_length} moves!')

end = time.time()
runtime = end - start

print(f'After {runtime} seconds, a path of {min_length} moves was found!')
print(f'Shortest path: {shortest_path}')


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
