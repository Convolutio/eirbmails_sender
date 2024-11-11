import smtplib
import imaplib
import ssl
import sys
import time
from os import getenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv_vault import load_dotenv
load_dotenv()

def get_nonnull_env(key: str) -> str:
    value = getenv(key)
    if (value is None):
        raise ValueError(
            f"The configuration value does not exist with key {key}."
        )
    return value

# Connexion setup: secret as the documentation about these credentials is private
smtp_server = get_nonnull_env("SMTP_HOST")
imap_server = get_nonnull_env("IMAP_HOST")
smtp_port = int(get_nonnull_env("SMTP_PORT")) # assume SSL is required
imap_port = int(get_nonnull_env("IMAP_PORT")) # assume SSL is required

# Credentials
sender_email = get_nonnull_env("SENDER_MAIL") # the true mail of the sender 
sender_password = get_nonnull_env("SENDER_PASSWORD")
shared_organization = getenv("SENDER_SHARED_ORGANIZATION")
shared_email = get_nonnull_env("SENDER_SHARED_MAIL")
shared_email_sent_box_name = get_nonnull_env("SENDER_SHARED_EMAIL_SENT_BOX_NAME")
shared_email_with_org_name = f"{shared_organization} <{shared_email}>" if shared_organization is not None else shared_email

def write_mail(html_version: str, txt_version: str):
    to_email = sender_email # TODO: input("Prompt your recipient's mail: ")
    subject = "Test mail" # TODO: input("What is your message's subject: ")

    message = MIMEMultipart("alternative")
    message['From'] = shared_email_with_org_name  # Adresse de la boîte partagée X
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(txt_version, 'plain', 'utf-8'))
    message.attach(MIMEText(html_version, 'html', 'utf-8'))

    email_string = message.as_string()

    # Create a secure SSL context
    context = ssl.create_default_context()
    context2 = ssl.create_default_context()

    # Connexion et envoi de l'email
    try:
        # envoi de l'email
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(shared_email_with_org_name, to_email, email_string)
        print("Successfully sent mail")
        # ajout de l'email aux mails envoyés
        with imaplib.IMAP4_SSL(imap_server, imap_port, ssl_context=context2) as server:
            server.login(sender_email, sender_password)
            server.select(f'"{shared_email_sent_box_name}"')
            server.append(f'"{shared_email_sent_box_name}"', '', imaplib.Time2Internaldate(time.time()), email_string.encode("utf-8"))
        print("Successfully added the mail into the sent mail box")
    except Exception as e:
        print(f"Error while sending the mail : {e}")

if __name__ == "__main__":
    # Corps du message
    text_version = f"La version texte de l\'email envoyé par {sender_email} au nom de {shared_email_with_org_name} n'est pas encore définissable par l'utilisateur. Il suffirait juste de remplacer ce texte en dur par n'importe quel autre texte. Je crois qu'ici on peut tout faire pour les emojis"
    html_version = sys.stdin.read()
    write_mail(html_version, text_version)
