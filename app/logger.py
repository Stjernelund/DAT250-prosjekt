from datetime import datetime, timedelta
import os
from app.mail import send_mail

def log(username, status):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    with open(f"./logs/{now.year}-{now.month}-{now.day}.txt", "a") as file:
        file.write(f"{now.year}-{now.month}-{now.day} {time} - {username} - {status}\n")
    if status == "Unsuccessful":
        check(now, time, username)
    return

def check(now, time, username):
    two_sec = datetime(100,1,1,00,0,2).time()
    five_min = datetime(100,1,1,00,5,0).time()
    five_min_two = datetime(100,1,1,00,5,2).time()
    time = datetime.strptime(time, '%H:%M:%S')
    with open(f"./logs/{now.year}-{now.month}-{now.day}.txt", "r") as f:
        for lines in f:
            words = lines.split(" ")
            if words[3] == username and words[5] == "Unsuccessful\n":
                f_time = datetime.strptime(words[1], '%H:%M:%S')
                delta = (time-f_time)
                delta = str(delta)
                delta = datetime.strptime(delta, '%H:%M:%S').time()
                if delta < two_sec:
                    send_mail("admin@gmail.com", f"Misstenkelig innlogging - {now}")
                    break
                if delta >= five_min and delta <= five_min_two:
                    send_mail("admin@gmail.com", f"Misstenkelig innlogging - {now}")
                    break
    return

def log_transactions(username, value):
    
    pass
