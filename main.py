import pandas as pd

from Passenger_Ranking import RankPassengers
from Flight_Matching import MatchFlights
from Flight_Matching import returnFlight
from Flight_Ranking import RateFlights

CancelledFlightDep_Key = 'ZZ20240406CCUHYD3723'
#RankPassengers(CancelledFlightDep_Key)

matched_flights_df = MatchFlights(CancelledFlightDep_Key)
print(matched_flights_df)

CancelledFlightINV = returnFlight(CancelledFlightDep_Key)

# Add a new column 'Rating' to the matched_flights_df
matched_flights_df['Rating'] = 0

# Iterate through each row and fill the 'Rating' column
for index, row in matched_flights_df.iterrows():
    # Assuming RateFlights is a function that takes flight information and returns a rating
    print(CancelledFlightINV)
    print(row)
    rating = RateFlights(CancelledFlightINV,row)  # Pass the flight information to the function
    matched_flights_df.at[index, 'Rating'] = rating

# Print the updated DataFrame with the 'Rating' column
print(matched_flights_df[['InventoryId', 'FlightNumber', 'Dep_Key', 'DepartureAirport', 'ArrivalAirport', 'AircraftType','DepartureDate','DepartureDateTime','ArrivalDateTime']])
