from datetime import datetime, timedelta
from icalendar import Calendar, Event
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from importlib import reload
from validate_email import validate_email
import smtplib
import json
import re
import os
import csv

class Wmt2Ics:
    """
       This class will accept user input from the command line.
       It will ask the user to type in a pay period and then paste
       a schedule from the Views:My Schedule view in wmtscheduler.
       It will take the pasted data, as copied from wmtscheduler and 
       place in schedule[]
    """
    def __init__(self, run_method):
        self.run_method = run_method
        self.basepath = os.path.dirname(__file__)
        self.config_file = os.path.abspath(os.path.join(self.basepath,"wmtconfig.json"))
        self.cats_file = os.path.abspath(os.path.join(self.basepath,"shift_cats.data"))
        self.save_as = os.path.abspath(os.path.join(self.basepath,"Pay_Period_"))
        self.eval_run_method()

    def eval_run_method(self):
        if self.run_method == "desktop":
            self.desktop = os.path.expanduser("~/Desktop")
            self.save_as = os.path.abspath(os.path.join(self.desktop,"Pay_Period_"))
            self.obtainData()
            self.buildShiftCats()
            self.addNewCategory()
            self.createCalendar()
        elif self.run_method == "email":
            self.getConfig()
            self.obtainData()
            self.buildShiftCats()
            self.addNewCategory()
            self.createCalendar()
            print("Sending Email with attachment -> "+self.outfile)
            self.sendEmail()

    def obtainData(self):
        """
        Not callable by user, will split pasted data into 
        attrib: schedule[]
        attrib: shifts[]
        attrib: dates[]
        This method will call buildShiftCats()
        """
        print("\n")
        self.pay_period = input("Enter the pay period\n")
        self.schedule = []
        print("Paste the schedule:")
        while True:
            self.schedule.append(input())
            if len(self.schedule) == 42:
                break
        self.shifts = self.schedule[2::3]
        self.dates = self.schedule[1::3]

    def buildShiftCats(self):
        """Not callable by user. Creates the
        attrib: shift_cats{}
        Uses the the shift_cats.txt file to create a dict 
        for which shifts[] will be compared against.
        It will contain in each line (The shift name from pasted schedule, 
        shift start time, shift lenght, Name to display on calendar)
        """
        self.shift_cats = {}
        if not os.path.isfile(self.cats_file):
            os.mknod(self.cats_file)
        with open(self.cats_file, 'r') as f:
            self.reader = csv.reader(f)
            for row in self.reader:
                self.shift_cats[row[0]] = (row[1],int(row[2]),row[3],)

    def addNewCategory(self):
        """Not callable by user. Will add during the session 
        any shift not found in shift_cats{}
        It will ask for user input
        attrib: time
        attrib: length
        attrib: display name for calendar
        This method calls createCalendar()"""
        for shift in self.shifts:
            if shift not in self.shift_cats:
                print(shift + " Not found. Enter start time for shift (format: 00:00:00)")
                self.time = input()
                print("Length of shift in hours")
                self.length = input()
                print("Calendar display name")
                self.shift_name = input()
                self.new_category = [shift,self.time,self.length,self.shift_name]
                with open(self.cats_file, "a+", newline='') as f:
                    self.csv_writer = csv.writer(f)
                    self.csv_writer.writerow(self.new_category)
                self.shift_cats.clear()
                self.buildShiftCats()

    def createCalendar(self):
        """
        Certainly not callable by user...
        Creates the entries for icalendar.
        attrib: ical[] (Used to store a list of tuples for each shift)
        attrib: events[] (Used to store the event = Event() for icalendar ics creation)
        attrib: event = Event() creates new event
        attrib: cal (Creates Calendar() object)
        This method will call sendEmail()
        """
        self.ical = []
        self.events =[]
        self.outfile = self.save_as+self.pay_period+".ics"
        for i in range(len(self.shifts)):
            if self.shifts[i] in self.shift_cats.keys():
                self.name = self.shift_cats[self.shifts[i]][2]
                self.date_time = self.dates[i] + " " + self.shift_cats[self.shifts[i]][0]
                self.date_time = datetime.strptime(self.date_time, "%m/%d/%Y %H:%M:%S")
                self.time = self.shift_cats[self.shifts[i]][0]
                self.hours = self.shift_cats[self.shifts[i]][1]
                self.ical.append((self.name, self.date_time, self.hours))
        for x, i in enumerate(self.ical):
            event = Event()
            if i[0] == "RDO":
                event.add("summary", i[0])
                event.add("description", "ZOB")
                event.add("dtstamp", i[1])
                event.add("dtstart", i[1].date())
                event.add("dtend", i[1].date())
                self.events.append(event)
            else:
                event.add("summary", i[0])
                event.add("description", "ZOB")
                event.add("dtstamp", i[1])
                event.add("dtstart", i[1])
                event.add("dtend", i[1] + timedelta(hours=i[2]))
                self.events.append(event)
        self.cal = Calendar()
        self.cal.add('prodid', '-//Michael H. Roberts//WMT TO ICS//')
        self.cal.add('version', '2.0')
        self.cal.add('calscale', 'GREGORIAN')
        for evnt in self.events:
            self.cal.add_component(evnt)
        with open(self.outfile, 'wb') as f:
            f.write(self.cal.to_ical())

    def removeFile(self):
        '''Removes the pay_period_x.ics file from the folder. Nobody has time for them to build up.
        '''
        if os.path.exists(self.outfile):
            os.remove(self.outfile)

    def getConfig(self): 
        if os.stat(self.config_file).st_size == 0:
            print("\n")
            print("You need to perform Setup \n")
            print("Enter your SMTPSERVER (ex. smtp.gmail.com): \n")
            self.srv = input("-> ")
            print("\n")
            print("Enter your SMTPSERVER PORT (ex. 587): \n")
            self.prt = input("-> ")
            print("\n")
            print("Enter the email address used to send the email: \n")
            self.snd = input("-> ")
            print("\n")
            while validate_email(self.snd) == False:
                print("Seems like that might not be a proper email address :( \n")
                self.snd = input("Re-Type Email, carefully now...-> ")
            else:
                pass
            print("\n")
            print("Enter the password for the email account used to send email: \n")
            self.pwd = input("-> ")
            print("\n")
            print("Enter the email you wish to receive .ics file: \n")
            self.rcv = input("-> ")
            print("\n")
            while validate_email(self.rcv) == False:
                print("Seems like that might not be a proper email address :( \n")
                self.rcv = input("Re-Type Email, carefully now...-> ")
            else:
                pass
            print("\n")
            print("Is this information Correct? \n")
            print("SMTPSERVER -> "+ self.srv+"\n")
            print("SMTPPORT -> "+ self.prt+"\n")
            print("EMAIL FROM -> "+ self.snd+"\n")
            print("PASSWORD -> "+ self.pwd+"\n")
            print("EMAIL TO -> "+ self.rcv+"\n")
            self.choice = input("Type 'Y' for yes, 'N' for No -> ")
            if self.choice == "Y" or "y":
                self.Setup(self.srv,self.prt,self.snd,self.pwd,self.rcv)
            else:
                self.getConfig()
            self.getConfig()
        else:
            with open(self.config_file, 'r' ) as f:
                self.config = f.read()
            self.cfg = json.loads(self.config)
            if self.cfg['APP_PWD'] == "":
                self.cfg['APP_PWD'] = os.environ.get('GMAIL_APP_PWD')
            self.smtpserver = self.cfg["SMTPSERVER"]
            self.smtpport = self.cfg["SMTPPORT"]
            self.emailFrom = self.cfg["SENDER"]
            self.app_passwd = self.cfg["APP_PWD"]
            self.emailReceiver = self.cfg["RECEIVER"]

    def sendEmail(self):
        """Sends the pay_period_xx.ics file to email account"""
        self.sender = self.emailFrom
        self.receiver = self.emailReceiver
        self.subject = "Pay Period " + self.pay_period
        self.msg = MIMEMultipart()
        self.msg['From'] = "Web Scheduler to ICS"
        self.msg['TO'] = self.receiver
        self.msg['Subject'] = self.subject
        self.body = "Have a pleasant day!\n"
        self.msg.attach(MIMEText(self.body,'plain'))
        self.attachment = open(self.outfile, 'rb')
        self.part = MIMEBase('application', 'octet-stream')
        self.part.set_payload((self.attachment).read())
        encoders.encode_base64(self.part)
        self.part.add_header('Content-Disposition', "attachment; filename= pay_period_"+self.pay_period+".ics")
        self.msg.attach(self.part)
        self.text = self.msg.as_string()
        self.server = smtplib.SMTP(self.smtpserver, self.smtpport)
        self.server.starttls()
        self.server.login(self.sender, self.app_passwd)
        self.server.sendmail(self.sender, self.receiver, self.text)
        self.server.quit()
        print("Email Sent Successfully!")
        self.removeFile()
        exit()

    @classmethod
    def Setup(self, svr, prt, snd, pwd, gets):
        self.basepath = os.path.dirname(__file__)
        self.config_file = os.path.abspath(os.path.join(self.basepath,"wmtconfig.json"))
        self.svr = svr
        self.prt = prt
        self.snd = snd
        self.pwd = pwd
        self.gets = gets
        self.config_data = '{"SMTPSERVER":"'+self.svr+'","SMTPPORT":"'+self.prt+'","SENDER":"'+self.snd+'","APP_PWD":"'+self.pwd+'","RECEIVER":"'+self.gets+'"}'
        self.config_json = json.loads(self.config_data)
        with open(self.config_file, 'w+') as f:
            f.write(json.dumps(self.config_json, indent = 3))


def main():
    Wmt()
if __name__ == '__main__':
    main()