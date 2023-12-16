import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def seat_type_passenger(seattype):
    if seattype == "BusinessClass":
        return "A"
    if seattype == "EconomyClass":
        return "D"
    if seattype == "PremiumEconomyClass":
        return "C"
    if seattype == "FirstClass":
        return "B"

def seat_type_flight(dataframe):
    dataframe.rename(columns={'BC_Oversold': 'A', 'EC_Oversold': 'D', 'PC_Oversold': 'C', 'FC_Oversold': 'B'}, inplace=True)
    return dataframe
def seat_type_flight_revert(dataframe):
    dataframe.rename(columns={'A': 'BC_Oversold', 'D': 'EC_Oversold', 'C': 'PC_Oversold', 'B': 'FC_Oversold'}, inplace=True)
    return dataframe
def solve_weighted_bipartite(graph):
    matching = nx.algorithms.max_weight_matching(graph, weight='weight', maxcardinality=True)
    return matching

def create_weighted_bipartite_graph(passengers, flights, upgrade_class=False, downgrade_class=False):
    G = nx.Graph()
    flights=seat_type_flight(flights)
    
    # Add nodes for passengers
    for _, passenger in passengers.iterrows():
        passenger['COS_CD'] = seat_type_passenger(passenger['COS_CD'])
        G.add_node(passenger['CUSTOMER_ID'], bipartite=0, seat_type=passenger['COS_CD'])  # bipartite=0 represents passengers
    
    # Add nodes for seats with the same seat type as flights
    for _, flight in flights.iterrows():
        for seat_type in ["A", "B", "C", "D"]:
            for seat_number in range(1, flight[seat_type] + 1):
                seat_name = f"{flight['FlightNumber']}_{seat_type}{seat_number}"
                G.add_node(seat_name, bipartite=1, seat_type=seat_type)  # bipartite=1 represents seats

                # Add edges with weights equal to the sum of passenger and flight scores
                for _, passenger in passengers.iterrows():
                    passenger['COS_CD'] = seat_type_passenger(passenger['COS_CD'])
                    if (passenger['COS_CD'] == seat_type)or ( ( ((passenger['COS_CD']=='A')or(passenger['COS_CD']=='B'))and((seat_type=='C') or ((seat_type=='D'))) )and downgrade_class) or ( ( ((passenger['COS_CD']=='D'))and((seat_type=='A') or ((seat_type=='B'))) )and upgrade_class) :
                        edge_weight = passenger['Passenger_Rating'] + flight['Rating']
                        G.add_edge(passenger['CUSTOMER_ID'], seat_name, weight=edge_weight)
                        
                        
    flights=seat_type_flight_revert(flights)
    
    return G