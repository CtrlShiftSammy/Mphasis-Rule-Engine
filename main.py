import pandas as pd

from Passenger_Ranking import RankPassengers
from Flight_Matching import MatchFlights
from Flight_Matching import returnFlight
from Flight_Ranking import rate_flights
from Flight_Ranking import load_rules_from_file

CancelledFlightDep_Key = 'ZZ20240403BLRCCU2504'
ranked_passengers_df = RankPassengers(CancelledFlightDep_Key)
print(ranked_passengers_df)
matched_flights_df = MatchFlights(CancelledFlightDep_Key)
print(matched_flights_df)

CancelledFlightINV = returnFlight(CancelledFlightDep_Key)

# Add a new column 'Rating' to the matched_flights_df
matched_flights_df['Rating'] = 0

# Iterate through each row and fill the 'Rating' column
for index, row in matched_flights_df.iterrows():
    # Assuming RateFlights is a function that takes flight information and returns a rating
    rules_df = load_rules_from_file('Rules/rule_profile1/Flight_Scoring.csv')
    row_df = pd.DataFrame([list(row)], columns=matched_flights_df.columns)
    rating = rate_flights(CancelledFlightINV,row_df,rules_df)  # Pass the flight information to the function
    matched_flights_df.loc[index, 'Rating'] = rating
    #print(CancelledFlightINV)
    #print(row_df)

# Print the updated DataFrame with the 'Rating' column
print('matched flights:')
print(matched_flights_df[['InventoryId', 'FlightNumber', 'Dep_Key', 'DepartureAirport', 'ArrivalAirport', 'AircraftType','DepartureDate','DepartureDateTime','ArrivalDateTime', 'Rating']])
