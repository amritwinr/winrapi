import smtplib, secrets
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receiver_email):
    # Generate a 6-digit OTP
    otp = random.randint(1000, 9999)

    # Your email and password
    sender_email = "winralgo@gmail.com"
    password = "crhdnkiyrwjxvqhb"

    # Email subject and message body
    subject = "Finish Creating Your Account On WINRALGO"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # HTML and CSS styling for the email body
    html = f"""
    <html>
        <head>
            <style>
                /* Define your styles here */
                h1 {{
                    color: #007bff;
                    text-align: center;
                }}
                p {{
                    font-size: 18px;
                    line-height: 1.6;
                    margin-bottom: 20px;
                }}
                .otp {{
                    display: inline-block;
                    padding: 5px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    border-color: rgb(151, 139, 139);
                    box-shadow: 2px 2px 5px #ccc;
                }}
                .thank-you {{
                    text-align: right;
                }}
            </style>
        </head>
        <body>
            <h2>Dear User</h2>
            <h1>Welcome to WINRALGO!</h1>
            <p>Plz enter the below OTP to continue to WINRALGO.</p>
            <p>Your OTP is: <span class="otp">{otp}</span></p>
            <p>Note: This OTP will expire in 10 minutes, plz do not share your OTP with anyone.</p>
            <h3 class="thank-you">Thank You Team, WINRALGO.</h3>  
        </body>
    </html>
    """

    # Attach the HTML message to the email
    message.attach(MIMEText(html, "html"))

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return otp

# Example usage
# receiver_email = "amrittiwary921@gmail.com"
# otp = send_email(receiver_email)
# print(f"OTP sent to {receiver_email}: {otp}")
# # print(send_email(receiver_email="amrittiwary921@gmail.com"))

# stored_otp = str(otp)#"123456"
# print(stored_otp)

# def verify_otp(otps):
#     if otps == stored_otp:
#         return True
#     else:
#         return False

# # Example usage
# user_otp = input("Enter the OTP: ")
# if verify_otp(user_otp):
#     print("OTP verified successfully!")
# else:
#     print("Invalid OTP. Please try again.")

# print(verify_otp(otps=stored_otp))



# import random

# # def generate_otp():
# #     return random.randint(1000, 9999)

# # # Example usage
# # otp = generate_otp()
# # print("Generated OTP: ", otp)

# otp = random.randint(1000, 9999)
# print(otp)



# "Welcome to the exciting world of the stock market! We're thrilled to have you as a new member of our community. With your new account, you have the opportunity to navigate the market, make informed investment decisions and potentially see your assets grow. We're here to support you every step of the way, so don't hesitate to reach out to us with any questions. Let's make the most of this journey together!"


# "We take your security very seriously and that's why we've implemented a one-time password (OTP) system for your account. Your OTP ensures that only you have access to your sensitive information. Simply enter the OTP sent to your registered email address to verify your identity and access your account. Thank you for choosing our service and for keeping your account safe!"


# import smtplib
# from email.mime.text import MIMEText

# # Your email credentials
# email_user = 'winralgo@gmail.com'
# email_password = 'crhdnkiyrwjxvqhb'

# # The recipient email address
# recipient = 'amrittiwary921@gmail.com'

# # The email message
# message = MIMEText("""
#     <html>
#         <body>
#             <h1 style="color: blue;">Welcome to our service!</h1>
#             <p>We're thrilled to have you onboard and can't wait to see how you'll make the most of your new account.</p>
#             <p>Reach out to us if you have any questions, and let's make the most of this journey together!</p>
#         </body>
#     </html>
# """, 'html')

# # The email subject
# message['Subject'] = 'Welcome to our service'

# # Connect to the email server
# smtp = smtplib.SMTP('smtp.gmail.com', 587)
# smtp.starttls()
# smtp.login(email_user, email_password)

# # Send the email
# smtp.sendmail(email_user, recipient, message.as_string())

# # Close the connection
# smtp.quit()

# https://chat.openai.com/chat
 