from multiprocessing.dummy import current_process
from nis import cat
from anyio import current_time
import networkx as nx
import matplotlib.pyplot as plt
from sqlalchemy import null
import random
import time
import logging

"""
G = nx.gnp_random_graph(200, .02, seed=1000)


print("---------------")


pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='green', )
nx.draw_networkx_labels(G, pos)
##plt.show()

MXG4 = nx.DiGraph(G)
print(nx.dijkstra_path(MXG4, 23, 150))
print(nx.dijkstra_path(MXG4, 45, 23))
"""
# Car are refrenced by alphabets
class Car(object):
    def __init__(self, car_num, current_pos, passenger_limit, current_passenger):
        self.car_num = car_num
        self.current_pos = current_pos
        self.passenger_limit = passenger_limit
        self.current_passenger = current_passenger

# Reservation struct.
class Reservation:
    def __init__(self, pick_up, drop_off, time):
        self.pick_up = null
        self.drop_off = null
        self.time = null

# Pick-up and drop-off generator
def rand_loc():
    num = random.randint(0,199)
    return num

# Reservation generator.
def reservation_gen():
    temp_pick = rand_loc()
    temp_drop = rand_loc()
    while temp_drop == temp_pick:
        temp_drop = rand_loc()

    res = Reservation()    
    res.pick_up = temp_pick
    res.drop_off = temp_drop

    logging.info('Reservation created')
        
    

# main class.

car_list = []
for x in range(30):
    car_list.append(Car(x, rand_loc(), 5 ,0))
for obj in car_list:
    print("Car number: ", obj.car_num, "| Position: ", obj.current_pos)



res = Reservation()
for x in range(30):
    reservation_gen()
    print("-------------------")
    print("Reservation: ", x)
    print("Pick up: ", res.pick_up)
    print("Drop off: ", res.drop_off)

