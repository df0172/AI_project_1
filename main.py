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

res_database = [] # Reservation List Declaration
car_list = [] # Vehicle List Declaration

# Reservation struct
class Reservation(object):
    def __init__(self, pick_up, drop_off, hour, min):
        self.pick_up = pick_up
        self.drop_off = drop_off
        self.hour = hour
        self.min = min

# Class Struct
class Car(object):
    def __init__(self, car_num, current_pos, passenger_limit, current_passenger):
        self.car_num = car_num
        self.current_pos = current_pos
        self.passenger_limit = passenger_limit
        self.current_passenger = current_passenger


# Random Location Generator
def rand_loc():
    num = random.randint(0,199)
    return num

# Random Minute Generator
def rand_min():
    num = random.randint(0,59)
    return num

# Reservation Generator
def reservation_gen():
    for x in range(8):
        temp_list = []
        res_range = random.randint(100, 150) # randomly creates the # of reservation between 100 - 150.
    
        for j in range(res_range):
            temp_list.append(rand_min())
        temp_list = sorted(temp_list)
    
        for k in range(res_range):
            res_database.append(Reservation(rand_loc(), rand_loc(), x, temp_list[k]))
        temp_list.clear()

def file_output():
    text_file = open("input.txt", "w")
    for obj in res_database:
        #text_file.write("Reservation: #", obj)
        string = "Pick up: "+ str(obj.pick_up)+"| Drop off: "+ str(obj.drop_off)+ "| Hour/Min/Sec: "+str(obj.hour)+":"+str(obj.min)+":00\n"
        text_file.write(string)
    text_file.close()
    

# main class.

for x in range(30):
    car_list.append(Car(x, rand_loc(), 5 ,0))
for obj in car_list:
    print("Car number: ", obj.car_num, "| Position: ", obj.current_pos)

reservation_gen()
file_output()




