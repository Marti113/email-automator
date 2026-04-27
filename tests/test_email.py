import unittest
from unittest.mock import MagicMock, patch

from email_automator.sender import send_email


class TestSendEmail(unittest.TestCase):

    @patch("email_automator.sender.smtplib.SMTP_SSL")
    def test_send_email_success(self, mock_smtp_class):
        """Email sends successfully with valid credentials."""
        mock_server = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_server

        result = send_email(
            sender="sender@gmail.com",
            password="fakepassword",
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test body.",
        )

        self.assertTrue(result)
        mock_server.login.assert_called_once_with("sender@gmail.com", "fakepassword")
        mock_server.sendmail.assert_called_once()

    @patch("email_automator.sender.smtplib.SMTP_SSL")
    def test_send_email_auth_failure(self, mock_smtp_class):
        """Returns False when authentication fails."""
        import smtplib

        mock_smtp_class.return_value.__enter__.side_effect = smtplib.SMTPAuthenticationError(
            535, b"Authentication failed"
        )

        result = send_email(
            sender="bad@gmail.com",
            password="wrongpassword",
            recipient="recipient@example.com",
            subject="Test",
            body="Test",
        )

        self.assertFalse(result)


class TestLoadConfig(unittest.TestCase):

    def test_missing_env_vars_raises(self):
        """Raises EnvironmentError when required vars are missing."""
        import os
        from email_automator.config import load_config

        # Temporarily remove env vars if they exist
        env_backup = {k: os.environ.pop(k, None) for k in ["SENDER_EMAIL", "SENDER_PASSWORD", "RECIPIENT_EMAIL"]}

        with self.assertRaises(EnvironmentError):
            load_config()

        # Restore
        for k, v in env_backup.items():
            if v is not None:
                os.environ[k] = v

    def test_loads_config_from_env(self):
        """Correctly loads config when all env vars are set."""
        import os
        from email_automator.config import load_config

        os.environ["SENDER_EMAIL"] = "sender@gmail.com"
        os.environ["SENDER_PASSWORD"] = "secret"
        os.environ["RECIPIENT_EMAIL"] = "recipient@example.com"

        config = load_config()

        self.assertEqual(config.sender_email, "sender@gmail.com")
        self.assertEqual(config.recipient_email, "recipient@example.com")


if __name__ == "__main__":
    unittest.main()