from multiprocessing.dummy import current_process
from nis import cat
from anyio import current_time
import networkx as nx
import matplotlib.pyplot as plt
from numpy import positive
from sqlalchemy import null
import random
import time
import logging

from sympy import reduce_abs_inequalities


G = nx.gnp_random_graph(200, .02, seed=1000)


print("---------------")


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
    def __init__(self, car_num, current_pos, passenger_limit, current_passenger, node_traveled, reservation = [], current_path = []):
        self.car_num = car_num
        self.current_pos = current_pos
        self.passenger_limit = passenger_limit
        self.current_passenger = current_passenger
        self.node_traveled = node_traveled
        self.reservation = reservation
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

    for x in range(30):
        num = rand_loc()
        while nx.degree(G, num) == 0:
            num = rand_loc()
        car_list.append(Car(x, rand_loc(), 5 ,0, 0, reservation=[], current_path=[]))
    


def file_output():
    text_file = open("input.txt", "w")
    for obj in res_database:
        #text_file.write("Reservation: #", obj)
        string = "Pick up: "+ str(obj.pick_up)+"| Drop off: "+ str(obj.drop_off)+ "| Hour/Min/Sec: "+str(obj.hour)+":"+str(obj.min)+":00\n"
        text_file.write(string)
    text_file.close()
    
def dispatch():
    index = 0
    for hours in range(8):
        for mins in range (60):
            if (res_database[index].hour == hours):
                found = False
                while (res_database[index].min == mins):
                    found = True
                    if nx.has_path(G, res_database[index].pick_up, res_database[index].drop_off):
                        num =0
                        #car_assign(index)

                    if (index+1 < len(res_database)):
                        index += 1
        # Drive() - (Pop() first index from path, Next stop for each car, Picking up anyone, Dropping off anyone, Add 1 to stops travelled for each car travelled)
  
                

def car_assign(index):
    
    car_index = null
    value = 200
   
    for x in range(30):
        if nx.has_path(G, car_list[x].current_pos, res_database[index].drop_off):
            temp = nx.shortest_path_length(G, car_list[x].current_pos, res_database[index].pick_up)
            if temp < value and temp !=0 and car_list[x].current_passenger < 5:
                value = temp
                car_index = x
    
    if car_index != null:
        car_list[car_index].reservation.append(index)
        car_list[car_index].current_passenger += 1 
        # Route_Optimization() - Optimize and update path


    for obj in car_list:
        print("Car number: ", obj.car_num, "| Position: ", obj.current_pos, "| res: ", obj.reservation)   
   


       
        
 
    



# main class.


car_gen()
reservation_gen()
file_output()
dispatch()
index = 5
if nx.has_path(G, res_database[index].pick_up, res_database[index].drop_off):
    car_assign(index)



"""
print("the adjancy list:")
for line in range(200):
    print(line, "|", nx.degree(G, line))
    """