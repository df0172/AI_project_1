from multiprocessing.dummy import current_process
from nis import cat
from pickle import TRUE
from anyio import current_time
import networkx as nx
import matplotlib.pyplot as plt
from numpy import empty, positive
from sqlalchemy import null
import random
import time
import logging
from sympy import reduce_abs_inequalities
from zmq import THREAD_NAME_PREFIX


G = nx.gnp_random_graph(200, .02, seed=1000)
print("*************** GRAPH CREATED ***************")
print("---------------------------------------------\n")
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='green', )
nx.draw_networkx_labels(G, pos)
#plt.show()

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
    def __init__(self, car_num, current_pos, passenger_limit, current_passenger, node_travelled, pending_pick = [], pending_drop = [], current_path = []):
        self.car_num = car_num
        self.current_pos = current_pos
        self.passenger_limit = passenger_limit
        self.current_passenger = current_passenger
        self.node_travelled = node_travelled
        self.pending_pick = pending_pick
        self.pending_drop = pending_drop
        self.current_path = current_path

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
    res_database.append(Reservation(0, 0, 5, null))

def car_gen():
    for x in range(2):
        num = rand_loc()
        while nx.degree(G, num) == 0:
            num = rand_loc()
        car_list.append(Car(x, rand_loc(), 5 ,0, 0, pending_pick=[],pending_drop=[], current_path=[]))
    


def file_output():
    text_file = open("input.txt", "w")
    for obj in res_database:
        #text_file.write("Reservation: #", obj)
        string = "Pick up: "+ str(obj.pick_up)+"| Drop off: "+ str(obj.drop_off)+ "| Hour/Min/Sec: "+str(obj.hour)+":"+str(obj.min)+":00\n"
        text_file.write(string)
    text_file.close()

    text_file = open("car.txt", "w")
    for obj in car_list:
        string = "Car number: "+ str(obj.car_num) + "| Current Position: "+ str(obj.current_pos) + "| Pending Pick: "+ str(obj.pending_pick) + "| Pending Drop: "+ str(obj.pending_drop) + "\n"
        text_file.write(string)
    text_file.close()

    text_file = open("edges.txt", "w")
    text_file.write(str(G.edges()))
    text_file.close()

def dispatch():
    index = 0
    for hours in range(2):
        print ("\nHour: ", hours)
        for mins in range (60):
            print("\nMins: ", mins, "\n")
            next_iteration = True
            if (res_database[index].hour <= hours):
                found = False
                while (res_database[index].min <= mins and next_iteration):
                    found = True
                    assign_success = False
                    if nx.has_path(G, res_database[index].pick_up, res_database[index].drop_off):
                        assign_success = car_assign(index)
                    if (index+1 < len(res_database) and assign_success == True):
                        index += 1
                    else:
                        next_iteration = False
            drive()
        # Drive() - (Pop() first index from path, Next stop for each car, Picking up anyone, Dropping off anyone, Add 1 to stops travelled for each car travelled)
  
                
def drive():
    print("Driving!")
    for obj in car_list:
            print("Car number: ", obj.car_num, "| Position: ", obj.current_pos, "| Pending Pick: ", obj.pending_pick, "| Pending Drop: ", obj.pending_drop)  
            print("---------------------------------------------")
    for x in range(len(car_list)):
        if (car_list[x].current_path):
            car_list[x].current_pos = car_list[x].current_path[0]
            print ("Current Pos: ", car_list[x].current_pos)
            for z in range(len(car_list[x].pending_drop)-2):
                if (res_database[car_list[x].pending_drop[z]].drop_off == car_list[x].current_pos):
                    print("Dropping Off")
                    car_list[x].pending_drop.pop(z)
                    car_list[x].current_passenger =- 1
                    route_optimization(x)
            for y in range(len(car_list[x].pending_pick)-2):
                if (res_database[car_list[x].pending_pick[y]].pick_up == car_list[x].current_pos):
                    print("Picking Up")
                    car_list[x].pending_drop.append(car_list[x].pending_pick[y])
                    car_list[x].pending_pick.pop(y)
                    route_optimization(x)
            
            car_list[x].node_travelled += 1
            car_list[x].current_path.pop(0)
            



def car_assign(index):
    car_index = null
    assigned = False
    value = 200
    for x in range(2):
        if nx.has_path(G, car_list[x].current_pos, res_database[index].pick_up):
            temp = nx.shortest_path_length(G, car_list[x].current_pos, res_database[index].pick_up)
            if temp < value and temp !=0 and car_list[x].current_passenger < 6:
                value = temp
                car_index = x
    
    if car_index != null and car_list[car_index].current_passenger < 6:
        car_list[car_index].pending_pick.append(index)
        car_list[car_index].current_passenger += 1 
        assigned = True
        # Route_Optimization() - Optimize and update path
        route_optimization(car_index)

    """for obj in car_list:
        print("Car number: ", obj.car_num, "| Position: ", obj.current_pos, "| Pending Pick: ", obj.pending_pick, "| Pending Drop: ", obj.pending_drop)  
        print("---------------------------------------------")"""
    return assigned

"""
def clean_up(car_index):
    for x in range(0, len(car_list[car_index].current_path)-1):
        if car_list[car_index].current_path[x] == car_list[car_index].current_path[x-1]:
            car_list[car_index].current_path.pop(x)
"""

def route_optimization(car_index):
    print("Entered Route Optimization")
    pick_up = False
    drop_off = False
    temp_index = -1
    path_len = 200

    for x in car_list[car_index].pending_pick:
        temp_len = nx.shortest_path_length(G, car_list[car_index].current_pos, res_database[car_list[car_index].pending_pick[x]].pick_up)
        if (temp_len < path_len and temp_len != 0):
            pick_up = True
            path_len = temp_len
            temp_index = x
    
    for x in car_list[car_index].pending_drop:
        temp_len = nx.shortest_path_length(G, car_list[car_index].current_pos, res_database[car_list[car_index].pending_pick[x]].drop_off)
        if (temp_len < path_len and temp_len != 0):
            drop_off = True
            path_len = temp_len
            temp_index = x

    if (pick_up and not drop_off):
        car_list[car_index].current_path.clear()
        car_list[car_index].current_path = nx.shortest_path(G, car_list[car_index].current_pos, res_database[car_list[car_index].pending_pick[temp_index]].pick_up)
        car_list[car_index].current_path.pop(0)

    elif (pick_up and drop_off):
        car_list[car_index].current_path.clear()
        car_list[car_index].current_path = nx.shortest_path(G, car_list[car_index].current_pos, res_database[car_list[car_index].pending_drop[temp_index]].drop_off)
        car_list[car_index].current_path.pop(0)

    elif (not pick_up and not drop_off):
        print ("Error: No path found.")

    print ("Car#: ", car_index, " Current Path: ")
    print (*car_list[car_index].current_path)


      
# main class.
index = 0
car_gen()
reservation_gen()
file_output()
dispatch()


"""
print("the adjancy list:")
for line in range(200):
    print(line, "|", nx.degree(G, line))
    """