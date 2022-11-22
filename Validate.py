#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import os
import xml.etree.ElementTree as ET

def main(appfilename):    
    checkdic = fillDictionaryFromXML(appfilename)   #fill dictionary from xml
    finaldic = checknewjobsdata(checkdic)           #check the jobs information
    returncode = validatefinalresults(finaldic)     #validate the job check
    return returncode

def validatefinalresults(testdic):    
    returncode = 0
    #cycle through the dictionary if any entries do not have NONE then invalid jobs
    for job in testdic:
        if testdic[job]['INVALID_ENTRIES'] != 'NONE':
            print('Job', job, 'has Invalid Entries:', testdic[job]['INVALID_ENTRIES'])
            returncode = 1
    return returncode

def checkKeyInDictionary(searchdict, searchkey):
    #this will build a unique key value for saving to dictionary
    counter = 1
    newSearchKey = searchkey
    while newSearchKey in searchdict:
        #increment key as original was found
        newSearchKey = searchkey + '-' + str(counter)
        counter += 1
    return newSearchKey

def fillDictionaryFromXML (checkfile):    
    #this block of code will fill a dictionary with the xml data for application and will return a dictionary object
    #xmlroot = xml object containing file read    
    mydict = {}     #Main Dictionary used to hold all app and job information
    jobdict = {}  #Application or Individual job information dictionary
    tagheadingoffset = 34    
    
    #Get the xml information
    #THE INFORMATION COMING IN HERE IS STRAIGHT FROM THE JOB STEP IN DAVES_TEST_VALIDATE
    #ARGUMENTS BEING PASSED /home/users/da6m157/Python/Validate.py /home/users/da6m157/Python/TEST_PISORRECONDLY.xml
    #THIS WILL NEED TO BE ADJUSTED ONCE WE DETERNMINE LOCATION OF FILES    
    tree = ET.parse(checkfile)
    xmlroot = tree.getroot()

    #get application name
    if 'name' in xmlroot.attrib:
        app_name = xmlroot.attrib['name']
        jobdict['app_name'] = app_name

    #cycle through the child elements
    for child in xmlroot:
        #get job name if we have gotten to a jobs definition
        job_name = None
        job_qualifier = None
        if 'name' in child.attrib:         
            job_name = child.attrib['name']
        if 'qualifier' in child.attrib:         
            job_qualifier = child.attrib['qualifier']
        if job_qualifier is not None:
            job_name = job_name + "." + job_qualifier    
        #Clear job dictionary for fill we would only have a job name once we are past the applications information
        if job_name is not None:
            jobdict = {}
            jobdict['Job_Type'] = child.tag.partition('}')[2]
        #cycle through all the elements of the child  
        for jobattribute in child.iter():
            #save application information if hit the job templates section of xml
            if jobattribute.tag.partition('}')[2] == 'job_templates':                       
                mydict['APPLICATION'] = dict(sorted(jobdict.items()))
                pastJobTemplates = True
                jobdict = {}
            #if tags we need and there is a value for the xml tag then save the data        
            if (jobattribute.tag.partition('}')[2].upper() in ['REQUEST','SCHEDULE','AGENT','DONOTRUN','SCHEDULED','SCHEDULEDLIMIT']) and (jobattribute.text != None):
                #add child element to dictionary    
                jobdict[checkKeyInDictionary(jobdict, jobattribute.tag.partition('}')[2])] = jobattribute.text  #add value to dictionary            
        #save job information
        if job_name is not None:
            jobdict['JobName'] = job_name  #add job name to dictionary        
            mydict[job_name] = dict(sorted(jobdict.items()))

    return mydict

def checknewjobsdata(testdic):
    jobname = ''   
    #get sub-system listing - THIS IS HARD CODED WILL NEED TO ADJUST BASED ON WHERE SAVING THE FILES
    List = open("/home/users/da6m157/Python/SubSystemsList.txt").read().splitlines()    
    #MUDDU-SHOULD WE CLOSE THIS OBJECT BEFORE EXITING THE MODULE?

    appHasRunScheduling = False
    appHasAgent = False

    for key in testdic:            
        validJobName = True
        validOmniJobName = False
        errormsg = None        
        #if application record check its data
        if key == 'APPLICATION':
            #set app has Agent
            if 'agent' in testdic[key]:
                appHasAgent = True
            #set app has Run Scheduling
            if 'schedule' in testdic[key]:
                appHasRunScheduling = True
            #app records are always valid
            testdic[key]['INVALID_ENTRIES'] = 'NONE'
        else:
            if (testdic[key]['Job_Type'].upper() == 'LINK') or (testdic[key]['Job_Type'].upper() == 'TASK'):                            
                testdic[key]['INVALID_ENTRIES'] = 'NONE'
            elif (testdic[key]['Job_Type'].upper() == 'EXT_JOB') or (testdic[key]['Job_Type'].upper() == 'EXTMON_JOB'):
                #external jobs check for the scheduled limits
                if ('scheduled' not in testdic[key]) or ('scheduledlimit' not in testdic[key]):
                    errormsg = errormsg + ' Invalid Scheduled Limits'
            else:
                #get the job name without qualifier
                if "." in testdic[key]['JobName']:
                    jobname = testdic[key]['JobName'][:testdic[key]['JobName'].find('.')]
                else:
                    jobname = testdic[key]['JobName']                    
                # Omni name job validation
                if jobname[0:4].upper() in ['PAM_','PPC_']:
                    validOmniJobName = True
                elif jobname[0:5].upper() in ['PAXE_','PICM_','PMDS_','PEMR_','PESP_','PINV_','PMCM_','POMS_','PPAL_','PPUB_','PSDC_','PWMS_']:
                    validOmniJobName = True
                elif jobname[0:6].upper() in ['BOPIS_','PCUST_','PITEM_','PXREF_']:
                    validOmniJobName = True
                elif jobname[0:7].upper() in ['PACMAN_','PCLEAR_','PHBASE_','PNGPOS_','PPURGE_','PTOOLS_','PTRANS_']:
                    validOmniJobName = True
                elif jobname[0:8].upper() in ['PREPORT_','PSELECT_','PROCESS_']:
                    validOmniJobName = True
                elif jobname[0:9].upper() in ['PAUTOPOP_','PCATALOG_','PHYSICAL_','PPRICECA_','PPRICEJP_','PPRICEUK_','PPRICING_','PPRODUCT_','PPUBLISH_']:
                    validOmniJobName = True
                elif jobname[0:11].upper() in ['POSRECLAIM_']:
                    validOmniJobName = True
                
                if not validOmniJobName:
                    # check for prod
                    if jobname[0:1].upper() != 'P':
                        errormsg = 'First letter of Job name not P'

                    # check for subsystem name
                    if jobname[1:4] not in List:
                        errormsg = errormsg + ' Invalid SubSystem Name'
        
            #if this tag in file then invalid, trying to push a job that never runs
            if 'donotrun' in testdic[key]:
                errormsg = errormsg + ' Job has donotrun setting'
            
            #if request setting = true invalid, trying to push a bypassed job
            if 'request' in testdic[key]:
                if testdic[key]['request'] == 'true':
                    errormsg = errormsg + ' Job has Request setting'

            #check for run scheduling
            if 'schedule' not in testdic[key]:
                if not appHasRunScheduling:
                    errormsg = errormsg + ' Job has NO Run Scheduling'
            #check for agent
            if 'agent' not in testdic[key]:
                if not appHasAgent:
                    errormsg = errormsg + ' Job has NO Agent'

        if errormsg is not None:
            testdic[key]['INVALID_ENTRIES'] = errormsg
        elif errormsg is None:
            testdic[key]['INVALID_ENTRIES'] = 'NONE'
        elif not validOmniJobName:
            testdic[key]['INVALID_ENTRIES'] = 'Invalid Omni Job Name'
    
    return testdic

#Main processing entry point
#should have received 2 arguments, the python script name and the app name validating
if len(sys.argv) == 2:
    returncode = main(sys.argv[1])
else:
    returncode = 1
    print('INVALID APP NAME MISSING')
#bubble back up to CAWA the return code value
if returncode == 0:
    print('Returncode= 0')    
    sys.exit(0)
else:
    print('Returncode= 1')
    sys.exit(1)
