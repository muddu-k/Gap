#!/bin/python
# -*- coding: ascii -*-
import sys
import xml.etree.ElementTree as ET


def loadprefix(prefixfile):
    # Module loads file containing all valid prefixes for applications
    # Returns a list object of valid sub-systems
    # prefixfile = string = Path and File name for location of input file
    try:
        with open(prefixfile) as subsystemfile:
            subsystemlist = (subsystemfile.read().splitlines())
            return(subsystemlist)
    #except (FileNotFoundError, IOError):  
    except Exception:
        print('Prefix file read failed')
        sys.exit(98)


global prefixlist
#pass the location of the Prefixlist.txt file and fill list
if len(sys.argv) > 2:
    prefixlist = loadprefix(sys.argv[2])
else:
    print('Invalid parameters, please provide path and file Name')
    sys.exit(99)


def ValidateJobname(job_name):
    # Module compares job naming to the list of valid sub-systems
    # Returns True if valid prefix, False if not valid
    # job_name = string = job name currently validation
    return(any(job_name.startswith(pre) for pre in prefixlist))


def appvalidation(xmlfile):
    # Module processes the application requested moving.  Performs the corp standards validations against each jobs settings
    # Returns 0 if successfully passes all validations, 1 if any error found in any job.  Information about the failure 
    # will be bubbled up to callin script for spool file.
    # xmlfile = string = application xml file to process
    ns = {'app': 'http://dto.wa.ca.com/application'}
    errordict = {}
    tree = ET.parse(xmlfile)
    xmlroot = tree.getroot()
    appschedule = appagent = None
    notvalidappschedule = notvalidappagent = False
    applicationname=xmlroot.attrib['name']
    print('Application Processing:', applicationname)

    # get applications run scheduling and agent
    for appdefault in xmlroot.findall('app:defaults', ns):
        for appsched in appdefault.findall('app:schedules/app:run/app:schedule', ns):
            appschedule = appsched.text
        for agent in appdefault.findall('app:rununit/app:agent', ns):
            appagent = agent.text
    # check scheduling and agent
    if appschedule is None:
        print("Application level default Schedule not defined.")
        notvalidappschedule = True
    if (appagent is None):
        notvalidappagent = True
        print("Application level default Agent not defined.")
    else:
        if not(appagent.startswith("%VAR")):
            print("Application level default Agent not valid, Please use global variable.")
            notvalidappagent = True

    if ( (appagent is not None) and  (not(appagent.startswith("%VAR")))):
        errordict[applicationname] = [' Application level default Agent is not valid; Please use a global variable.']


    # Begin processing all jobs
    for job in xmlroot.findall('*[@name]'):
        jobtype = job.tag.partition('}')[2]

        schedule = []
        noschedule = []
        jobname = donotrun = agent = request = None
        homeapplication = scheduledfrom = scheduledto = extscheduler = None

        #capture job name
        if job.attrib.get('qualifier') is not None:
            jobname = job.attrib.get('name') + '.' + job.attrib.get('qualifier')
        else:
            jobname = job.attrib.get('name')

        #capture information for agent/schedule/no run schedule/do not run/request - settings
        for agent in job.findall('app:agent', ns):
            agent = agent.text
        for run in job.findall('app:schedules/app:run/app:schedule', ns):
            schedule.append(run.text.upper())
        for norun in job.findall('app:schedules/app:norun/app:schedule', ns):
            noschedule.append(norun.text.upper())
        for donotrun in job.findall('app:donotrun', ns):
            donotrun = donotrun.text
        for rqst in job.findall('app:request', ns):
            request = rqst.text

        #capture information for external jobs
        if jobtype in ['ext_job', 'extmon_job']:
            for homeapp in job.findall('app:applid', ns):
                homeapplication = homeapp.text
            for scheduledfrom in job.findall('app:scheduled', ns):
                scheduledfrom = scheduledfrom.text
            for scheduledto in job.findall('app:scheduledlimit', ns):
                scheduledto = scheduledto.text
            for extsched in job.findall('app:extscheduler', ns):
                extscheduler = extsched.text

        #BEGIN validations
        errorlist = []
        #check job naming
        if not(jobtype in ['ext_job', 'extmon_job', 'link', 'task', 'file_trigger']):
            if not ValidateJobname(jobname):
                errorlist.append(' Not a Valid job name.')
        #check agent all jobs except external same scheduler, links and tasks as these 3 do not use any agent
        if (agent is None and notvalidappagent) and not(jobtype in ['ext_job','link','task']):
            errorlist.append(' Job level agent is Invalid or missing.')
        #check agent configuration is using global variable reference
        # external monitor other jobs use 2 formats do not check here
        if (agent is not None and (not(agent.startswith("%VAR")))) and not(jobtype in ['extmon_job']):
            errorlist.append(' Job agent is invalid, agent need to be a global variable.')
        #check for valid scheduling
        if len(schedule) == 0 and notvalidappschedule:
            errorlist.append(' Job Schedule is missing.')
        #check job has not been flagged as Do Not Run
        if donotrun == 'true':
            errorlist.append(' Job Do Not Run setting is checked.')
        #check that job has not been set as a Request job
        if request == 'true':
            errorlist.append(' Job marked as Request job.')
        #check that any Do Not Run setting is valid do not allow ANYDAY or DAILY
        if ('ANYDAY' in noschedule) or ('DAILY' in noschedule):
            errorlist.append(' Job DONOTRUN schedule has DAILY or ANYDAY.')
        #check for External jobs settings
        if jobtype in ['ext_job','extmon_job']:
            if homeapplication is None:
                errorlist.append(' External jobs Home Application is missing.')
            if (scheduledfrom is None):
                errorlist.append(' External job Scheduled "From or AT" is missing.')
            if (scheduledto is None):
                errorlist.append(' External job Scheduled "TO" is missing.')
            if (agent is not None and not(agent.startswith("%"))) and (jobtype in ['extmon_job']):
                errorlist.append(' External job agent is invalid, agent need to be a global variable.')
            if (extscheduler is not None) and (not(extscheduler.startswith("%"))):
                errorlist.append(' External job Scheduler Agent is invalid, agent need to be a global variable.')
        #END job validations

        #if any errors found thne add job and errors to dictionary
        if len(errorlist) > 0:
            errordict[jobname] = errorlist
    # End processing all jobs        

    return(errordict)


def printdict(printdict):
    for key, value in printdict.items():
        print("   ")
        print( key, "Validation Errors: ")
        #[print("   ",message) for message in value]
        for message in value:
            print("   ", message)
        print("   ")


def main(args):
    # basepath=args[1]
    appxmlname = args
    validationdict = appvalidation(appxmlname)

    if len(validationdict) > 0:
        printdict(validationdict)
        return(1)
    else:
        return(0)


if __name__ == '__main__':
    returncode =0
    if len(sys.argv) > 2:
        returncode = main(sys.argv[1])
    else:
        print('Invalid parameters, please provide path and file Name')
        sys.exit(99)

    #bubble back up to CAWA the return code value
    if returncode == 0:
        print('All Jobs pass Validation!')
        #print('Returncode= 0')
        sys.exit(0)
    else:
        #print('Returncode= 1')
        sys.exit(1)
