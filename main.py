import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

from Passenger_Ranking import RankPassengers
from Flight_Matching import *
from Flight_Ranking import *
from Flight_Selection import *
from Solution_Calc import *

CancelledFlightDep_Key = 'ZZ20240515AMDHYD2223'
ranked_passengers_df = RankPassengers(CancelledFlightDep_Key)
#print(ranked_passengers_df)

ranked_flights_df = returnmMatchedRankedFlights(CancelledFlightDep_Key)
columns = ['InventoryId', 'Dep_Key', 'AircraftType', 'DepartureDateTime', 'ArrivalDateTime', 'DepartureAirport', 'ArrivalAirport', 'Flight_Rating']
print(ranked_flights_df[columns])

solution_df = returnSolution(ranked_passengers_df, ranked_flights_df, upgrade_class=False, downgrade_class=False)

reaccomodation_df = add_details_columns(solution_df, ranked_passengers_df, ranked_flights_df)

unreaccommodated_passengers_df = find_unreaccommodated_passengers(ranked_passengers_df, reaccomodation_df)

print(reaccomodation_df)


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

# Print the resulting DataFrame
print(unreaccommodated_passengers_df)