import os
import pandas as pd
from datetime import datetime

def calculate_rating():
    results_folder = 'Results/'
    # Get a list of solution set folders
    solution_sets = [folder for folder in os.listdir(results_folder) if os.path.isdir(os.path.join(results_folder, folder))]

    best_solution_set = None
    best_rating = float('inf')  # Initialize with positive infinity, as lower rating is better

    for solution_set in solution_sets:
        # Define paths to necessary files
        reaccomodation_path = os.path.join(results_folder, solution_set, 'reaccomodation.csv')
        exception_path = os.path.join(results_folder, solution_set, 'exception.csv')
        cancelled_flight_path = os.path.join(results_folder, solution_set, 'cancelled_flight.csv')

        try:
            # Load data from CSV files
            reaccomodation = pd.read_csv(reaccomodation_path)
            exception = pd.read_csv(exception_path)
            cancelled_flight = pd.read_csv(cancelled_flight_path)

            # Calculate % of unreaccommodated passengers
            unreaccomodated_percentage = ((len(exception) - 1) / ((len(reaccomodation) - 1) + (len(exception) - 1))) * 100

            # Calculate average difference between DepartureDateTime of cancelled flight and reaccommodations
            cancelled_departure_time = datetime.strptime(cancelled_flight['DepartureDateTime'].iloc[0], '%Y-%m-%d %H:%M:%S')
            reaccomodation_departure_times = pd.to_datetime(reaccomodation['DepartureDateTime'])
            average_time_difference = (reaccomodation_departure_times - cancelled_departure_time).mean()

            # Check for the presence of layover flight
            layover_present = 'layover' in solution_set.lower()

            # Calculate overall rating
            rating = unreaccomodated_percentage + average_time_difference.total_seconds() + layover_present

            # Update best solution set if the current rating is lower
            if rating < best_rating:
                best_rating = rating
                best_solution_set = solution_set

        except Exception as e:
            print(f"Error processing solution set {solution_set}: {e}")

    return best_solution_set

# Example usage:
best_solution = calculate_rating()
print(f"The best solution set is: {best_solution}")