import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from Passenger_Ranking import RankPassengers
from Flight_Matching import *
from Flight_Ranking import *
from Flight_Selection import *
from Solution_Calc import *

CancelledFlightDep_Key = 'ZZ20240615BLRDEL2257'
ranked_passengers_df = RankPassengers(CancelledFlightDep_Key)
#print(ranked_passengers_df)

ranked_flights_df = returnmMatchedRankedFlights(CancelledFlightDep_Key)
print(ranked_flights_df)

solution_df = returnSolution(ranked_passengers_df, ranked_flights_df, upgrade_class=True, downgrade_class=False)

reaccomodation_df = add_details_columns(solution_df, ranked_passengers_df, ranked_flights_df)

print(reaccomodation_df)