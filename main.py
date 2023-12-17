import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

from Passenger_Ranking import *
from Flight_Matching import *
from Flight_Ranking import *
from Flight_Selection import *
from Solution_Calc import *

CancelledFlightDep_Key = 'ZZ20240515AMDHYD2223'
ranked_passengers_df = RankPassengers(CancelledFlightDep_Key)

ranked_flights_df = returnmMatchedRankedFlights(CancelledFlightDep_Key)
columns = ['InventoryId', 'Dep_Key', 'AircraftType', 'DepartureDateTime', 'ArrivalDateTime', 'DepartureAirport', 'ArrivalAirport', 'Flight_Rating']

solution_df = returnSolution(ranked_passengers_df, ranked_flights_df, upgrade_class=False, downgrade_class=False)

reaccomodation_df = add_details_columns(solution_df, ranked_passengers_df, ranked_flights_df)

unreaccommodated_passengers_df = find_unreaccommodated_passengers(ranked_passengers_df, reaccomodation_df)

produce_solution_fileset(ranked_passengers_df, ranked_flights_df, solution_df, reaccomodation_df, unreaccommodated_passengers_df)
