import random
import itertools
from collections import deque
from statistics import mean

class User:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        if avg_friendships >= num_users:
            return 'error- number of users must be greater than the average number of friendships'

        # Add users
        for i in range(num_users):
            self.add_user(f'User {i+1}')

        # Create friendships
        total_friendships = avg_friendships * num_users
        combos = list(itertools.combinations(self.users.keys(), 2))
        random.shuffle(combos)
        for i in range(total_friendships // 2):
            self.add_friendship(combos[i][0], combos[i][1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # create a queue
        q = deque()
        #add path to the starting user_id
        q.append([user_id])
        #while the queue is not empty
        while len(q) > 0:
            #get the current path from the left of the queue (FIFO)
            path = q.popleft()
            #get the last node in the path
            v = path[-1]
            #check if its been visited- if it hasnt:
            if v not in visited:
                #add the path to visited
                visited[v] = path
                #get the friends of the last node in current path
                for friend in self.friendships[v]:
                    #add path to each friend to the queue
                    q.append(path[:] + [friend])

        return visited



if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(f'Users: {sg.users}\n')
    print(f'Friendships: {sg.friendships}\n')
    connections = sg.get_all_social_paths(1)
    print(f'Connections: {connections}\n')

    #Question 3 answers
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    num_connected_users = []
    avg_degrees_separation = []
    for user in sg.users:
        separation_degrees = []
        connections = sg.get_all_social_paths(user)
        num_connected_users.append(len(connections))
        for friend in connections.keys():
            separation_degrees.append(len(connections[friend]))
        avg_degrees_separation.append(mean(separation_degrees))
    mean_connected_users = mean(num_connected_users)
    mean_avg_degrees_separation = mean(avg_degrees_separation)
    print('In a social network of 1000 users w/ avg of 5 friends:\n')
    print(f'The avg number of connected users per user is {mean_connected_users}, or {round(mean_connected_users / 10, 2)}% of total users\n')
    print('The average degree of separation between a user and those in his/her extended network is:')
    print(round(mean_avg_degrees_separation, 2))