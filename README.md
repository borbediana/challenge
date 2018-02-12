# Challenge


## Prerequisites:

 - Python: 2.7
 - Git: 2.11
 - Docker: 18.01-ce


## Content:

I will refer to input sources/project as sources repository and output sources/project as binary repository. 
Be aware that is bad practice to commit binaries to repository (such as Git)!


This repository contains:

 - exercise.py - script that does all the work:
	- check for sources repository
	- build the sources
	- if the case: commit results to binary repository, send email to notice build failure
 - configuration.properties - contains configuration for: 
	- smtp server
	- sources repository
	- binary repository
	- workspace
 - execution.log - keeps track of the script execution, checks the latest commit of the source repository

 - pyjavaproperties.py file is dowloaded from https://bitbucket.org/jnoller/pyjavaproperties/downloads/ , makes it easy to handle the properties file



## Flow:

 - The scripts:
	- creates workspace
	- clones/updates source repository
	- clones/updates binary repository
	- runs build.sh from source repository - it runs the build based on last commit
	- if build is successful, then commits the result of the build on the binary repository
	- if the build fails, it sends email

## Notes:
 - in configuration.properties you must specify the source repository and binary repository. If you omit them, the current directory will be used.
 - if you omit source repository and binary repository, you must also omit workspace. Current directory will be used as workspace.
 - source repository can be the same with binary repository

