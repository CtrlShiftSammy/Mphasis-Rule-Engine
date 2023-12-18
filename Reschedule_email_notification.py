import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send email to passengers
def send_email(recipient, subject, body, attachment_path=None):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    if attachment_path:
        # Attach the ranked_flights.csv file
        attachment = open(attachment_path, 'rb')
        message.attach(MIMEText(attachment.read(), 'csv'))
        attachment.close()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}. Error: {str(e)}")


def email_reaccomodations(solution_choice)

    # Reading the CSV files containing rescheduled passenger data, unaccommodated passengers, and ranked flights
    rescheduled_passengers_file = 'Results/'+solution_choice+'/reaccomodation.csv'
    unaccommodated_passengers_file = 'Results/'+solution_choice+'/exception.csv'
    ranked_flights_file = 'Results/'+solution_choice+'/ranked_flights.csv'

    # Read CSV files using Pandas
    rescheduled_passengers = pd.read_csv(rescheduled_passengers_file)
    unaccommodated_passengers = pd.read_csv(unaccommodated_passengers_file)
    ranked_flights = pd.read_csv(ranked_flights_file)

    # Email configurations
    sender_email = 'airline.rescheduleinfo.72@gmail.com'
    password = 'wiimiairkxzipzfk'


    # Sending emails to rescheduled passengers
    for index, passenger in rescheduled_passengers.iterrows():
        # Extracting necessary information for the email content
        customer_id = passenger['CUSTOMER_ID']
        last_name = passenger['LAST_NAME']
        first_name = passenger['FIRST_NAME']
        new_schedule_info = f"Flight: {passenger['FlightNumber']}, Departure: {passenger['DepartureDateTime']}, Arrival: {passenger['ArrivalDateTime']}, From: {passenger['DepartureAirport']}, To: {passenger['ArrivalAirport']}"
        
        # Composing the email content
        email_subject = f"Flight Rescheduling Information for Passenger {first_name} {last_name}"
        email_body = f"Dear {first_name} {last_name},\n\nWe regret to inform you that your flight has been rescheduled. Below are the updated details:\n\n{new_schedule_info}\n\n"
        email_body += f"These are the available alternative flights you can choose from:\n{ranked_flights[['FlightNumber', 'AircraftType', 'DepartureDate', 'DepartureDateTime', 'ArrivalDateTime', 'DepartureAirport', 'ArrivalAirport', 'Flight_Rating', 'Flight_Quality_Grade']]}\n\nSincerely,\nThe Airline Team"

        # Sending email to each passenger with the ranked_flights.csv attachment
        send_email(passenger['CONTACT_EMAIL'], email_subject, email_body, ranked_flights_file)

    # Sending emails to unaccommodated passengers
    for index, passenger in unaccommodated_passengers.iterrows():
        # Extracting necessary information for the email content
        customer_id = passenger['CUSTOMER_ID']
        last_name = passenger['LAST_NAME']
        first_name = passenger['FIRST_NAME']
        
        # Composing the email content
        email_subject = f"Unable to Accommodate Passenger {first_name} {last_name}"
        email_body = f"Dear {first_name} {last_name},\n\nWe regret to inform you that we were unable to accommodate you after the reschedule.\n\n"
        email_body += f"These are the available alternative flights you can choose from:\n{ranked_flights[['FlightNumber', 'AircraftType', 'DepartureDate', 'DepartureDateTime', 'ArrivalDateTime', 'DepartureAirport', 'ArrivalAirport', 'Flight_Rating', 'Flight_Quality_Grade']]}\n\nSincerely,\nThe Airline Team"

        # Sending email to each unaccommodated passenger with the ranked_flights.csv attachment
        send_email(passenger['CONTACT_EMAIL'], email_subject, email_body, ranked_flights_file)
