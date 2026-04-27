import os
from dataclasses import dataclass


@dataclass
class Config:
    sender_email: str
    sender_password: str
    recipient_email: str
    subject: str
    body: str


def load_config() -> Config:
    """
    Load email configuration from environment variables.

    Set these in a .env file (see .env.example) and load with:
        source .env   (Mac/Linux)
        or use python-dotenv

    Raises:
        EnvironmentError: If any required variable is missing.
    """
    required = ["SENDER_EMAIL", "SENDER_PASSWORD", "RECIPIENT_EMAIL"]
    missing = [key for key in required if not os.environ.get(key)]

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Copy .env.example to .env and fill in your values."
        )

    return Config(
        sender_email=os.environ["SENDER_EMAIL"],
        sender_password=os.environ["SENDER_PASSWORD"],
        recipient_email=os.environ["RECIPIENT_EMAIL"],
        subject=os.environ.get("EMAIL_SUBJECT", "Hello from Python!"),
        body=os.environ.get(
            "EMAIL_BODY",
            "This email was sent automatically using Python.",
        ),
    )