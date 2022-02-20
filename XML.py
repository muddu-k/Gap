import xml.etree.ElementTree as ET
import os
#fileline = 'JOBNAME,AGENT,SUBAPPLICATION,'
outfile = open('out.txt','w')
#path = input("Enter the path of your file: ")
path = "C:\\Users\\mu6g8mn\\Documents\\1SCEDULING\\Extract"
os.chdir(path)
#appnm = input("Enter XML name: ")
appnm='SAMPLE.xml'
ns = {'app' : 'http://dto.wa.ca.com/application'}
tree = ET.parse(appnm)
root = tree.getroot()
print (root.attrib.get('name'))
for applopts in root.findall('app:applopts',ns):
    for applwait in applopts.findall('app:wait',ns):
        print(applwait.text)
    for estimate_endtime in applopts.findall('app:estimate_endtime',ns):
        print(estimate_endtime.text)
    for prop_dueout in applopts.findall('app:prop_dueout',ns):
        print(prop_dueout.text)
    for apphold in applopts.findall('app:hold',ns):
        print(apphold.text)
    for noinherit in applopts.findall('app:noinherit',ns):
        print(noinherit.text)
    for notrigger_ifactive in applopts.findall('app:notrigger_ifactive',ns):
        print(notrigger_ifactive.text)
    for suppress_nowork_notification in applopts.findall('app:suppress_nowork_notification',ns):
        print(suppress_nowork_notification.text)
    for reason_required in applopts.findall('app:reason_required',ns):
        print(reason_required.text)
for appdefault in root.findall('app:defaults',ns):
    for schedules in appdefault.findall('app:schedules',ns):
        for apprun in schedules.findall('app:run',ns):
            for appsched in apprun.findall('app:schedule',ns):
                print ("App Schedule:")
                print(appsched.text)
        for appnorun in schedules.findall('app:norun',ns):
            for appnosched in appnorun.findall('app:schedule',ns):
                print("App No schedule:")
                print(appnosched.text)
    for rununit in appdefault.findall('app:rununit',ns):
        for appagent in rununit.findall('app:agent',ns):
            print ("App Agent:")
            print(appagent.text)
for unixjob in root.findall('app:unix_job',ns):
    print('Jobname:')
    print (unixjob.attrib.get('name')+'.'+unixjob.attrib.get('qualifier'))
    print('successor:')
    SUCCES=[]
    for dependencies in unixjob.findall('app:dependencies',ns):
        for rel in dependencies.findall('app:relconditionlist',ns):
            for relcon in rel.findall('app:relcondition',ns):
                    for succes in relcon.findall('app:successorname',ns):
                        SUCCES.append(succes.text)
    SUCCES.sort()
    print(SUCCES)
    print('Agent:')
    for agent in unixjob.findall('app:agent',ns):
        print(agent.text)
    for cmdname in unixjob.findall('app:cmdname',ns):
        print (cmdname.text)
    for args in unixjob.findall('app:args',ns):
        print (args.text)
