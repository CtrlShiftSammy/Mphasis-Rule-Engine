import pandas as pd

FlightInventory_csv = "Data/mphasis_dataset/INV-ZZ-20231208_041852.csv"
FlightSchedule_csv = "Data/mphasis_dataset/SCH-ZZ-20231208_035117.csv"

FlightInventory_df = pd.read_csv(FlightInventory_csv)
FlightSchedule_df = pd.read_csv(FlightSchedule_csv)

def returnFlight(DEP_KEY):
    matching_rows = FlightInventory_df[FlightInventory_df['Dep_Key'].astype(str) == DEP_KEY+".0"]

    # Check if there are any matching rows
    if not matching_rows.empty:
        # Return the first matching row
        return matching_rows.iloc[0]
    else:
        # If no matching rows found, return None
        return None

def MatchFlights(DEP_KEY):
# Filter FlightInventory_df for the given DEP_KEY
#flight_inventory_row = FlightInventory_df[FlightInventory_df['Dep_Key'] == DEP_KEY]
    flight_inventory_row = FlightInventory_df[FlightInventory_df['Dep_Key'].astype(str).str.startswith(DEP_KEY)]

    #print(FlightInventory_df.head())
    # Get Departure Airport and Arrival Airport as single values
    departure_airport = flight_inventory_row['DepartureAirport'].iloc[0]
    arrival_airport = flight_inventory_row['ArrivalAirport'].iloc[0]
    # print(flight_inventory_row)
    # print("DEPARTURE", departure_airport)
    # print("ARRIVAL", arrival_airport)
    # print("ARRIVAL", FlightInventory_df['ArrivalAirport'])
    # print("DEPARTURE", FlightInventory_df['DepartureAirport'])
    FlightSchedule_df['CombinedDateTime'] = pd.to_datetime(FlightSchedule_df['StartDate'] + ' ' + FlightSchedule_df['DepartureTime'])
    # print(pd.to_datetime(flight_inventory_row['DepartureDateTime'].iloc[0]))
    # print(FlightSchedule_df['CombinedDateTime'])
    matched_flights_df = FlightInventory_df[
        (FlightInventory_df['ArrivalAirport'] == arrival_airport) &
        (FlightInventory_df['DepartureAirport'] == departure_airport)
    ]

    # print("Matched Flights:")
    # print(matched_flights_df[['InventoryId', 'FlightNumber', 'DepartureAirport', 'ArrivalAirport', 'AircraftType','DepartureDate','DepartureDateTime','ArrivalDateTime']])
    return(matched_flights_df)

