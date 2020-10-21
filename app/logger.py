from datetime import datetime, timedelta
from app.mail import send_mail_fil
import pathlib

def log(username, status):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    file = pathlib.Path(f"./log-login/{now.year}-{now.month}-{now.day}.txt")
    past = datetime.today() - timedelta(days=1)
    if not file.exists():
        try:
            send_mail_fil("dat250python@gmail.com", "Log:", "Daglig log", f"./log-login/{past.year}-{past.month}-{past.day}.txt")
        except:
            send_mail_fil("dat250python@gmail.com", "Ingen log, ingen aktivitet", "Daglig log")
    with open(f"./log-login/{now.year}-{now.month}-{now.day}.txt", "a") as file:
        file.write(f"{now.year}-{now.month}-{now.day} {time} - {username} - {status}")
    if status == "Unsuccessful":
        check(now, time, username)
    with open(f"./log-login/{now.year}-{now.month}-{now.day}.txt", "a") as file:
        file.write(f"\n")
    return

def check(now, time, username):
    two_sec = datetime(100,1,1,00,0,2).time()
    five_min = datetime(100,1,1,00,5,0).time()
    five_min_two = datetime(100,1,1,00,5,2).time()
    time = datetime.strptime(time, '%H:%M:%S')
    with open(f"./log-login/{now.year}-{now.month}-{now.day}.txt", "r") as f:
        for lines in f:
            words = lines.split(" ")
            if words[3] == username and words[5] == "Unsuccessful\n":
                f_time = datetime.strptime(words[1], '%H:%M:%S')
                delta = (time-f_time)
                delta = str(delta)
                delta = datetime.strptime(delta, '%H:%M:%S').time()
                if delta < two_sec:
                    send_mail_fil("dat250python@gmail.com", f"Misstenkelig innlogging - {now}", "Potensiell trussel", f"./log-login/{now.year}-{now.month}-{now.day}.txt")
                    break
                if delta >= five_min and delta <= five_min_two:
                    send_mail_fil("dat250python@gmail.com", f"Misstenkelig innlogging - {now}", "Potensiell trussel", f"./log-login/{now.year}-{now.month}-{now.day}.txt")
                    break
    return

def log_transaction(user, from_acc, to_acc, value, now=datetime.now()):
    date = now.strftime("%Y-%m-%d")
    file = pathlib.Path(f"./log-transaction/{now.year}-{now.month}-{now.day}.txt")
    past = datetime.today() - timedelta(days=1)
    if not file.exists():
        try:
            send_mail_fil("dat250python@gmail.com", "Log:", "Daglig log", f"./log-login/{past.year}-{past.month}-{past.day}.txt")
        except:
            pass
    with open(f"./log-transaction/{date}.txt", "a") as file:
        file.write(f"{user} transfered {value}kr from {from_acc} to {to_acc}\n")
    if int(value) > 500:
        try:
            send_mail_fil("dat250python@gmail.com", "Log:", "Høy transaksjon", f"./log-login/{now.year}-{now.month}-{now.day}.txt")
        except:
            return
    pass