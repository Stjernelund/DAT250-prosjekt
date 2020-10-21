import smtplib
import ssl
import email
from flask import session

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(receivers_email=None, melding=None):
    sender_email = "dat250python@gmail.com"
    password = "fEtryb-mugpuc-defmi1"

    message = MIMEMultipart()
    message['Subject'] = "Bekreft bankoverføring"
    message['From'] = sender_email
    message['To'] = receivers_email
    html = MIMEText(melding, "html")

    if 'user_id' in session:
        tfrom = session['tfrom']
        tto = session['tto']
        tsum = session['tsum']
        text = f"Hei, \nBankoverføringen er som følgende: \nFra konto: {tfrom} \nTil konto: {tto} \nBeløp: {tsum} kroner"
        tekst = MIMEText(text, "plain")
        message.attach(tekst)

    message.attach(html)

    context = ssl._create_unverified_context()
    receivers_email = receivers_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receivers_email, message.as_string()
        )

def send_mail_fil(receivers_email="dat250python@gmail.com", melding="Test", subject="Mail fra banken", filename=None):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "dat250python@gmail.com"
    password = "fEtryb-mugpuc-defmi1"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receivers_email
    message["Subject"] = "Mail fra banken"
    message["Bcc"] = receivers_email

    message.attach(MIMEText(melding, "plain"))

    if filename:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet,stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}"
        )
        message.attach(part)
    text = message.as_string()


    context = ssl._create_unverified_context()
    receivers_email = receivers_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receivers_email, text)
        print("mail sendt")
    #except Exception as e:
    #    print(e)
    #return

if __name__ == "__main__":
    send_mail_fil()