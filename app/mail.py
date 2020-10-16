import smtplib
import ssl

def send_mail(receivers_email=None, melding=None):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "dat250python@gmail.com"
    password = "fEtryb-mugpuc-defmi1"

    message = (f"""\
    Mail fra bank:

    {melding}""")

    context = ssl._create_unverified_context()

    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receivers_email, message)
        print("mail sendt")
    except Exception as e:
        print(e)
    return

if __name__ == "__main__":
    send_mail()