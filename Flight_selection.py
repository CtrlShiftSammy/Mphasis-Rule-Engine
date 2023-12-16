import pandas as pd
import numpy as np
from datetime import datetime as dt
from Passenger_Ranking import RankPassengers
PNR_Booking_csv = "Data/mphasis_dataset/PNRB-ZZ-20231208_062017.csv"
PNR_Passenger_csv = "Data/mphasis_dataset/PNRP-ZZ-20231208_111136.csv"

PNR_Booking_df = pd.read_csv(PNR_Booking_csv)
PNR_Passenger_df = pd.read_csv(PNR_Passenger_csv)

FlightInventory_csv = "Data/mphasis_dataset/INV-ZZ-20231208_041852.csv"
FlightSchedule_csv = "Data/mphasis_dataset/SCH-ZZ-20231208_035117.csv"

FlightInventory_df = pd.read_csv(FlightInventory_csv)
FlightSchedule_df = pd.read_csv(FlightSchedule_csv)

def load_rules_from_file(file_path):
    # Implement logic to read rules from file (CSV, JSON, etc.)
    # Return a DataFrame with rules
    rules_df = pd.read_csv(file_path)  # Update this line based on your file format
    return rules_df

def select_flight(ChangedFlight_Sched, AlterFlight_Sched, nextFlight, rules_df):
    ChangedFlight_Sched['DepartureDateTime'] = pd.to_datetime(ChangedFlight_Sched['DepartureDateTime'])
    ChangedFlight_Sched['ArrivalDateTime'] = pd.to_datetime(ChangedFlight_Sched['ArrivalDateTime'])
    ChangedFlight_Sched.sort_values(by=['DepartureDateTime'])
    
    AlterFlight_Sched['DepartureDateTime'] = pd.to_datetime(AlterFlight_Sched['DepartureDateTime'])
    AlterFlight_Sched['ArrivalDateTime'] = pd.to_datetime(AlterFlight_Sched['ArrivalDateTime'])
    AlterFlight_Sched.sort_values(by=['DepartureDateTime'])

    constraints = {'MAX_DEPARTURE_DELAY': float('inf'), 'MAX_DOWNLINE_GAP': float('inf'), 'MIN_DOWNLINE_GAP': 0}

    for index, rule in rules_df.iterrows():
        # Extract rule conditions and rating
        variable = rule['Variable']
        value = eval(rule['Value'])
        constraints[variable] = value
    
    DIFF_DEP = (AlterFlight_Sched['ArrivalDateTime'].iloc[0] - ChangedFlight_Sched['ArrivalDateTime'].iloc[0]).total_seconds()/3600
    if DIFF_DEP > constraints['MAX_DEPARTURE_DELAY']:
        return False
    
    for i in range(1, AlterFlight_Sched.shape[0]):
        diff =(AlterFlight_Sched['DepartureDateTime'].iloc[i] - AlterFlight_Sched['ArrivalDateTime'].iloc[i-1]).total_seconds()/3600
        if constraints['MAX_DOWNLINE_GAP']>=diff>=constraints['MIN_DOWNLINE_GAP']:
            pass
        else:
            return False
    
    if nextFlight is not None:
        nextFlight['DepartureDateTime'] = pd.to_datetime(nextFlight['DepartureDateTime'])
        nextFlight['ArrivalDateTime'] = pd.to_datetime(nextFlight['ArrivalDateTime'])
        nextFlight.sort_values(by=['DepartureDateTime'])
        diff = (nextFlight['DepartureDateTime'].iloc[0] - AlterFlight_Sched['ArrivalDateTime'].iloc[-1]).total_seconds()/3600
        if constraints['MAX_DOWNLINE_GAP']>=diff>=constraints['MIN_DOWNLINE_GAP']:
            pass
        else:
            return False

    return True

def SelectFlight(ChangedFlight_Sched, AlterFlight_Sched, nextFlight): # If there is no nextFlight pass None

    rules_file_path = 'Rules/rule_profile1/Flight_selection.csv'
    rules_df = load_rules_from_file(rules_file_path)
    score = select_flight(ChangedFlight_Sched, AlterFlight_Sched, nextFlight, rules_df)
    return score

def find_downline_connections(DEP_KEY):
    rated_passengers_df = RankPassengers(DEP_KEY)
    passenger_row = rated_passengers_df[rated_passengers_df['DEP_KEY'].astype(str).str.startswith(DEP_KEY)]

    if not passenger_row.empty:
        # Check if downline connections exist
        downline_connections = passenger_row['DL_Conn'].iloc[0]

        if downline_connections > 0:
            # Find associated RECLOC in PNR_Passenger_df
            recloc = passenger_row['RECLOC'].iloc[0]

            # Find flights with the same RECLOC in FlightInventory_df
            matching_flights = PNR_Booking_df[PNR_Booking_df['RECLOC'] == recloc]

            # Find the flight with seg_seq greater than the cancelled flight seg_seq by 1
            cancelled_flight_seg_seq = passenger_row['SEG_SEQ'].iloc[0]
            next_flight = matching_flights[matching_flights['SEG_SEQ'] == cancelled_flight_seg_seq + 1]

            if not next_flight.empty:
                return next_flight
            else:
                return None
        else:
            return None
    else:
        return None
