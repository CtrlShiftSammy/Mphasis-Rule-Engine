import pandas as pd
import os

from Passenger_Ranking import *
from Flight_Matching import *
from Flight_Ranking import *
from Flight_Selection import *

FlightInventory_csv = "Data/mphasis_dataset/INV-ZZ-20231208_041852.csv"
FlightSchedule_csv = "Data/mphasis_dataset/SCH-ZZ-20231208_035117.csv"

FlightInventory_df = pd.read_csv(FlightInventory_csv)
FlightSchedule_df = pd.read_csv(FlightSchedule_csv)
def load_rules_from_file(file_path):
    # Implement logic to read rules from file (CSV, JSON, etc.)
    # Return a DataFrame with rules
    rules_df = pd.read_csv(file_path)  # Update this line based on your file format
    return rules_df

def returnFlight(DEP_KEY):
    matching_rows = FlightInventory_df[FlightInventory_df['Dep_Key'].astype(str) == DEP_KEY+".0"]

    # Check if there are any matching rows
    if not matching_rows.empty:
        # Return the first matching row
        return matching_rows
    else:
        # If no matching rows found, return None
        return None

def MatchFlights(DEP_KEY,ruleProfile):
# Filter FlightInventory_df for the given DEP_KEY
    flight_inventory_row = FlightInventory_df[FlightInventory_df['Dep_Key'].astype(str).str.startswith(DEP_KEY)]
    
    # Get Departure Airport and Arrival Airport as single values
    departure_airport = flight_inventory_row['DepartureAirport'].iloc[0]
    arrival_airport = flight_inventory_row['ArrivalAirport'].iloc[0]
    FlightSchedule_df['CombinedDateTime'] = pd.to_datetime(FlightSchedule_df['StartDate'] + ' ' + FlightSchedule_df['DepartureTime'])
    matched_flights_df = FlightInventory_df[
        (FlightInventory_df['ArrivalAirport'] == arrival_airport) &
        (FlightInventory_df['DepartureAirport'] == departure_airport)
    ]

    rules_file_path = 'Rules/'+ruleProfile+'/Flight_Scoring.csv'
    rules_df = load_rules_from_file(rules_file_path)
    # print("Matched Flights:")
    #print(matched_flights_df[['InventoryId', 'FlightNumber', 'DepartureAirport', 'ArrivalAirport', 'AircraftType','DepartureDate','DepartureDateTime','ArrivalDateTime']])
    return(matched_flights_df)

def returnmMatchedRankedFlights(DEP_KEY, ruleProfile, ranked_passengers_df, cancelled_flight_df):
    ranked_passengers_df = RankPassengers(DEP_KEY, ruleProfile)
    #print(ranked_passengers_df)
    matched_flights_df = MatchFlights(DEP_KEY, ruleProfile)
    #print(matched_flights_df)

    CancelledFlightINV = returnFlight(DEP_KEY)

    # Add a new column 'Rating' to the matched_flights_df
    matched_flights_df['Flight_Rating'] = 0
    matched_flights_df['Flight_Quality_Grade'] = 'D'

    selected_flights_df = pd.DataFrame(columns=matched_flights_df.columns)
    insert_index = 0
    # Iterate through each row and fill the 'Rating' column
    for index, row in matched_flights_df.iterrows():
        # Assuming RateFlights is a function that takes flight information and returns a rating
        flight_scoring_rules_df = load_rules_from_file('Rules/'+ruleProfile+'/Flight_Scoring.csv')
        flight_selection_rules_df = load_rules_from_file('Rules/'+ruleProfile+'/Flight_Selection.csv')
        row_df = pd.DataFrame([list(row)], columns=matched_flights_df.columns)
        rating, grade = rate_flights(CancelledFlightINV, row_df, flight_scoring_rules_df)  # Pass the flight information to the function
        
        if select_flight(CancelledFlightINV, row_df, find_downline_connections(DEP_KEY, ruleProfile, ranked_passengers_df), flight_selection_rules_df):
            selected_flights_df = pd.concat([selected_flights_df, row_df], ignore_index=True)
            matched_flights_df.loc[insert_index, 'Flight_Rating'] = rating
            selected_flights_df.loc[insert_index, 'Flight_Rating'] = rating
            
            selected_flights_df.loc[insert_index, 'Flight_Quality_Grade'] = grade
            
            insert_index = insert_index + 1
            #print(rating)

    #print(matched_flights_df[['InventoryId', 'FlightNumber', 'Dep_Key', 'DepartureAirport', 'ArrivalAirport', 'AircraftType','DepartureDate','DepartureDateTime','ArrivalDateTime', 'Rating']])
    return(selected_flights_df)

