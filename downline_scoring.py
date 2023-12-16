from Flight_Ranking import matched_flights_df
from Passenger_Ranking import rated_passengers_df
import pandas as pd

PNR_Booking_csv = "Data/mphasis_dataset/PNRB-ZZ-20231208_062017.csv"
pnrb_df = pd.read_csv(PNR_Booking_csv)
# def matched_recloc(PNR_Booking_csv):
#     matching_dep_keys = matched_flights_df['DEP_KEY'].tolist()
#     df_downline = PNR_Booking_csv[PNR_Booking_csv['DEP_KEY'].isin(matching_dep_keys)]
#     return df_downline

# print(matched_recloc(PNR_Booking_csv))

def matched_recloc(rated_passengers_df, matched_flights_df):
    for i in len(rated_passengers_df):
        if rated_passengers_df['DL_Conn'] > 0:
            
            # df_downline = rated_passengers_df[rated_passengers_df['DL_Conn'].isin(matching_dep_keys)]

            downline_rows = []  # Collect rows meeting criteria
            matching_recloc = rated_passengers_df['RECLOC']
            matching_DL = rated_passengers_df['DL_Conn']-1

            # Search for matching RECLOC and DL-1 in PNRB DataFrame
            matching_row = pnrb_df[(pnrb_df['RECLOC'] == matching_recloc) & ((pnrb_df['SEG_TOTAL']-pnrb_df['SEG_SEQ']) == matching_DL)]
            
            if not matching_row.empty:
                downline_rows.append(matching_row)
            
            downline_df = pd.concat(downline_rows)
            # print(downline_df)

            # dept_time_further records dept. time of the immediate next leg of the affected passenger's journey in case of downline connections
            downline_df['DEP_DTML'] = pd.to_datetime(downline_df['DEP_DTML'], format='%d/%m/%Y %H:%M')
            dept_time_further = downline_df['DEP_DTML'].dt.time

