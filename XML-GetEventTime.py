import xml.etree.ElementTree as ET
import os
import csv


def eventparse(file):
    ns = {'e': 'http://dto.wa.ca.com/event'}
    tree = ET.parse(file)
    root = tree.getroot()
    event={}
    for desc in root.findall('e:eventsch/e:description', ns):
        for name in desc.findall('e:name',ns): 
            event["EVENT_NAME"] = name.text
        for executionuser in desc.findall('e:executionuser',ns):
            event["EXECUTIONUSER"] = executionuser.text
        for holdcount in desc.findall('e:holdcount',ns):
            event["HOLDCOUNT"] = holdcount.text
        for suspendcount in desc.findall('e:suspendcount',ns):
            event["SUSPENDCOUNT"] = suspendcount.text
    for app in root.findall('e:eventsch/e:action/e:runApplication', ns):
        event["APPLICATION"]=app.text
    for s in root.findall('e:eventsch/e:schedule', ns):
        sched=[]
        nosched=[]
        for schedule in s.findall('e:scheduleelement', ns):
            sched.append(schedule.attrib.get('original'))
        event["SCHEDULE"]= ','.join(sched)
        for noschedule in s.findall('e:noscheduleelement',ns):
            nosched.append(schedule.attrib.get('original'))
        if len(nosched) > 0:
            event["NOSCHEDULE"]= ','.join(nosched)
        for suspendelement in s.findall('e:suspendelement',ns):
            event["SUSPENDAT"] = suspendelement.text
        for resumeelement in s.findall('e:resumeelement',ns):
            event["RESUMEAT"] = resumeelement.text
        scripts=[]
        for script in root.findall('e:eventsch/e:script_name', ns):
            scripts.append(script.text)
        event["JAVASCRIPT"]= ','.join(scripts) 
    return(event)
                    
                

def main():
    ns = {'e': 'http://dto.wa.ca.com/event'}
    event_keys = ["EVENT_NAME", "APPLICATION","JAVASCRIPT",
                  "EXECUTIONUSER","SUSPENDCOUNT","HOLDCOUNT", 
                  "SCHEDULE","NOSCHEDULE","SUSPENDAT","RESUMEAT"]  
    xmlfilepath = input("Enter the file path: ")
    outpath = input("Enter the outfile path: ")
    outfile = input("Enter the outfile name: ")

    csv_out_file = os.path.join(outpath, outfile)

    xml_data_to_csv = open(csv_out_file, 'w', newline='', encoding='utf-8')
    csv_writer = csv.DictWriter(xml_data_to_csv, fieldnames=event_keys)
    
    csv_writer.writeheader()
    
    files = os.listdir(xmlfilepath)
    for file in files:
        event_file = os.path.join(xmlfilepath, file)
       # print(event_file)
        event_parse=eventparse(event_file)
        csv_writer.writerow(event_parse)                            
    xml_data_to_csv.close() 


if __name__ == '__main__':
    main()
