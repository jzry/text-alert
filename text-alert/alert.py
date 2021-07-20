# SCRIPT TO SEND MESSAGES THROUGH GOOGLE'S GMAIL SMTP SERVER

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from os.path import basename

from etext.providers import PROVIDERS
from etext.exceptions import (ProviderNotFoundException, NoMMSSupportException, NumberNotValidException)


# Check if a number is 10 digits long.
def validate_number(number: str):

    num = ""

    # Valid phone number is 10 digits.
    for character in number:
        if character.isdigit():
            num += character

    # Find the length of the phone number.
    if len(num) == 10:
        return num

    # Number is invalid.
    raise NumberNotValidException(number)


# Return the proper provider formatting.
def format_provider_email(number: str, provider: str, mms=False):

    # Get the service provider (AT&T, T-Mobile, Verizon, etc).
    provider_info = PROVIDERS.get(provider)

    # Error catching.
    if provider_info == None:
        raise ProviderNotFoundException(provider)

    # Find the domain for the service provider.
    domain = provider_info.get("sms")

    # See if the service provider accepts mms.
    if mms:
        mms_domain = provider_info.get("mms")

        # Only causes exception if mms is not supported.
        if not (mms_support = provider_info.get("mms_support")):
            raise NoMMSSupportException(provider)

        # Use mms domain if provider allows.
        if mms_domain:
            domain = mms_domain

    return f"{number}@{domain}"

# Send SMS (Text) with email (Google's SMTP server).
def send_sms_via_email
(
number: str,
message: str,
provider: str,
sender_credentials: tuple,
subject: str = "AlertBot",
smtp_server: str = "smtp.gmail.com",
smtp_port: int = 465
):

    number = validate_number(number)
    sender_email, email_password = sender_credentials
    receiver_email = format_provider_email(number, provider)

    email_message = f"Subject: {subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

# Send MMS (Images) with email
def send_mms_via_email
(
number: str,
message: str,
file_path: str,
mime_maintype: str,
mime_subtype: str,
provider: str,
sender_credentials: tuple,
subject: str = "sent using etext",
smtp_server: str = "smtp.gmail.com",
smtp_port: int = 465,
):

    number = validate_number(number)
    sender_email, email_password = sender_credentials
    receiver_email = _address(number, provider, mms=True)

    email_message = MIMEMultipart()
    email_message["Subject"] = subject
    email_message["From"] = sender_email
    email_message["To"] = receiver_email

    email_message.attach(MIMEText(message, "plain"))

    with open(file_path, "rb") as attachment:
        part = MIMEBase(mime_maintype, mime_subtype)
        part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={basename(file_path)}",
        )

        email_message.attach(part)

    text = email_message.as_string()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, text)
