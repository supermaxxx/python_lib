#This file is to get the configuration from file
import ConfigParser
import logging
import MySQLdb
import os
import sys
import urllib
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

#Email class
class sendmail(object):
    def __init__(self):
        self.MAIL_HOST = 'smtp.??.com'    # smtp server, eg: smtp.qq.com
        self.MAIL_USERNAME = '??????@??.com'    # username of your account, eg: 98***90@qq.com
        self.MAIL_PASSWORD = '??????'    # password of your account
    def run(self,mail_to,mail_subject,mail_message):
        emsg = MIMEMultipart()
        body = MIMEText(mail_message)  # mail_message
        emsg.attach(body)
        emsg['To'] = mail_to    # Where to send the mail, eg: 30***04@qq.com
        emsg['from'] = self.MAIL_USERNAME
        emsg['subject'] = mail_subject    # title of the mail
        try:
            session = smtplib.SMTP()
            session.connect(self.MAIL_HOST)
            session.login(self.MAIL_USERNAME,self.MAIL_PASSWORD)
            session.sendmail(self.MAIL_USERNAME,mail_to,emsg.as_string())
            session.close()
            print 'Success.'
        except Exception,e:
            print e
    def help():
        print "Usage: sendmail().run('30*****04@qq.com','Title','Message')"


#SMS class
class sendsms(object):
    def __init__(self):
        pass
    def run(self, phone, msg_text):
        data = urllib.urlencode({'msg':msg_text})
        cmd = 'curl '+ '"http://sms.sdo.com:9090/submit.asp?CPID=SDCYSF&PWD=P2N5G9X7&PID=500107&phone='+phone+'&msg='+data+'"'
        os.system(cmd)
        

class config(object):
   def __init__(self,conf):
       self.conf = conf
       self.value = None
   def get_config(self,section,name):
       config = ConfigParser.ConfigParser()
       config.read(self.conf)
       try:
           self.value = config.get(section,name)
       except ConfigParser.Error:
           self.value = None
           return self.Value
       else:
           return self.value


#The logger class
class mylogger(object):
   def __init__(self,filename):
       self.filename = filename
   def initlog(self):
       logging.basicConfig(filename=self.filename,level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
       logger = logging.getLogger()
       return logger


#The mysql class
class mysql(object):
    def __init__(self,user,passwd,db):
        self.conn = None
        self.cursor = None
        self.user = user
        self.passwd = passwd
        self.db = db

    def getconn(self):
        self.conn = MySQLdb.connect(host = "localhost",
                           user = self.user,
                           passwd = self.passwd,
                           db = self.db)
        return self.conn

    def change_db(self,db):
        self.conn.select_db(db)
        return self.conn

    def run(self,cmd):
        try:
            self.getconn()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)

        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(cmd);
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)

        self.cursor.close()
        self.conn.close()

    def get_response(self,cmd):
        try:
            self.getconn()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)

        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(cmd);
            rows = self.cursor.fetchall()
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return False,None
            except IndexError:
                print "MySQL Error: %s" % str(e)
                return False,None

        self.cursor.close()
        self.conn.close()
        return True,rows

         
#Write Log file class
class writelogfile(object):
    def __init__(self,logname):
        self.logfilename = logname

    def log(self,logmsg):
        fd = open(self.logfilename, 'a')
        fd.write(logmsg)
        fd.close()


if __name__ == '__main__':
    pass
    #sendsms().run('137*****677','This is a test')
    #sendmail().run('30*****04@qq.com','Title','Message')
