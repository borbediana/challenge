import smtplib
import subprocess
from smtplib import SMTPException
from smtplib import SMTP

# Import the email modules we'll need
from email.mime.text import MIMEText
from pyjavaproperties import Properties
p = Properties()
p.load(open('configuration.properties'))

# load connection data from configuration file
sender = p['username']
password = p['password']
receiver = ['b.antohidiana@gmail.com']
host = p['smtp.server']
port = p['smtp.port']

print "Call build.sh"
subprocess.call(['./build.sh'])


def sendEmail(host, port, sender, password):

	message = """From: From Person <from@fromdomain.com>
	To: To Person <to@todomain.com>
	Subject: SMTP e-mail test

	This is a test e-mail message.
	"""

	print message

	try:
		server = smtplib.SMTP(host, port)
		server.ehlo()
		server.login(sender,password)
		#server.sendmail(sender,receiver,message)
		server.close()    
		print "Successfully sent email"
	except SMTPException:
		print "Error: unable to send email"


sendEmail(host, port, sender, password)
