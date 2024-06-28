import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Generate a random OTP
def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

@app.route('/sendOTP', methods=['POST'])
def send_otp():
    # Email configuration
    sender_email = 'gokulp.21cse@kongu.edu'
    sender_password = 'Gokul@332003'
    subject = 'OTP Verification'
    
    try:
        # Get JSON data from the request
        data = request.get_json()

        # List of recipient email addresses
        recipient_emails = data.get('email')

        if not recipient_emails:
            return jsonify({"error": "Missing 'email' field in request data"}), 400

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to Gmail
        server.login(sender_email, sender_password)
        server.set_debuglevel(1)  # Enable debugging

        otps = {}  # Dictionary to store OTPs for each recipient

        for recipient_email in recipient_emails:
            # Generate OTP
            otp = generate_otp()
            otps[recipient_email] = otp  # Store the OTP for this recipient

            # Email content
            message = f"Hello,\n\nYour OTP for verification is: {otp}\n\nLet's Connect,\nTeam Homepro"
            # Create a MIMEText object
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Send the email
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"OTP sent successfully to {recipient_email}")

        # Disconnect from the server
        server.quit()

        return jsonify({"success": True, "otps": otps}), 200

    except smtplib.SMTPException as smtp_error:
        return jsonify({"error": f"SMTP Error: {str(smtp_error)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
