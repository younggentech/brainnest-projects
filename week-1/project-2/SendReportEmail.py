import datetime
import logging
import os.path
import smtplib
from time import sleep
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from schedule import repeat, every, run_pending
from configparser import ConfigParser  # importing file to read configuration params

##################################
# FEEL FREE TO MODIFY THIS SECTION
EMAIL_SUBJECT = ""  # specify the subject
ATTACHMENTS = []  # specify paths to attachments as strings
RECIPIENTS = []  # write recipients here as strings
# add your own SMTP if you need
SMTPs = {
    "gmail": {
        "server": "smtp.gmail.com",
    },
    "outlook": {
        "server": "smtp-mail.outlook.com",
    },
}
##################################

PORT = 587

try:  # trying to load settings from config.ini
    settings = ConfigParser()
    settings.read("config.ini")
    sender_email = settings["email"]["sender_email"]
    email_password = settings["email"]["email_password"]
    scheduled_time = settings["schedule"]["run-time"]
except KeyError:
    sender_email = ""  # the email
    email_password = ""  # the password
    scheduled_time = "9:00"

# specify config for logging, logs go to the terminal and to the file with the name DATE_OF_RUNNING_THE_SCRIPT.log
# for example 20.01.2023.log
logging.basicConfig(
    format="%(asctime)s-%(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%d.%m.%Y %H:%M:%S",
    handlers=[
        logging.FileHandler(
            filename=f"{datetime.datetime.now().date().strftime('%d.%m.%Y')}.log"
        ),
        logging.StreamHandler(),
    ],
)


@repeat(every().day.at(scheduled_time))
def main():
    try:
        logging.info("starting email forming and sending")
        smtp = SMTPs.get(
            sender_email.split("@")[1].split(".")[
                0
            ]  # to extract the domain (between @ and .) from email
        )
        msg = MIMEMultipart("alternative")
        msg["Subject"] = EMAIL_SUBJECT  # the subject of the email
        msg["From"] = sender_email
        # attaching specified files if they exist
        for attachment in ATTACHMENTS:
            if os.path.exists(attachment):
                with open(attachment, "rb") as attach:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attach.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", f"attachment; filename={attachment}"
                )
                msg.attach(part)
            else:
                # log that file was not found
                logging.error(f"file not found {attachment}")

        server = smtplib.SMTP(host=smtp.get("server"), port=PORT)
        server.starttls()
        server.login(sender_email, email_password)
        logging.info("successful login")
        for recipient in RECIPIENTS:
            server.sendmail(
                from_addr=sender_email, to_addrs=[recipient], msg=msg.as_string()
            )
            logging.info(f"email was sent to {recipient}")
    except Exception as e:
        logging.error(f"{e}", stack_info=True)
    logging.info("job finished")


if __name__ == "__main__":
    while 1:
        run_pending()
        sleep(1)
