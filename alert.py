# import smtplib
from plyer import notification
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
from constants import alerts_data_file,all_alert_notification_data_file,userManagementDataFile
from dataFormatter import load_file,save_file
from datetime import datetime
import requests

class Alert:
    def __init__(self,logMessage,detectedAttacks):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logMessage = logMessage
        self.detectedAttacks = detectedAttacks
    
# def send_alert_email(self,subject, body, to_email):
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     sender_email = "your_email@gmail.com"
#     sender_password = "your_app_password"

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = to_email
#     message["Subject"] = subject
#     message.attach(MIMEText(body, "plain"))

#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.send_message(message)
    
def send_desktop_alert(title, message,detectedAttacks):
    alerts_data = load_file(alerts_data_file)
    alerts_notifications_data = load_file(all_alert_notification_data_file)
    alerts_notifications_data.append(Alert(message,detectedAttacks))
    userData = load_file(userManagementDataFile)
    url = "http://127.0.0.1:5000/send-email"
    print(alerts_data['count'])
    data = {
        'to':userData['email'],
        'subject':"HIDS Alert",
        'body':message
    }
    if alerts_data['count'] == 0:
        notification.notify(
            title=title,
            message=message,
            app_icon=None,  # e.g. 'path/to/icon.png'
            timeout=10,
        )
        if userData['sendEmailAlerts']:
            try:
                response = requests.post(url, json=data)
                
                if response.status_code == 200:
                    print("Request successful!")
                    print("Response JSON:", response.json())
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    print("Response:", response.text)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

    elif alerts_data['count'] == 1:
        notification.notify(
            title=title,
            message=alerts_data['defaultMessage'],
            app_icon=None,
            timeout=10
        )
        if userData['sendEmailAlerts']:
            try:
                data['body'] = alerts_data['defaultMessage']
                response = requests.post(url, json=data)
                
                if response.status_code == 200:
                    print("Request successful!")
                    print("Response JSON:", response.json())
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    print("Response:", response.text)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

    alerts_data['count'] = (alerts_data['count']+1)
    save_file(alerts_data,alerts_data_file)
    save_file(alerts_notifications_data,all_alert_notification_data_file)
