from anyio import current_time
import networkx as nx
import matplotlib.pyplot as plt
from sqlalchemy import null
import random
import time


G = nx.gnp_random_graph(200, .02, seed=1000)


print("---------------")


pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='green', )
nx.draw_networkx_labels(G, pos)
plt.show()

MXG4 = nx.DiGraph(G)
print(nx.dijkstra_path(MXG4, 23, 150))

"""
# Car are refrenced by alphabets
class Car:
    def _init_(self, car_num, current_pos, passenger_limit, current_passenger):
        self.car_num = null
        self.current_pos = null
        self.passenger_limit = 5
        self.current_passenger = 0

# Reservation struct.
class Reservation:
    def _init_(self, pick_up, drop_off, time):
        self.pick_up = null
        self.drop_off = null
        self.time = null

# Pick-up and drop-off generator
def rand_loc():
    num = random.randint(0,9)
    return num


# main class.
print("Generating a Reservation")
res = Reservation()
car = Car()

for x in range(10):
    num1 = rand_loc()
    num2 = rand_loc()
   
    while num1 == num2:
        num2 = rand_loc()

res.pick_up = num1
res.drop_off = num2


car_list = []

for x in range(4):
    car_list.append(Car(x))

print(car.car_num())
"""