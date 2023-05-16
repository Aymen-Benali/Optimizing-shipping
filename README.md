# Optimizing-shipping
Supply Chain Logistics Problem

This is a Python script that solves a supply chain logistics problem using linear programming.
Problem Description

The problem involves shipping products from plants to warehouses through ports. The objective is to minimize the total cost of shipping while satisfying the demand and supply constraints. The following tables are used in the problem:

orders: contains information about the orders such as order ID, order date, product ID, destination port, unit quantity, and weight.
freight_rates: contains information about the shipping cost per unit weight between different ports.
wh_capacities: contains information about the daily capacity of each warehouse.
products_per_plant: contains information about the products available at each plant and their cost per unit.
ports: contains information about the ports used in the shipping.

How to use

Clone this repository or download the main.py file.
    Install the required dependencies: pandas, numpy, and pulp.
    Run the main.py file using a Python interpreter.
    The script will output the optimal shipping plan and the total cost of shipping.

Notes

    The script assumes that the input data is in an Excel file named Supply-chain-logisitcs-problem.xlsx.
    The output is displayed on the console.
    The script is tested on Python 3.10.4.
