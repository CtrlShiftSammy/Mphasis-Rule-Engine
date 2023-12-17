import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Reading the CSV files containing rescheduled passenger data and unaccommodated passengers
rescheduled_passengers_file = 'Results/SolutionFileset1/reaccomodation.csv'
unaccommodated_passengers_file = 'Results/SolutionFileset1/exception.csv'

# Read CSV files using Pandas
rescheduled_passengers = pd.read_csv(rescheduled_passengers_file)
unaccommodated_passengers = pd.read_csv(unaccommodated_passengers_file)

# Email configurations
sender_email = 'airline.rescheduleinfo.72@gmail.com'
password = 'wiimiairkxzipzfk'

# Function to send email to passengers
def send_email(recipient, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}. Error: {str(e)}")

# Sending emails to rescheduled passengers
for index, passenger in rescheduled_passengers.iterrows():
    # Extracting necessary information for the email content
    customer_id = passenger['CUSTOMER_ID']
    last_name = passenger['LAST_NAME']
    first_name = passenger['FIRST_NAME']
    new_schedule_info = f"Flight: {passenger['FlightNumber']}, Departure: {passenger['DepartureDateTime']}, Arrival: {passenger['ArrivalDateTime']}, From: {passenger['DepartureAirport']}, To: {passenger['ArrivalAirport']}"
    
    # Composing the email content
    email_subject = f"Flight Rescheduling Information for Passenger {first_name} {last_name}"
    email_body = f"Dear {first_name} {last_name},\n\nWe regret to inform you that your flight has been rescheduled. Below are the updated details:\n\n{new_schedule_info}\n\nSincerely,\nThe Airline Team"

    # Sending email to each passenger
    send_email(passenger['CONTACT_EMAIL'], email_subject, email_body)

# Sending emails to unaccommodated passengers
for index, passenger in unaccommodated_passengers.iterrows():
    # Extracting necessary information for the email content
    customer_id = passenger['CUSTOMER_ID']
    last_name = passenger['LAST_NAME']
    first_name = passenger['FIRST_NAME']
    
    # Composing the email content
    email_subject = f"Unable to Accommodate Passenger {first_name} {last_name}"
    email_body = f"Dear {first_name} {last_name},\n\nWe regret to inform you that we were unable to accommodate you after the reschedule.\n\nSincerely,\nThe Airline Team"

    # Sending email to each unaccommodated passenger
    send_email(passenger['CONTACT_EMAIL'], email_subject, email_body)
