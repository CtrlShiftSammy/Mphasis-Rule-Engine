import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from Passenger_Ranking import RankPassengers
from Flight_Matching import *
from Flight_Ranking import *
from Flight_Selection import *
from Solution_Calc import *

CancelledFlightDep_Key = 'ZZ20240602AMDHYD2223'
ranked_passengers_df = RankPassengers(CancelledFlightDep_Key)
print(ranked_passengers_df)
matched_flights_df = MatchFlights(CancelledFlightDep_Key)
#print(matched_flights_df)

ranked_flights_df = returnmMatchedRankedFlights(CancelledFlightDep_Key)
print(ranked_flights_df)

print(returnSolution(ranked_passengers_df.head(), ranked_flights_df.head(), upgrade_class=False, downgrade_class=False))
