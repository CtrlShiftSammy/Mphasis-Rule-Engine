import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

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
                seat_name = f"{flight['FlightNumber']}_{seat_type}{seat_number}_{flight['InventoryId']}"
                G.add_node(seat_name, bipartite=1, seat_type=seat_type)  # bipartite=1 represents seats

                # Add edges with weights equal to the sum of passenger and flight scores
                for _, passenger in passengers.iterrows():
                    passenger['COS_CD'] = seat_type_passenger(passenger['COS_CD'])
                    if (passenger['COS_CD'] == seat_type)or ( ( ((passenger['COS_CD']=='A')or(passenger['COS_CD']=='B'))and((seat_type=='C') or ((seat_type=='D'))) )and downgrade_class) or ( ( ((passenger['COS_CD']=='D'))and((seat_type=='A') or ((seat_type=='B'))) )and upgrade_class) :
                        edge_weight = passenger['Passenger_Rating'] + flight['Flight_Rating']
                        G.add_edge(passenger['CUSTOMER_ID'], seat_name, weight=edge_weight)
                        
                        
    flights=seat_type_flight_revert(flights)
    
    return G

def returnSolution(passengers, flights, upgrade_class=False, downgrade_class=False):
    graph = create_weighted_bipartite_graph(passengers, flights, upgrade_class=False, downgrade_class=False)
    return(returnSolution_df(solve_weighted_bipartite(graph)))

def returnSolution_df(output_dict):
    # Create an empty DataFrame with the desired columns
    columns = ['FlightNumber', 'Seat', 'InventoryId', 'CUSTOMER_ID']
    result_df = pd.DataFrame(columns=columns)
    # Iterate through the dictionary and append rows to the DataFrame
    for key1, key2 in output_dict:
        # Determine which key is 'FlightNumber' and which is 'CUSTOMER_ID'
        if key1[0].isalpha():
            flight_number, seat, inventory_id , customer_id= key2.split('_')[0], key2.split('_')[1], key2.split('_')[2], key1
        else:
            flight_number, seat, inventory_id , customer_id = key1.split('_')[0], key1.split('_')[1], key1.split('_')[2], key2

        # Append the row to the DataFrame
        result_df = pd.concat([result_df, pd.DataFrame([{'FlightNumber': flight_number, 'Seat': seat, 'InventoryId': inventory_id, 'CUSTOMER_ID': customer_id}])], ignore_index=True)
    #Solution_df = add_details_columns(result_df)
    return result_df


def add_details_columns(input_df, customer_details_df, flight_details_df):
    # Merge the input DataFrame with flight details on 'InventoryId'
    merged_df = pd.merge(input_df, flight_details_df, how='left', left_on='InventoryId', right_on='InventoryId', suffixes=('_flight', ''))

    # Merge the merged DataFrame with customer details on 'CUSTOMER_ID'
    result_df = pd.merge(merged_df, customer_details_df, how='left', left_on='CUSTOMER_ID', right_on='CUSTOMER_ID', suffixes=('_customer', ''))

    # Select and reorder columns
    selected_columns = [
        'CUSTOMER_ID', 'LAST_NAME', 'FIRST_NAME', 'CONTACT_PH_NUM', 'CONTACT_EMAIL', 'FlightNumber', 'Seat', 'InventoryId', 
        'Dep_Key', 'AircraftType', 'DepartureDateTime', 'ArrivalDateTime', 'DepartureAirport', 'ArrivalAirport', 'Passenger_Rating', 'Flight_Rating'
    ]
    
    result_df = result_df[selected_columns]

    return result_df

def find_unreaccommodated_passengers(ranked_passengers_df, reaccommodation_df):
    # Extract CUSTOMER_IDs from the reaccommodation DataFrame
    reaccommodated_passengers = set(reaccommodation_df['CUSTOMER_ID'])

    # Filter ranked passengers DataFrame for those not in the reaccommodated set
    unreaccommodated_passengers_df = ranked_passengers_df[~ranked_passengers_df['CUSTOMER_ID'].isin(reaccommodated_passengers)]


    return unreaccommodated_passengers_df

def get_next_fileset_directory(base_directory='Results'):
    fileset_directories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d)) and d.startswith('SolutionFileset')]
    if not fileset_directories:
        return os.path.join(base_directory, 'SolutionFileset1')
    else:
        latest_fileset = max(map(lambda x: int(x.split('SolutionFileset')[-1]), fileset_directories))
        return os.path.join(base_directory, f'SolutionFileset{latest_fileset + 1}')

def produce_solution_fileset(ranked_passengers_df, ranked_flights_df, solution_df, reaccomodation_df, unreaccommodated_passengers_df):
    # Get the next fileset directory
    results_directory = get_next_fileset_directory()

    # Create the directory if it doesn't exist
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    # Store dataframes in CSV files
    ranked_passengers_df.to_csv(os.path.join(results_directory, 'ranked_passengers.csv'), index=False)
    ranked_flights_df.to_csv(os.path.join(results_directory, 'ranked_flights.csv'), index=False)
    solution_df.to_csv(os.path.join(results_directory, 'solution.csv'), index=False)
    reaccomodation_df.to_csv(os.path.join(results_directory, 'reaccomodation.csv'), index=False)
    unreaccommodated_passengers_df.to_csv(os.path.join(results_directory, 'exception.csv'), index=False)

