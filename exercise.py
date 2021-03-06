import smtplib
import subprocess
from smtplib import SMTPException
from smtplib import SMTP
from email.mime.text import MIMEText
from pyjavaproperties import Properties
import string
import os

def sendEmail(host, port, sender, password, msj, files_changed):

	SUBJECT = "Build failed!"
	message = string.join((
		"From: %s" % sender,
		"To: %s" % sender,
		"Subject: %s" % SUBJECT ,
		"",
		msj,
		files_changed
		), "\r\n")

	print message
	try:
		server = smtplib.SMTP(host, port)
		server.ehlo()
		server.login(sender,password)
		server.sendmail(sender,receiver,message)
		server.close()    
		print "Successfully sent email!"
	except SMTPException:
		print "Error: unable to send email!"


p = Properties()
p.load(open('configuration.properties'))

# load connection data from configuration file
sender = p['username']
password = p['password']
receiver = ['b.antohidiana@gmail.com']
host = p['smtp.server']
port = p['smtp.port']
source_repo=p['source.repo']
binary_repo=p['binary.repo']
workspace_dir=p['workspace.directory']

source_repo_dir="source_repo"
binary_repo_dir="binary_repo"


# checking repositories
if source_repo:
	print "Checking source repository"
else:
	print "Using current directory as source repository!"
	source_repo_dir = os.getcwd();

if binary_repo:
	print "Checking binary repository"
else:
	print "Using current directory as binary repository!"
	binary_repo_dir = os.getcwd();

# Check log file of script execution
scriptFilePath = os.getcwd() + "/execution.log"

if os.path.isfile(scriptFilePath):
	print "File ",scriptFilePath," exists"
else:
	print "File ",scriptFilePath," doesn't  exists. Creating it!"
	open(scriptFilePath,"w+")

# Checking local workspace
if os.path.isdir(workspace_dir):
	print "Workspace exists ",workspace_dir
else:
	if workspace_dir != "":
		print "Workspace directory doesn't exist. Creating workspace!"
		os.mkdir(workspace_dir)
	else:
		print "No workspace directory specified. Using current directory!"
		workspace_dir = os.getcwd()
		#quit()

# Build.sh file
if workspace_dir == os.getcwd():
	buildFilePath = workspace_dir + "/build.sh"
else:
	buildFilePath = workspace_dir + "/" + source_repo_dir + "/build.sh"

# Check build file exists
if os.path.isfile(buildFilePath):
	print "File ",buildFilePath," exists"
else:
	print "File ",buildFilePath," is missing. Aborting build execution!"
	quit()


# use local folder as workspace
if source_repo_dir == binary_repo_dir and source_repo_dir == os.getcwd():
	workspace_dir = os.getcwd()
	print "Workspace: ",workspace_dir

os.chdir(workspace_dir)

if os.path.isdir(source_repo_dir):
	print "Local repository already exists. Updating repository"
	os.chdir(source_repo_dir)
	subprocess.call(["git","pull"])
else:
	print "Creating local repository"
	subprocess.call(["git","clone", source_repo, source_repo_dir])
	os.chdir(source_repo_dir)

# last commit hash
lastCommit = subprocess.check_output(["git","rev-parse", "HEAD"])

# last commit from execution.log
lastLineFromLog = subprocess.check_output(['tail', '-1', scriptFilePath])
print "The previous commit the script ran on:",lastLineFromLog

# if the last commit from repository is already in execution.log, this means we have already ran the script for this commit
# else, we rerun the script and add commit to execution.log

if lastCommit == lastLineFromLog:
	print "Script already ran on commit", lastCommit, ". Build is skipped!"
	quit()
else:
	print "New commit found. Running build on commit",lastCommit
	if workspace_dir == source_repo_dir:
		sources_dir = workspace_dir
	else:
		sources_dir = workspace_dir + "/" + source_repo_dir + "/"
	
	print "sources_dir: ",sources_dir
	print "source_repo_dir: ",source_repo_dir
	print "workspace_dir: ",workspace_dir
	files_changed = subprocess.check_output(["git", "show"])
	result = subprocess.call([buildFilePath, sources_dir])


# if build is successfull, then copy the binary from source repo to binary repo and commit
if result == 0:
	# checking binary repository
	os.chdir(workspace_dir)

	if os.path.isdir(binary_repo_dir):
		print "Local binary repository already exists. Updating repository"
		os.chdir(binary_repo_dir)
		subprocess.call(["git","pull"])
	else:
		print "Creating local binary repository"
		subprocess.call(["git","clone", binary_repo, binary_repo_dir])
		os.chdir(binary_repo_dir)

	sources_dir_target = sources_dir +"/target/."

	if workspace_dir == binary_repo_dir:
		binaries_dir = workspace_dir
	else:
		binaries_dir = workspace_dir + "/" + binary_repo_dir + "/"

	subprocess.call(["cp", "-r", sources_dir_target, binaries_dir])
	os.chdir(binaries_dir)
	print "Check if we have changes!"
	changes = subprocess.check_output(["git", "status"])
	if "modified:" in changes:
		print "Changes exist, we will commit them for you!"
		subprocess.call(["git","add", "."])
		subprocess.call(["git","commit", "-m", "Commit binaries to binary_repo !"])
		subprocess.call(["git","push"])
	else:
		print "We don't have changes to commit!"
	# add hash to executing.log
	with open(scriptFilePath, 'a') as file:
    		file.write(lastCommit)
else:
	print "Build failed! Sending email to notice people!"
	f = open("error_file","r")
	error_message = f.read()
	sendEmail(host, port, sender, password, error_message, files_changed)

