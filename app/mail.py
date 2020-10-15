import smtplib, ssl

def send_mail(receivers_email="sindrevatnaland97@gmail.com", melding="Test"):
    print("mail sendt")
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "dat250python@gmail.com"
    password = "fEtryb-mugpuc-defmi1"

    message = (f"""\
    Mail fra bank:

    {melding}""")

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receivers_email, message)
        # TODO: Send email here
    except Exception as e:
    # Print any error messages to stdout
        print(e)
    return




if __name__ == "__main__":
    send_mail()