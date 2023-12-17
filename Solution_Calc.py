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

def returnSolution(passengers, flights, upgrade_class=False, downgrade_class=False):
    graph = create_weighted_bipartite_graph(passengers, flights, upgrade_class=False, downgrade_class=False)
    return(returnSolution_df(solve_weighted_bipartite(graph)))

def returnSolution_df(output_dict):
    # Create an empty DataFrame with the desired columns
    columns = ['FlightNumber', 'Seat', 'CUSTOMER_ID']
    result_df = pd.DataFrame(columns=columns)

    # Iterate through the dictionary and append rows to the DataFrame
    for key1, key2 in output_dict:
        # Determine which key is 'FlightNumber' and which is 'CUSTOMER_ID'
        if key1[0].isalpha():
            flight_number, seat, customer_id = key2.split('.0_')[0], key2.split('_')[1], key1
        else:
            flight_number, seat, customer_id = key1.split('.0_')[0], key1.split('_')[1], key2

        # Append the row to the DataFrame
        result_df = pd.concat([result_df, pd.DataFrame([{'FlightNumber': flight_number, 'Seat': seat, 'CUSTOMER_ID': customer_id}])], ignore_index=True)

    return result_df
    # Create an empty DataFrame with the desired columns
    columns = ['FlightNumber', 'Seat', 'CUSTOMER_ID']
    result_df = pd.DataFrame(columns=columns)

    # Iterate through the dictionary and append rows to the DataFrame
    for key1, key2 in output_dict:
        # Determine which key is 'FlightNumber' and which is 'CUSTOMER_ID'
        if key1[0].isalpha():
            flight_number, seat, customer_id = key2.split('_')[0], key2.split('_')[1], key1
        else:
            flight_number, seat, customer_id = key1.split('_')[0], key1.split('_')[1], key2

        # Append the row to the DataFrame
        result_df = pd.concat([result_df, pd.DataFrame([{'FlightNumber': flight_number, 'Seat': seat, 'CUSTOMER_ID': customer_id}])], ignore_index=True)

    return result_df    # Create an empty DataFrame with the desired columns
    columns = ['FlightNumber', 'CUSTOMER_ID']
    result_df = pd.DataFrame(columns=columns)
    rows_to_append = []
    # Iterate through the dictionary and append rows to the DataFrame
    for key1, key2 in output_dict:
        # Determine which key is 'FlightNumber' and which is 'CUSTOMER_ID'
        if key1[0].isalpha():
            flight_number, customer_id = key2, key1
        else:
            flight_number, customer_id = key1, key2

        # Append the row to the DataFrame
        # Append the row to the list
        rows_to_append.append({'FlightNumber': flight_number, 'CUSTOMER_ID': customer_id})

    # Concatenate the list of rows to the DataFrame
    result_df = pd.concat([result_df, pd.DataFrame(rows_to_append)], ignore_index=True)

    return result_df