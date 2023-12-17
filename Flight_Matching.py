import pandas as pd

FlightInventory_csv = "Data/mphasis_dataset/INV-ZZ-20231208_041852.csv"
FlightSchedule_csv = "Data/mphasis_dataset/SCH-ZZ-20231208_035117.csv"
FlightInventory_csv102002002 = "Data/mphasis_dataset/updated_INV-ZZ-20231208_041852.csv"

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

def MatchFlights(DEP_KEY):
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

    rules_file_path = 'Rules/rule_profile1/Flight_Scoring.csv'
    rules_df = load_rules_from_file(rules_file_path)
    # print("Matched Flights:")
    # print(matched_flights_df[['InventoryId', 'FlightNumber', 'DepartureAirport', 'ArrivalAirport', 'AircraftType','DepartureDate','DepartureDateTime','ArrivalDateTime']])
    return(matched_flights_df)

def UpdateFlightRecords(flight_df, pax_cnt, class_code):
    FlightInventory_df.loc[FlightInventory_df['InventoryId'] == flight_df.iloc[0]['InventoryId'], 'BookedInventory'] += pax_cnt
    FlightInventory_df.loc[FlightInventory_df['InventoryId'] == flight_df.iloc[0]['InventoryId'], 'Oversold'] += pax_cnt
    FlightInventory_df.loc[FlightInventory_df['InventoryId'] == flight_df.iloc[0]['InventoryId'], 'AvailableInventory'] -= pax_cnt
    FlightInventory_df.loc[FlightInventory_df['InventoryId'] == flight_df.iloc[0]['InventoryId'], class_code+'_BookedInventory'] += pax_cnt
    FlightInventory_df.loc[FlightInventory_df['InventoryId'] == flight_df.iloc[0]['InventoryId'], class_code+'_Oversold'] += pax_cnt
    FlightInventory_df.loc[FlightInventory_df['InventoryId'] == flight_df.iloc[0]['InventoryId'], class_code+'_BookedInventory'] -= pax_cnt
    FlightInventory_df.to_csv(FlightInventory_csv102002002)
