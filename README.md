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
> You can use your own mail as shared mail

```sh
poetry shell

# In the poetry's venv, use your system ssl certificates
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt 

# Add your text/plain and html message's body to the standard input of the main script
python main.py $MAIL_TXT_FILE $MAIL_HTML_FILE
```

Then, the python script will ask you some mail data as the recipient, the
subject, etc. You can automate that with a `credentials.txt` file, as in the
`credentials.example.txt`.

```sh
python main.py $MAIL_TXT_FILE $MAIL_HTML_FILE < credentials.txt
```
