from socketserver import ThreadingUnixDatagramServer
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from Passenger_Ranking import RankPassengers
from Flight_Matching import MatchFlights
from Flight_Matching import returnFlight, UpdateFlightRecords
from Flight_Ranking import rate_flights
from Flight_Ranking import load_rules_from_file
from Flight_selection import select_flight
from Flight_selection import find_downline_connections
from Class_Rules_Matching import ClassValues

UnaccomodatedPassengers_csv = "Data/mphasis_dataset/UnaccomodatedPassengers.csv"
ScheduledPassengers_csv = "Data/mphasis_dataset/ScheduledPassengers.csv"

CancelledFlightDep_KeyList = ['ZZ20240403BLRCCU2504']
ranked_passengers_dfList = [RankPassengers(CancelledFlightDep_KeyList[i]) for i in range(len(CancelledFlightDep_KeyList))]

class_acronym = {'FirstClass':'FC', 'BusinessClass':'BC', 'PremiumEconomyClass':'PC', 'EconomyClass':'EC'}

unaccomodated_passengers = []
resched_details = []

# print(ranked_passengers_df)
def reschedule(CancelledFlightDep_Key, ranked_passengers_df):
    for _, passenger in ranked_passengers_df.iterrows():
        # print(passenger)
        # print(passenger)
        matched_flights_df = MatchFlights(CancelledFlightDep_Key)
        # print(matched_flights_df)

        CancelledFlightINV = returnFlight(CancelledFlightDep_Key)

        # Add a new column 'Rating' to the matched_flights_df
        matched_flights_df['Rating'] = 0
        matched_flights_df['Eligible_cd'] = 1

        change = False
        may_change = False
        reason_3 = False

        # Iterate through each row and fill the 'Rating' column
        for index, row in matched_flights_df.iterrows():
            # Assuming RateFlights is a function that takes flight information and returns a rating
            flight_scoring_rules_df = load_rules_from_file('Rules/rule_profile1/Flight_Scoring.csv')
            flight_selection_rules_df = load_rules_from_file('Rules/rule_profile1/Flight_Selection.csv')
            row_df = pd.DataFrame([list(row)], columns=matched_flights_df.columns)
            passenger_df = pd.DataFrame([list(passenger)], columns=ranked_passengers_df.columns)
            rating = rate_flights(CancelledFlightINV,row_df,flight_scoring_rules_df)  # Pass the flight information to the function
            boolv, reason = select_flight(CancelledFlightINV, row_df, find_downline_connections(CancelledFlightDep_Key, passenger_df), flight_selection_rules_df)
            if (boolv):
                matched_flights_df.loc[index, 'Rating'] = rating
                matched_flights_df['Eligible_cd'] = 0
                may_change = True
            elif reason == 3:
                matched_flights_df.loc[index, 'Rating'] = rating
                matched_flights_df['Eligible_cd'] = 3
                reason_3 = True
        
        if may_change == True and reason_3 == False:
            matched_flights_df.sort_values(by=['Rating'], ascending = False)
            for index, row in matched_flights_df.iterrows():
                if matched_flights_df.loc[index, 'Eligible_cd'] !=0:
                    continue
                allowed_classes = ClassValues(passenger['COS_CD'])
                for i in allowed_classes:
                    c_acronym = class_acronym[i]
                    if row[c_acronym+'_AvailableInventory'] >= passenger['PAX_CNT']:
                        # 'allot flight to passenger' can add passenger to solution file
                        resched_details.append([passenger,row])
                        # 'make changes to dataframe' update the records
                        # check for future inconsistencies
                        change = True
                        break
                if change == True:
                    break
        
        if reason_3 == True and change == False:    
            matched_flights_df.sort_values(by=['Rating'], ascending = False)
            for index, row in matched_flights_df.iterrows():
                if matched_flights_df.loc[index, 'Rating'] not in [0, 3]:
                    continue
                allowed_classes = ClassValues(passenger['COS_CD'])
                for i in allowed_classes:
                    c_acronym = class_acronym[i]
                    if row[c_acronym+'_AvailableInventory'] >= passenger['PAX_CNT']:
                        # 'allot flight to passenger' can add passenger to solution file
                        passenger['COS_CD'] = i
                        resched_details.append([passenger,row])
                        # 'make changes to dataframe' update the records
                        row_df = pd.DataFrame([list(row)], columns=matched_flights_df.columns)
                        UpdateFlightRecords(row_df, passenger_df['PAX_CNT'], c_acronym)
                        # check for future inconsistencies
                        change = True
                        break
                if change == True:
                    break
            if change == True:
                # print(find_downline_connections(CancelledFlightDep_Key, passenger_df)['DEP_KEY'].iloc[0])
                CancelledFlightDep_KeyList.append(find_downline_connections(CancelledFlightDep_Key, passenger_df)['DEP_KEY'].iloc[0])#Append airplant data
                ssq = passenger_df['SEG_SEQ'].iloc[0]
                pass_pnr = passenger_df['RECLOC'].iloc[0]
                passenger_df = passenger_df[(passenger_df['SEG_SEQ'] == ssq+1) & (passenger_df['RECLOC'] == pass_pnr)]
                ranked_passengers_dfList.append(passenger_df)# Make passenger into dataframe
        
        if change == False:
            # can make a change to the future flights
            unaccomodated_passengers.append(passenger)

    # Print the updated DataFrame with the 'Rating' column
    # print(matched_flights_df[['InventoryId', 'FlightNumber', 'Dep_Key', 'DepartureAirport', 'ArrivalAirport', 'AircraftType','DepartureDate','DepartureDateTime','ArrivalDateTime', 'Rating']])

i = 0
while i < len(CancelledFlightDep_KeyList):
    print(i, len(CancelledFlightDep_KeyList), CancelledFlightDep_KeyList[i], ranked_passengers_dfList[i])
    reschedule(CancelledFlightDep_KeyList[i], ranked_passengers_dfList[i])
    i+=1

h_PNR_Booking_csv = "Data/mphasis_dataset/PNRB-ZZ-20231208_062017.csv"
h_PNR_Booking_df = pd.read_csv(h_PNR_Booking_csv)

unaccomodated_passengers = pd.DataFrame(unaccomodated_passengers, columns=h_PNR_Booking_df.columns)
unaccomodated_passengers.to_csv(UnaccomodatedPassengers_csv)

ScheduledPassengers = []
for i in range(len(resched_details)):
    passenger, row = resched_details[i]
    passenger['FLT_NUM'] = row['FlightNumber']
    passenger['ORIG_CD'] = row['DepartureAirport']
    passenger['DEST_CD'] = row['ArrivalAirport']
    passenger['DEP_DT'] = row['DepartureDate']
    passenger['DEP_DTML'] = row['DepartureDateTime']
    passenger['ARR_DTML'] = row['ArrivalDateTime']
    passenger['DEP_DTMZ'] = 0
    passenger['DEP_DTMZ'] = 0
    ScheduledPassengers.append(passenger)
ScheduledPassengers = pd.DataFrame(ScheduledPassengers, columns=h_PNR_Booking_df.columns)
non_considered_passengers = h_PNR_Booking_df[~h_PNR_Booking_df[['RECLOC', 'SEG_SEQ']].isin(ScheduledPassengers).all(axis=1) & ~h_PNR_Booking_df[['RECLOC', 'SEG_SEQ']].isin(unaccomodated_passengers).all(axis=1)]
ScheduledPassengers = ScheduledPassengers._append(non_considered_passengers, ignore_index=True)
ScheduledPassengers.to_csv(ScheduledPassengers_csv)

print(i, len(CancelledFlightDep_KeyList))
print(len(unaccomodated_passengers), len(resched_details))
