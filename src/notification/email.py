import os
import boto3

from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from notification.notification import Notification
from typing import Dict, List
from utils.utils import write_items_to_csv


class Sender:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class Recipient:
    def __init__(self, email: str):
        self.email = email


class Email(Notification):
    def __init__(
        self,
        sender: Sender,
        recipient: Recipient,
        aws_region: str,
    ):
        super().__init__()
        self.sender = sender
        self.recipient = recipient
        self.aws_region = aws_region

    def notify(
        self, subject: str, items: Dict[str, Dict[str, Dict[str, str]]]
    ) -> ClientError:
        filepaths = write_items_to_csv(items)
        message = self._create_message(subject, filepaths)
        sender = f"{self.sender.name} <{self.sender.email}>"
        recipient = self.recipient.email
        ses_client = boto3.client("ses", region_name=self.aws_region)
        try:
            ses_client.send_raw_email(
                Source=sender,
                Destinations=[recipient, sender],
                RawMessage={
                    "Data": message.as_string(),
                },
            )
        except ClientError as e:
            return e
        return None

    def _create_message(self, subject: str, filepaths: List[str]):
        sender = f"{self.sender.name} <{self.sender.email}>"
        recipient = self.recipient.email

        # Create a multipart/mixed parent container.
        msg = MIMEMultipart("mixed")
        # Add subject, from and to lines.
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart("alternative")

        attachments = []
        for filepath in filepaths:
            # Define the attachment part and encode it using MIMEApplication.
            att = MIMEApplication(open(filepath, "rb").read())

            # Add a header to tell the email client to treat this part as an attachment,
            # and to give the attachment a name.
            att.add_header(
                "Content-Disposition", "attachment", filename=os.path.basename(filepath)
            )
            attachments.append(att)

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Add the attachment to the parent container.
        for att in attachments:
            msg.attach(att)

        return msg
