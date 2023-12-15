import pandas as pd
import numpy as np
from datetime import datetime as dt

PNR_Booking_csv = "Data/mphasis_dataset/PNRB-ZZ-20231208_062017.csv"
PNR_Passenger_csv = "Data/mphasis_dataset/PNRP-ZZ-20231208_111136.csv"
INV_Flight_csv = "Data/mphasis_dataset/INV-ZZ-20231208_041852.csv"
SCH_Flight_csv = "SCH-ZZ-20231208_035117.csv"

def load_rules_from_file(file_path):
    # Implement logic to read rules from file (CSV, JSON, etc.)
    # Return a DataFrame with rules
    rules_df = pd.read_csv(file_path)  # Update this line based on your file format
    return rules_df

def unique_sorted_dataframe(df):
    # Returns unique values in a dataframe column as a numpy array
    df1 = df.unique()
    df1.sort()
    return df1

def rate_flights(CurrentFlight_Sched, AlternateFlight_Sched, rules_df):
    score = 0

    CurrentFlight_Sched['DepartureDateTime'] = pd.to_datetime(CurrentFlight_Sched['DepartureDateTime'])
    CurrentFlight_Sched['ArrivalDateTime'] = pd.to_datetime(CurrentFlight_Sched['ArrivalDateTime'])
    CurrentFlight_Sched.sort_values(by=['DepartureDateTime'])

    AlternateFlight_Sched['DepartureDateTime'] = pd.to_datetime(AlternateFlight_Sched['DepartureDateTime'])
    AlternateFlight_Sched['ArrivalDateTime'] = pd.to_datetime(AlternateFlight_Sched['ArrivalDateTime'])
    AlternateFlight_Sched.sort_values(by=['DepartureDateTime'])

    DIFF_ARR = (AlternateFlight_Sched['DepartureDateTime'].iloc[-1] - CurrentFlight_Sched['DepartureDateTime'].iloc[-1]).total_seconds()/3600
    DIFF_DEP = (AlternateFlight_Sched['ArrivalDateTime'].iloc[0] - CurrentFlight_Sched['ArrivalDateTime'].iloc[0]).total_seconds()/3600

    STOPOVER = False
    if AlternateFlight_Sched.shape[0] > 1:
        STOPOVER = True
    
    SAME_EQUIPMENTS = False
    old_aircrafts = unique_sorted_dataframe(CurrentFlight_Sched['AircraftType'])
    new_aircrafts = unique_sorted_dataframe(AlternateFlight_Sched['AircraftType'])
    
    if np.array_equal(old_aircrafts, new_aircrafts):
        SAME_EQUIPMENTS = True

    CITY_PAIRS_SAME = False
    CITY_PAIRS_DIFF_BUT_SAME_CITIES = False
    CITY_PAIRS_DIFFERENT = False

    old_departure = AlternateFlight_Sched['DepartureAirport']
    new_departure = CurrentFlight_Sched['DepartureAirport']

    old_arrival = AlternateFlight_Sched['ArrivalAirport']
    new_arrival = CurrentFlight_Sched['ArrivalAirport']

    if np.array_equal(old_departure, new_departure) and np.array_equal(old_arrival, new_arrival):
        CITY_PAIRS_SAME = True
    
    old_departure = unique_sorted_dataframe(old_departure)
    new_departure = unique_sorted_dataframe(new_departure)
    old_arrival = unique_sorted_dataframe(old_arrival)
    new_arrival = unique_sorted_dataframe(new_arrival)
    if CITY_PAIRS_SAME == False and np.array_equal(old_departure, new_departure) and np.array_equal(old_arrival, new_arrival):
        CITY_PAIRS_DIFF_BUT_SAME_CITIES = True
    else:
        CITY_PAIRS_DIFFERENT = True

    # Loop through each rule
    for index, rule in rules_df.iterrows():
        # Extract rule conditions and rating
        conditions = rule['Conditions']
        rating = rule['Rating']
        # print(conditions)
        # Evaluate conditions for each passenger
        mask = eval(conditions)

        # Assign rating to passengers meeting the conditions
        score += rating * mask
        # print(index)
        
    return score

def RateFlights(CurrentFlight_Sched, AlternateFlight_Sched):
    # ImpactedPassengers = returnImpactedPassengers(DEP_KEY)

    rules_file_path = 'Rules/Flight_Scoring.csv'
    # rules_file_path = 'Rules/rule_profile1/Flight_Scoring.csv'
    rules_df = load_rules_from_file(rules_file_path)

    # Call the function to rate passengers
    score = rate_flights(CurrentFlight_Sched, AlternateFlight_Sched, rules_df)

    # Display the DataFrame with passenger ratings
    return score