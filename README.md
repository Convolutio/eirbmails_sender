# HTML mail sender for a shared mailbox

## Install dependencies

```sh
poetry install
```

## Setup your credentials

Fill up a `.env` file with the correct credentials, as in the `.env.example`
file.

## Run the mail sender

With the commands below, a mail will be sent to yourself from the shared mail

> [!NOTE]
> Your sender mail must have the sending right to shared mail.

```sh
poetry shell

# In the poetry's venv, use your system ssl certificates
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt 

# Add your html message's body to the standard input of the main script
cat mail_body.html | python main.py
```
