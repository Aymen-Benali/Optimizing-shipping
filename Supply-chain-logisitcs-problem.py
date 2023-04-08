import pandas as pd
import numpy as np
import pulp

''' Look what we have here'''
orders = pd.read_excel('Supply-chain-logisitcs-problem.xlsx',sheet_name  = 0)
orders.dropna(axis = 1, how = 'all', inplace = True)
orders.dropna(axis = 0, how = 'all', inplace = True)
orders.head()

freight_rates = pd.read_excel('Supply-chain-logisitcs-problem.xlsx', sheet_name  = 1)
freight_rates.dropna(axis = 1, how = 'all', inplace = True)
freight_rates.dropna(axis = 0, how = 'all', inplace = True)
freight_rates.head()

wh_capacities = pd.read_excel('Supply-chain-logisitcs-problem.xlsx', sheet_name  = 2)
wh_capacities.dropna(axis = 1, how = 'all', inplace = True)
wh_capacities.dropna(axis = 0, how = 'all', inplace = True)
wh_capacities.head()

products_per_plant = pd.read_excel('Supply-chain-logisitcs-problem.xlsx', sheet_name  = 3)
products_per_plant.dropna(axis = 1, how = 'all', inplace = True)
products_per_plant.dropna(axis = 0, how = 'all', inplace = True)
products_per_plant.head()

ports = pd.read_excel('Supply-chain-logisitcs-problem.xlsx', sheet_name  = 4)
ports.dropna(axis = 1, how = 'all', inplace = True)
ports.dropna(axis = 0, how = 'all', inplace = True)
ports.head()

'''We need to turn the shipping costs into a dictionary for easy lookup. We use the 'dict(zip(column1, column2))' paradigm.'''

shipping_costs = dict(zip(freight_rates['orig_port_cd'], freight_rates['rate']))

'''Next, we create a list of all unique products per plant. For now, you can treat the 'tuple' data type as a list:'''

def get_plants(product_id):
    temp = products_per_plant[products_per_plant['Product ID'] == product_id]
    return tuple(np.unique(temp['Plant Code']))
'''Part 1
Create a new column in the 'orders' dataframe called 'allowed_plants'. 
To do this, you'll need to apply the defined get_plants function using a lambda function.'''

orders['allowed_plants'] = orders['Product ID'].apply(lambda x: get_plants(x))
'''b) Set the index of the 'orders' dataframe to be the 'Order ID'. Make sure you set the index in place. '''


orders.set_index('Order ID', inplace = True)

'''Next, we create a dictionary to connect plants (warehouses) with the associated ports. Again, we use the 'dict(zip(column1, column2))' paradigm.'''

plant_ports = dict(zip(ports['Plant Code'], ports['Port']))
'''Part 2:

    a) Return the production cost for a given order_id and plant (wahrehouse) name. 
    From the order id, you should first get the associated product id, which can be used to get the cost per unit.
    From here, multiply the cost per unit by the unit quantity to get the total production cost.
''' 
def production_cost(order_id, plant):    

    t = orders.loc[order_id]
    prod_id = t['Product ID']
    pt = products_per_plant[products_per_plant['Product ID'] == prod_id]
    pt = pt[pt['Plant Code'] == plant]
    cpu = pt['Cost per unit']
    production_cost = cpu * t['Unit quantity']
    return production_cost.iloc[0]    

'''b) Return the shipping cost for a given order_id and plant (warehouse) name. 
From the plant name, you should first get the associated port, which can be used to get the shipping cost per lb.
From here, multiply the cost per lb by the weight to get the total shipping cost.
'''
def shipping_cost(order_id, plant):

    t = orders.loc[order_id]
    w = t['Weight']
    port = plant_ports[plant]
    cp = shipping_costs[port]
    ship_cost = cp * w
    return ship_cost

'''c) Return the total cost for a given order_id and plant (warehouse) name. 
You should add the results of the two functions above. 
'''
def total_cost(order_id, plant):

    return shipping_cost(order_id, plant) + production_cost(order_id, plant)

'''We create a dictionary with the key-value pair 'orderId_plantName': total_cost.
'''
order_costs = {}
for name, row in orders.iterrows():
    order_id = name
    for plant in row['allowed_plants']:   
        order_costs[str(order_id) + '_' + str(plant)] = total_cost(order_id, plant)

'''We create a dictionary with the key-value pair 'plantName': list_of_orders.
'''
plants = np.unique(ports['Plant Code'])

plant_orders = {}
for plant in plants:
    temp_list = []
    for name, row in orders.iterrows():
        if plant in row['allowed_plants']:  
            temp_list.append(str(name) + '_' + plant)
    plant_orders[plant] = temp_list
'''
###Creating linear programming constraints###

In this section, we build the linear programming problem and solve.
'''
build = pulp.LpVariable.dicts("Route",order_costs.keys(),0,None, pulp.LpInteger)
prob = pulp.LpProblem("Problem",pulp.LpMinimize)
prob += pulp.lpSum([build[b] * order_costs[b] for b in order_costs.keys()]), "Total Cost"

for plant in plant_orders:
    if len(plant_orders[plant]) > 0:
        prob += pulp.lpSum(build[p] for p in plant_orders[plant]) <= plant_cap[plant], "Total orders out of plant %s"%plant

for o in order_plants:
    prob += pulp.lpSum(build[p] for p in order_plants[o]) == 1, "Order_" + str(o) + "_filled"
'''
Part 3
a) Solve the linear programming problem and store its status in a variable called 'status'.
'''
status = pulp.LpStatus[prob.status]
for i in range(3):
    if status == 'Optimal':
        break
    prob.solve()

print("Status:", status)
'''
b) Find the total cost to produce and ship all products and store the answer in a variable called total_cost
Round the final answer to 2 decimal places
'''
import pulp
total_cost = round(pulp.value(prob.objective), 2)
print("Total Cost = ", str(total_cost))
