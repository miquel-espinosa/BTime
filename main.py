#!/usr/bin/env python3

from crontab import CronTab
import argparse
import subprocess, sys, os
from simple_term_menu import TerminalMenu
from datetime import date
import calendar
import re

def arguments():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest='opt')
    for opt in ["reset", "addtoday", "week", "edit", "addfixed", "delevent", "resetall", "show", "help"]:
        sp.add_parser(opt)
    args = parser.parse_args()
    FLAG = args.opt
    if FLAG == 'help':
        parser.print_help()
        print()
        print("   Please, type: `myday <option>´ where <option> can be: ")
        print('     <empty>    (if its left empty it will show your timetable for today)')
        print('     reset      (to reset your daily tasks)')
        print('     addtoday   (to define your daily tasks)')
        print('     week       (to show your timetable for the entire week)')
        print('     edit       (to edit any task)')
        print('     addfixed   (to define your weekly tasks)')
        print('     delevent   (to delete an event)')
        print('     resetall   (to delete all your cron tasks)')
        print('     show       (to show BTime message)')
        print('     help       (to show this message)')
        print()
        sys.exit()
    return FLAG

def get_username():
    username=subprocess.Popen('whoami', text=True, stdout=subprocess.PIPE).communicate()[0]
    return username[:-1]

def get_directory():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path

def get_day_of_week():
    my_date = date.today()
    return calendar.day_name[my_date.weekday()]

def get_cron():
    cron = CronTab(user=get_username())
    return cron

def get_job_title_msg(job):
    pattern = r'\"(.*)\".*\"(.*)\"'
    texto = re.search(pattern,job.command)
    titulo = texto.groups()[0]
    mensaje = texto.groups()[1]
    return titulo, mensaje

def print_horario_hoy(jobs,day_of_week):
    print( "                           "+day_of_week.upper())
    print( "    ----------------------------------------------------")
    for i in jobs:
        hora = str(i.hour)
        minuto = str(i.minute)
        if int(hora)<10: hora = str("0"+hora)
        if int(minuto)<10: minuto = str("0"+minuto)
        titulo, mensaje = get_job_title_msg(i)
        print("     "+hora+":"+minuto+"   "+titulo.upper()+". "+mensaje)
    print( "    ----------------------------------------------------")
    print()

def intro():
    print("------------------------------------------------------")
    print(" Hey, ", get_username(), ". Let's organize the day! 🕑 ")
    print("------------------------------------------------------")
    print()

def check_fin(char):
    if char == 'q':
        print()
        print("   ************************************************************************")
        print("    Felicidades tio, ya esta todo programado. Eres un grande. Lo petas hoy")
        print("   ************************************************************************")
        print()
        sys.exit(0)

def multiple_select(msg, list):
    print(msg)
    d = TerminalMenu(list).show()
    return list[d]

def choose_time(day_of_week):
    if day_of_week!="today":
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','Exit']
        msg = "Please select a day of the week"
        day = multiple_select(msg,days)
        print(" DAY: ", day)
        if day=='Exit': check_fin('q')
    else: day = None
    hora = input("Enter an hour [HH] (0-23) (q to exit): ")
    check_fin(hora)
    while not ( hora.isdigit() and int(hora)>=0 and int(hora)<24): hora = input("Please, enter an hour between 0-23: ")
    print(" HOURS: ", hora)
    min = input("Enter an minute [MM] (0-59): ")
    while not ( min.isdigit() and int(min)>=0 and int(min)<60): min = input("Please, enter a minute between 0-60: ")
    print(" MINUTES: ", min)
    return day,str(hora),str(min)

def title_and_text(comment):
    if comment == None: comment='today'
    title = input("Enter title of "+comment.upper()+" notification: ")
    print("Title: ",title)
    msg_text = input("Enter text of notification: ")
    print("Text: ",msg_text)
    return str("\""+title.upper()+"\""), str("\""+msg_text+"\"")

def notification_description(title,msg_text,hour,minute):
    if int(hour)<10: hour = str("0"+str(hour))
    if int(minute)<10: minute = str("0"+str(minute))
    print()
    print("---------------------------------")
    print("|----NOTIFICATION-DETAILS-------|")
    print("| Time: ",hour,":",minute,"               |")
    print("| Message: ",title.upper(),": ",msg_text)
    print("---------------------------------")
    print()

def add_notification(cron,title,msg_text,day,hour,minute,comment):
    path = get_directory()
    notification = str("XDG_RUNTIME_DIR=/run/user/$(id -u) notify-send -i "+path+"/clock.svg ")
    raise_vol = str(" && amixer -D pulse sset Master unmute && amixer -D pulse sset Master 15%")
    beep= str(" && play -q "+path+"/swiftly.mp3 -t alsa")
    lower_vol = str(" && amixer -D pulse sset Master 5%")

    final_command = str(notification+title+" "+msg_text+raise_vol+beep+lower_vol)

    job = cron.new(command=final_command, comment=comment)
    job.hour.on(int(hour))
    job.minute.on(int(minute))
    if day!= 'today': job.dow.on(day[0:3])

    # Reminder
    final_command = str(notification+title+" "+msg_text+lower_vol+beep)
    job2 = cron.new(command=final_command, comment=(comment+" reminder"))
    if int(minute)>5:job2.minute.on(int(minute)-5)
    else:
        diff = 5-int(minute)
        job2.minute.on(60-diff)
        if int(hour) > 0: hour = int(hour) - 1
    job2.hour.on(int(hour))
    if day!= 'today': job2.dow.on(day[0:3])

    cron.write()
    notification_description(title,msg_text,hour,minute)
    print(" STATUS: ",comment.upper()," notification added 😊 ")
    print("--------------------------------------------------")
    print()

def show_week(cron):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = get_day_of_week()
    for i in days:
        print()
        if today == i: show_day(cron,i,one_day=True)
        else: show_day(cron,i,one_day=False)

def print_horario_title():
    print(r"               _   _                      _       ")
    print(r"              | | | | ___  _ __ __ _ _ __(_) ___  ")
    print(r"              | |_| |/ _ \| '__/ _` | '__| |/ _ \ ")
    print(r"              |  _  | (_) | | | (_| | |  | | (_) |")
    print(r"              |_| |_|\___/|_|  \__,_|_|  |_|\___/ ")
    print(r"                                                  ")
    


def print_logo():
    print()
    print(r"       -----------------------------------------------------")
    print(r"                                                            ")
    print(r"              =  =           ____ _____ _                   ")
    print(r"           =    |   =       | __ )_   _(_)_ __ ___   ___    ")
    print(r"          =     |    =      |  _ \ | | | | '_ ` _ \ / _ \   ")
    print(r"          =      \   =      | |_) || | | | | | | | |  __/   ")
    print(r"           =      \ =       |____/ |_| |_|_| |_| |_|\___|   ")
    print(r"              =  =                                          ")
    print(r"                                                            ")
    print(r"                         N e v e r   b e   l a t e   🕑     ")
    print(r"                                                            ")
    print(r"       -----------------------------------------------------")
    print(r"                                                            ")
    print(r"                  Maintained by: Miquel Espinosa            ")
    print(r"                                                            ")

def error_msg():
    print()
    print()
    print()
    print("     Ups, error. Exiting BTime...")
    print()
    print("     . . . but remember . . . ")
    print()
    print("     N e v e r   b e   l a t e   🕑")
    print()
    print()
    
def show_day(cron, day_of_week, one_day):
    jobs = []
    for job in cron:
        if one_day: 
            if (job.comment=='today' or job.comment==day_of_week): 
                jobs.append(job)
        else:
            if (job.comment==day_of_week):
                jobs.append(job)
    jobs.sort(key=lambda x:(int(str(x.hour)),int(str(x.minute))))
    print_horario_hoy(jobs,day_of_week)


def delete_event(cron):
    ans = input('    Type the title or message of the event: ')
    print()
    jobs_titles = []
    jobs = []
    jobs_reminders = []
    for job in cron:
        title, messaje = get_job_title_msg(job)
        if ((ans.lower() in str(title.lower())) or (ans in str(messaje.lower()))):
            if (not ('reminder' in str(job.comment))):
                jobs_titles.append(str("("+str(job.comment)+") "+title+": "+messaje))
                jobs.append(job)
            elif ('reminder' in str(job.comment)):
                jobs_reminders.append(job)
    if not jobs_titles:
        print("    There is no event with such title or comment ☹")
        print()
        sys.exit()
    else:
        msg = " Select the event to be deleted: "
        selected = multiple_select(msg, jobs_titles)
        print(" EVENT DELETED: ", selected)
        index = jobs_titles.index(selected)
        cron.remove(jobs[index])
        cron.remove(jobs_reminders[index])
        cron.write()

def add_new_event(cron, day_of_week):
    if day_of_week=='today': show_day(cron,day_of_week,one_day=True)
    day,hour,min = choose_time(day_of_week)
    title, text = title_and_text(day)
    if day_of_week=='today': day='today'
    add_notification(cron,title,text,day,hour,min,day)


def main():

    try:

        FLAG = arguments()
        cron = get_cron()

        if FLAG==None:
            day_of_week = get_day_of_week()
            print_horario_title()
            show_day(cron, day_of_week, one_day=True)
            

        elif FLAG=='addtoday' or FLAG=='addfixed':
            if FLAG=='addtoday': day_of_week = 'today'
            else: day_of_week = get_day_of_week()
            intro()
            while True:
                add_new_event(cron,day_of_week)
        

        elif FLAG=='reset':
            print()
            ans=input("Please, confirm that you want to delete all non-fixed events: (y/n)")
            if ans!='y': sys.exit()
            cron.remove_all(comment='today')
            cron.remove_all(comment='today reminder')
            cron.write()
            print()
            print(" . . . Removing events from yesterday")
            print()

        elif FLAG=='week':
            show_week(cron)

        elif FLAG=='resetall':
            print()
            print('-------   ¡¡¡ CAUTION !!!   -------')
            print()
            ans=input("Please, confirm that you want to delete ALL cron tasks from your profile: (y/n)")
            if ans!='y': sys.exit()
            cron.remove_all()
            cron.write()
            print()
            print(" . . . Removing ALL tasks")
            print()

        elif FLAG=='show':
            print_logo()
            
        elif FLAG=='delevent':
            print()
            print("   --------- ¡¡¡ CAUTION !!! ---------")
            print("    You are going to delete an event")
            print("   -------------------------------------")
            print()
            delete_event(cron)

        elif FLAG=='edit':
            while True:
                print()
                a = input('    Press l to show week, e to edit, and q to exit: ')
                if a == 'l': show_week(cron)
                elif a == 'q': check_fin(a)
                elif a == 'e':
                    print()
                    delete_event(cron)
                    msg=" Select if the NEW event should be weekly or for today: "
                    options=["Today", "Weekly"]
                    result = multiple_select(msg, options)
                    print()
                    day_of_week='today'
                    if result == "Weekly": day_of_week=get_day_of_week()
                    add_new_event(cron,day_of_week)
    
    except KeyboardInterrupt:
        error_msg()

main()

