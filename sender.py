import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender: str, password: str, recipient: str, subject: str, body: str) -> bool:
    """
    Send a plain-text email via Gmail's SMTP server.

    Args:
        sender:    Gmail address to send from.
        password:  Gmail App Password (not your regular password).
        recipient: Email address to send to.
        subject:   Subject line of the email.
        body:      Plain-text body of the email.

    Returns:
        True if the email was sent successfully, False otherwise.
    """
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, message.as_string())
        print(f"✅ Email sent successfully to {recipient}!")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check your email and App Password.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Failed to send email: {e}")
        return False