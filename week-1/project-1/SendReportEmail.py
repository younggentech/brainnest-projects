import smtplib
from time import sleep
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from schedule import repeat, every, run_pending
from configparser import ConfigParser  # importing file to read configuration params

SMTPs = {
    "gmail": {
        "server": "smtp.gmail.com",
    },
    "outlook": {
        "server": "smtp-mail.outlook.com",
    },
}
PORT = 587
recipients = []  # write recipients here
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


@repeat(every().day.at(scheduled_time))
def main():
    try:
        smtp = SMTPs.get(
            sender_email.split("@")[1].split(".")[0]  # to extract the domain (between @ and .) from email
        )
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "The Report"  # the subject of the email
        msg["From"] = sender_email
        attachment = "config.ini"  # this is the attachment file, which should be the report
        with open(attachment, "rb") as attach:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attach.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f"attachment; filename={attachment}")
        msg.attach(part)
        server = smtplib.SMTP(host=smtp.get("server"), port=PORT)
        server.starttls()
        server.login(sender_email, email_password)
        for recipient in recipients:
            server.sendmail(from_addr=sender_email, to_addrs=[recipient], msg=msg.as_string())
    except Exception as e:
        print(e)


if __name__ == "__main__":
    while 1:
        run_pending()
        sleep(1)
