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
    num = random.randint(0,int(location)-1)
    return num

# Random Minute Generator
def rand_min():
    num = random.randint(0,59)
    return num

# Reservation Generator
def reservation_gen(res_hour):
    for x in range(res_hour):
        temp_list = []
        res_range = random.randint(100, 150) # randomly creates the # of reservation between 100 - 150.
    
        for j in range(res_range):
            temp_list.append(rand_min())
        temp_list = sorted(temp_list)
    
        for k in range(res_range):
            res_database.append(Reservation(rand_loc(), rand_loc(), x, temp_list[k]))
        temp_list.clear()
    res_database.append(Reservation(0, 0, 5, -1))

def car_gen(car_count):
    for x in range(car_count):
        num = rand_loc()
        while nx.degree(G, num) == 0:
            num = rand_loc()
        car_list.append(Car(x, rand_loc(), 5 ,0, 0, pending_pick=[],pending_drop=[], current_path=[]))
    
def avg_distance(car_count):
    total = 0
    for x in range(car_count):
        total = total + car_list[x].node_travelled
    total = total * 0.05
    average = total / 30
    average = "{:.2}".format(average)
    print ("----------------------------------------")
    print("Average distance travelled: ", average, "miles.")
    print ("----------------------------------------\n\n")

def file_output():
    text_file = open("Reservation.txt", "w")
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


def dispatch(text_file, car_count, res_hour):
    index = 0
    x = 0
    for hours in range(res_hour+1):
        for mins in range (60):
            if (x < len(res_database)):
                text_file.write("------------------------------------------------------------------------------------------------------------------------------------------\n")
                text_file.write("{} {}\n".format("Hour: ", hours))
                text_file.write("{} {}\n".format("Mins: ", mins))
                next_iteration = True
                if (res_database[index].hour <= hours):
                    while (res_database[index].min <= mins and next_iteration):
                        found = True
                        assign_success = False
                        if nx.has_path(G, res_database[index].pick_up, res_database[index].drop_off):
                            assign_success = car_assign(index, car_count)
                        else:
                            text_file.write("No path!\n")
                            index += 1
                        if (index < len(res_database) and assign_success == True and res_database[index+1].min != -1):
                            index += 1
                        else:
                            next_iteration = False
                else:
                    text_file.write("No reservations!\n")
                x += 1
            drive()
        # Drive() - (Pop() first index from path, Next stop for each car, Picking up anyone, Dropping off anyone, Add 1 to stops travelled for each car travelled)
  
                
def drive():
    text_file.write("Driving!\n")
    for obj in car_list:
           text_file.write("{} {} {} {} {} {} {} {} {} {} {} {}\n".format("Car number: ", obj.car_num, "| Position: ", obj.current_pos, "| Passengers: ", obj.current_passenger, "     Pending Pick: ", obj.pending_pick, "     Pending Drop: ", obj.pending_drop,  "     Current Path: ", obj.current_path))     
    for x in range(len(car_list)):
       # print ("Car#: ", x, " Current Path: ")
        #print (*car_list[x].current_path)
        if (len(car_list[x].current_path) > 0):
            y = 0
            z = 0
            car_list[x].current_pos = car_list[x].current_path[0]
            #print ("Current Pos: ", car_list[x].current_pos)
            while z < len(car_list[x].pending_drop):
                if (res_database[car_list[x].pending_drop[z]].drop_off == car_list[x].current_pos):
                    car_list[x].pending_drop.pop(z)
                    #print("Dropping: ", z)
                    car_list[x].current_passenger -= 1
                    route_optimization(x)
                z += 1
            while y < len(car_list[x].pending_pick):
                if (res_database[car_list[x].pending_pick[y]].pick_up == car_list[x].current_pos):
                    #print("Picking: ", y)
                    car_list[x].pending_drop.append(car_list[x].pending_pick[y])
                    car_list[x].pending_pick.pop(y)
                    route_optimization(x)
                y += 1
            car_list[x].node_travelled += 1
            car_list[x].current_path.pop(0)
            

def car_assign(index, car_count):
    car_index = null
    assigned = False
    value = 200
    for x in range(car_count):
        if nx.has_path(G, car_list[x].current_pos, res_database[index].pick_up):
            temp = nx.shortest_path_length(G, car_list[x].current_pos, res_database[index].pick_up)
            if temp < value and temp !=0 and car_list[x].current_passenger < 5:
                value = temp
                car_index = x
    
    if car_index != null and car_list[car_index].current_passenger < 5:
        car_list[car_index].pending_pick.append(index)
        car_list[car_index].current_passenger += 1 
        assigned = True
        # Route_Optimization() - Optimize and update path
        route_optimization(car_index)
        
        wait_time = (nx.shortest_path_length(G, car_list[car_index].current_pos, res_database[index].pick_up)) + 2
        print ("Reservation ", index, "assigned to Car ", car_index, "!")
        print ("Estimated wait time is: ", wait_time,"minutes.\n")
        car_list[car_index].current_path.pop(0)
    else:
        string = "Reservation: " + str(index) + " 'Not able to assign!'\n"
        text_file.write(string)

    return assigned


def route_optimization(car_index):
   # print("Entered Route Optimization")
    pick_up = False
    drop_off = False
    temp_index = -1
    path_len = 200
    x = 0
    y = 0

    while x < len(car_list[car_index].pending_pick):
        temp_len = nx.shortest_path_length(G, car_list[car_index].current_pos, res_database[car_list[car_index].pending_pick[x]].pick_up)
        if (temp_len < path_len and temp_len != 0):
            pick_up = True
            path_len = temp_len
            temp_index = x
        x += 1
    
    while y < len(car_list[car_index].pending_drop):
        temp_len = nx.shortest_path_length(G, car_list[car_index].current_pos, res_database[car_list[car_index].pending_drop[y]].drop_off)
        if (temp_len < path_len and temp_len != 0):
            drop_off = True
            path_len = temp_len
            temp_index = y
        y += 1

    if (pick_up and not drop_off and temp_index != -1):
        car_list[car_index].current_path.clear()
        car_list[car_index].current_path = nx.shortest_path(G, car_list[car_index].current_pos, res_database[car_list[car_index].pending_pick[temp_index]].pick_up)


    elif (pick_up and drop_off and temp_index != -1) or (not pick_up and drop_off and temp_index != -1):
        car_list[car_index].current_path.clear()
        car_list[car_index].current_path = nx.shortest_path(G, car_list[car_index].current_pos, res_database[car_list[car_index].pending_drop[temp_index]].drop_off)


    elif (not pick_up and not drop_off):
        string = "Car: " + str(car_index) + " 'Error: No path found.'\n"
        text_file.write(string)

      
# main class.
index = 0
text_file = open("Dashboard.txt", "w")
print("*************** Ride Sharing ***************")
location = input("Enter number of locations: ")
frequency = input("Enter node connectivity (Int): ")
res_hours = input("Enter number of hours: ")
car_count = input("Enter number of cars: ")

G = nx.gnp_random_graph(int(location), float(int(frequency)/100), seed=1000)

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='green', )
nx.draw_networkx_labels(G, pos)
#plt.show()

print("Graph created!")
print("---------------------------------------------")

car_gen(int(car_count))
reservation_gen(int(res_hours))
file_output()
dispatch(text_file, int(car_count), int(res_hours))
avg_distance(int(car_count))

text_file.close()