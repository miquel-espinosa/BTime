#!/usr/bin/env python3

from crontab import CronTab
import argparse
import subprocess, sys
from simple_term_menu import TerminalMenu
from datetime import date
import calendar
import re

def arguments():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest='opt')
    for opt in ["reset", "today", "week", "edit", "fixed", "help"]:
        sp.add_parser(opt)
    args = parser.parse_args()
    FLAG = args.opt
    if FLAG == 'help':
        parser.print_help()
        print()
        print("   Please, type: `myday <option>´ where <option> can be: ")
        print('     <empty> (if its left empty it will show your timetable for today)')
        print('     reset   (to reset your daily tasks)')
        print('     today   (to define your daily tasks)')
        print('     week    (to show your timetable for the entire week)')
        print('     edit    (to edit any task)')
        print('     fixed   (to define your weekly tasks)')
        print('     help    (to show this message)')
        print()
        sys.exit()
    return FLAG

def get_username():
    username=subprocess.Popen('whoami', text=True, stdout=subprocess.PIPE).communicate()[0]
    return username[:-1]

def get_day_of_week():
    my_date = date.today()
    return calendar.day_name[my_date.weekday()]

def get_cron():
    cron = CronTab(user=get_username())
    return cron

def print_horario_hoy(jobs,day_of_week):
    print()
    print( " -----------TIMETABLE "+day_of_week.upper()+"-----------")
    pattern = r'notify-send \"(.*)\".*\"(.*)\"'
    for i in jobs:
        hora = str(i.hour)
        minuto = str(i.minute)
        if int(hora)<10: hora = str("0"+hora)
        if int(minuto)<10: minuto = str("0"+minuto)
        texto = re.search(pattern,i.command)
        titulo = texto.groups()[0]
        mensaje = texto.groups()[1]
        print("  "+hora+":"+minuto+"   "+titulo.upper()+". "+mensaje)
    print( " --------------------------------------")
    print()

def intro():
    print("------------------------")
    print(" Hey, ", get_username(), ". Let's organize the day! 🕑 ")
    print("------------------------")
    print()

# def choose_option():
#     print("Choose between options (select time) or text (enter time): ")
#     options=["options","text"]
#     terminal_menu = TerminalMenu(options).show()
#     return options[terminal_menu]

def check_fin(char):
    if char == 'q':
        print()
        print("************************")
        print("Felicidades tio, ya esta todo programado. Eres un grande. Lo petas hoy")
        print("************************")
        sys.exit(0)
    else: return

# def choose_time_options():
#     hours = ["07","08","09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]
#     minutes = ["05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
#     print("Please select an hour for your event")
#     h = TerminalMenu(hours).show()
#     print(" HOURS: ", hours[h])
#     print("Please select a minute for your event")
#     m = TerminalMenu(minutes).show()
#     print(" MINUTES: ", minutes[m])
#     return hours[h], minutes[m]
    
def choose_time_text(day_of_week):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','Exit']
    if day_of_week!="today": 
        print("Please select a day of the week")
        d = TerminalMenu(days).show()
        day = days[d]
        if day=='Exit': check_fin('q')
    else: day = None
    hora = input("Enter an hour (HH) (q to exit): ")
    check_fin(hora)
    print(" HOURS: ", hora)
    min = input("Enter an minute (MM): ")
    print(" MINUTES: ", min)
    return day,hora,min

def title_and_text(comment):
    title = input("Enter title of "+comment.upper()+" notification: ")
    print("Title: ",title)
    msg_text = input("Enter text of notification: ")
    print("Text: ",msg_text)
    return str("\""+title.upper()+"\""), str("\""+msg_text+"\"")

def notification_description(title,msg_text,hour,minute):
    if int(hour)<10: hour = str("0"+hour)
    if int(minute)<10: minute = str("0"+minute)
    print()
    print("---------------------------------")
    print("|----NOTIFICATION-DETAILS-------|")
    print("| Time: ",hour,":",minute,"               |")
    print("| Message: ",title.upper(),": ",msg_text)
    print("---------------------------------")
    print()

def add_notification(cron,title,msg_text,day,hour,minute,comment):
    notification = "XDG_RUNTIME_DIR=/run/user/$(id -u) notify-send "
    beep= " && play -q ~/swiftly.mp3 -t alsa"

    final_command = str(notification+title+" "+msg_text+beep)

    job = cron.new(command=final_command, comment=comment)
    job.hour.on(hour)
    job.minute.on(minute)
    if day!= None: job.dow.on(day[0:3])

    # Reminder
    job2 = cron.new(command=final_command, comment=(comment+" reminder"))
    if int(minute)>5:job2.minute.on(int(minute)-5)
    else:
        diff = 5-int(minute)
        job2.minute.on(60-diff)
        if int(hour) > 0: hour = int(hour) - 1
    job2.hour.on(hour)
    if day!= None: job2.dow.on(day[0:3])

    cron.write()
    notification_description(title,msg_text,hour,minute)
    print(" STATUS: ",comment.upper()," notification added 😊 ")
    print("--------------------------------------------------")
    print()


    
def show_day(cron, day_of_week, one_day):
    jobs = []
    for job in cron:
        if one_day: 
            if (job.comment=='today' or job.comment==day_of_week): jobs.append(job)
        else:
            if (job.comment==day_of_week): jobs.append(job)
    jobs.sort(key=lambda x:(int(str(x.hour)),int(str(x.minute))))
    print_horario_hoy(jobs,day_of_week)



def main():

    FLAG = arguments()
    cron = get_cron()

    if FLAG==None:
        day_of_week = get_day_of_week()
        show_day(cron, day_of_week, one_day=True)
        

    elif FLAG=='today' or FLAG=='fixed':
        if FLAG=='today': day_of_week = 'today'
        else: day_of_week = get_day_of_week()
        intro()
        while True:
            day,hour,min = choose_time_text(day_of_week)
            title, text = title_and_text(day)
            add_notification(cron,title,text,day,hour,min,day_of_week)

    elif FLAG=='reset':
        print()
        print(" . . . Removing items from yesterday")
        print()
        
        cron.remove_all(comment='today')

    elif FLAG=='week':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i in days:
            show_day(cron,i,one_day=False)
            print()

    # elif FLAG=='edit':

    





main()