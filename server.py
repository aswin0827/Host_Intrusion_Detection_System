from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

from dotenv import load_dotenv
import os
load_dotenv()

# Access environment variables
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        recipient_email = data['to']
        subject = data['subject']
        body = data['body']

        print("Establishing connection...")
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        print("Logging in...")
        s.login(SENDER_EMAIL, SENDER_PASSWORD)

        print("Sending email...")
        email_message = f"Subject: {subject}\n\n{body}"
        s.sendmail(SENDER_EMAIL, recipient_email, email_message)

        s.quit()
        print("Email sent successfully.")
        return jsonify({'message': 'Email sent successfully!'}), 200

    except smtplib.SMTPException as smtp_err:
        print(f"SMTP error: {smtp_err}")
        return jsonify({'error': f"SMTP error: {smtp_err}"}), 500

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': f"Unexpected error: {e}"}), 500

    
@app.route('/', methods=['GET'])
def running():
    return jsonify({'message': 'Server is running!'})


if __name__ == '__main__':
    app.run(debug=True)
