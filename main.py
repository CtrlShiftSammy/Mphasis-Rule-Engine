import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from Initialize import *
from Passenger_Ranking import *
from Flight_Matching import *
from Flight_Ranking import *
from Flight_Selection import *
from Solution_Calc import *


defaultCancelledFlightDep_Key = 'ZZ20240515AMDHYD2223'
user_input = input("Enter the Departure Key of the Flight:")
CancelledFlightDep_Key = user_input if user_input else defaultCancelledFlightDep_Key

# Check if default value is being used
if not user_input:
    print(f"No user input given, using default value: {CancelledFlightDep_Key}")

choose_sched_change(CancelledFlightDep_Key)

ruleProfile = choose_folder()

ranked_passengers_df = RankPassengers(CancelledFlightDep_Key, ruleProfile)
print("Cancelled Flight DEP_KEY = ", CancelledFlightDep_Key)
print("Using Agent Rule Profile = ", ruleProfile)

print("Ranking Passengers...")
ranked_flights_df = returnmMatchedRankedFlights(CancelledFlightDep_Key, ruleProfile)

print("Calculating and Ranking Alternate Flights...")
solution_df = returnSolution(ranked_passengers_df, ranked_flights_df, upgrade_class=False, downgrade_class=False)

print("Reaccomodating Passengers...")
reaccomodation_df = add_details_columns(solution_df, ranked_passengers_df, ranked_flights_df)

unreaccommodated_passengers_df = find_unreaccommodated_passengers(ranked_passengers_df, reaccomodation_df)

produce_solution_fileset(ranked_passengers_df, ranked_flights_df, solution_df, reaccomodation_df, unreaccommodated_passengers_df)


