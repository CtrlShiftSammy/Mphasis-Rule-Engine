import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from Initialize import *
from Passenger_Ranking import *
from Flight_Matching import *
from Flight_Ranking import *
from Flight_Selection import *
from Solution_Calc import *
from Solution_Ranking import *

defaultCancelledFlightDep_Key = 'ZZ20240515AMDHYD2223'
user_input = input("Enter the Departure Key of the Flight:")
CancelledFlightDep_Key = user_input if user_input else defaultCancelledFlightDep_Key

# Check if default value is being used
if not user_input:
    print(f"No user input given, using default value: {CancelledFlightDep_Key}")

choose_sched_change(CancelledFlightDep_Key)

ruleProfile = choose_folder('Rules/')

ranked_passengers_df = RankPassengers(CancelledFlightDep_Key, ruleProfile)
print("Cancelled Flight DEP_KEY = ", CancelledFlightDep_Key)
cancelled_flight_df = returnFlight(CancelledFlightDep_Key)
print("Using Agent Rule Profile = ", ruleProfile)

print("Ranking Passengers...")
ranked_flights_df = returnmMatchedRankedFlights(CancelledFlightDep_Key, ruleProfile, ranked_passengers_df, cancelled_flight_df)

print("Calculating and Ranking Alternate Flights...")
solution_df = returnSolution(ranked_passengers_df, ranked_flights_df, upgrade_class=False, downgrade_class=False)

print("Reaccomodating Passengers...")
reaccomodation_df = add_details_columns(solution_df, ranked_passengers_df, ranked_flights_df)

unreaccommodated_passengers_df = find_unreaccommodated_passengers(ranked_passengers_df, reaccomodation_df)

produce_solution_fileset(cancelled_flight_df, ranked_passengers_df, ranked_flights_df, solution_df, reaccomodation_df, unreaccommodated_passengers_df)

user_input = input("Do you want to find the best solution set? (yes/no): ").lower()

if user_input in ['yes', 'y']:
    best_solution = calculate_rating()
    print(f"The best solution set is: {best_solution}")
else:
    print("Solution ranking skipped")


user_input = input("Do you want to email the reaccomodations to the passengers? (yes/no): ").lower()

if user_input in ['yes', 'y']:
    print('Select the solution set to use')
    solution_choice = choose_folder('Results/')
    email_reaccomodations(solution_choice)
else:
    print("Reaccomodation emails skipped")


