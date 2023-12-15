import pandas as pd

PNR_Booking_csv = "Data/mphasis_dataset/PNRB-ZZ-20231208_062017.csv"
PNR_Passenger_csv = "Data/mphasis_dataset/PNRP-ZZ-20231208_111136.csv"

PNR_Booking_df = pd.read_csv(PNR_Booking_csv)
PNR_Passenger_df = pd.read_csv(PNR_Passenger_csv)

#Identify impacted flights and passengers with the proposed schedule changes
def returnImpactedPassengers(DEP_KEY):
    # Filter PNR_Booking_df based on DEP_KEY
    impacted_booking_df = PNR_Booking_df[PNR_Booking_df['DEP_KEY'] == DEP_KEY]

    # Extract unique RECLOC values from the impacted booking DataFrame
    impacted_reclocs = impacted_booking_df['RECLOC'].unique()

    # Filter PNR_Passenger_df based on matching RECLOC values
    impacted_passenger_df = PNR_Passenger_df[PNR_Passenger_df['RECLOC'].isin(impacted_reclocs)]

    impacted_passenger_df = pd.merge(impacted_passenger_df, impacted_booking_df, on='RECLOC', how='left')
    
    # Add a new column DL_Conn = SEG_TOTAL - SEG_SEQ
    impacted_passenger_df['DL_Conn'] = impacted_passenger_df['SEG_TOTAL'] - impacted_passenger_df['SEG_SEQ']

    return impacted_passenger_df

def load_rules_from_file(file_path):
    # Implement logic to read rules from file (CSV, JSON, etc.)
    # Return a DataFrame with rules
    rules_df = pd.read_csv(file_path)  # Update this line based on your file format
    return rules_df

def rate_passengers(df, rules_df):
    # Create a new column to store ratings
    df['Passenger_Rating'] = 0

    # Loop through each rule
    for index, rule in rules_df.iterrows():
        # Extract rule conditions and rating
        conditions = rule['Conditions']
        rating = rule['Rating']
        var = rule['Variable']
        # Evaluate conditions for each passenger
        mask = df.eval(conditions)

        # Assign rating to passengers meeting the conditions
        df.loc[mask, 'Passenger_Rating'] += rating * ( 1 if (var == '.') else df[var])
    return df



def RankPassengers(DEP_KEY):
    ImpactedPassengers = returnImpactedPassengers(DEP_KEY)

    rules_file_path = 'Rules/rule_profile1/PNR_Rating.csv'
    rules_df = load_rules_from_file(rules_file_path)

    # Call the function to rate passengers
    rated_passengers_df = rate_passengers(ImpactedPassengers, rules_df)

    # Display the DataFrame with passenger ratings
    print(rated_passengers_df)
