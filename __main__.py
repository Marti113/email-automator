"""
Entry point for the email automator.

Usage:
    python -m email_automator

Make sure your .env file is set up first (see .env.example).
"""

from dotenv import load_dotenv

from email_automator.config import load_config
from email_automator.sender import send_email


def main():
    load_dotenv()  # Load variables from .env file

    try:
        config = load_config()
    except EnvironmentError as e:
        print(f"Configuration error:\n{e}")
        return

    send_email(
        sender=config.sender_email,
        password=config.sender_password,
        recipient=config.recipient_email,
        subject=config.subject,
        body=config.body,
    )


if __name__ == "__main__":
    main()