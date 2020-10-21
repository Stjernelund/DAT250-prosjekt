import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(receivers_email=None, melding=None):
    #smtp_server = "smtp.gmail.com"
    #port = 587
    sender_email = "dat250python@gmail.com"
    password = "fEtryb-mugpuc-defmi1"

    message = MIMEMultipart()
    message['Subject'] = "Bekreft bankoverføring"
    message['From'] = sender_email
    message['To'] = receivers_email
    html = MIMEText(melding, "html")
    message.attach(html)

    #message = (f"""\
    #Mail fra bank:

    #{melding}""")

    context = ssl._create_unverified_context()
    receivers_email = receivers_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receivers_email, message.as_string()
        )
    #try:
    #    server = smtplib.SMTP(smtp_server,port)
    #    server.ehlo()
    #    server.starttls(context=context)
    #    server.ehlo()
    #    server.login(sender_email, password)
    #    server.sendmail(sender_email, receivers_email, message.as_string())
    #    print("mail sendt")
    #except Exception as e:
    #    print(e)
    #return

if __name__ == "__main__":
    send_mail()