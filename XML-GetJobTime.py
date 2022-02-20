import xml.etree.ElementTree as ET
import csv
import os


def main():
    ns = {'app': 'http://dto.wa.ca.com/application'}
    job_type = {'link',
                'unix_job',
                'extmon_job',
                'ext_job',
                'filemon_job',
                'nt_job',
                'oracle_apps_single_request',
                'oracle_apps_request_set',
                'peoplesoft_job',
                'mssqlserver_job',
                'task',
                'om_textlog_job',
                'servlet_job',
                'zos_job',
                'ftp_job',
                'sftp_job'
                }
    time_keys = ["AppName", "JobName",
                 "Submitat", "Delaysubmit",
                 "DUEMIN_TIME", "DUEMAX_TIME",
                 "Startby", "Completedby",
                 "abandon_submission", "abandon_predecessors",
                 "abandon_resources", "abandon_variable_dependencies"]
    time_value_found = False
    xmlfilepath = input("Enter the file path: ")
    outpath = input("Enter the outfile path: ")
    outfile = input("Enter the outfile name: ")
    csv_out_file = os.path.join(outpath, outfile)

    xml_data_to_csv = open(csv_out_file, 'w', newline='', encoding='utf-8')
    csv_writer = csv.DictWriter(xml_data_to_csv, fieldnames=time_keys)
    xmltime_dict = dict()
    csv_writer.writeheader()
    os.chdir(xmlfilepath)
    files = os.listdir(xmlfilepath)
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        for job in root.findall('*'):
            tag = job.tag.partition('}')[2]
            if tag in job_type:
                xmltime_dict = dict()
                time_value_found = False
                for Submitat in job.findall('app:states/app:exec/app:absolute_in_delay', ns):
                    if Submitat.text is not None:
                        time_value_found = True
                        xmltime_dict["Submitat"] = Submitat.text
                for Delaysubmit in job.findall('app:states/app:exec/app:relative_in_delay', ns):
                    if Delaysubmit.text is not None:
                        time_value_found = True
                        xmltime_dict["Delaysubmit"] = Delaysubmit.text
                for Completedby in job.findall('app:states/app:exec/app:dueout', ns):
                    if Completedby.text is not None:
                        time_value_found = True
                        xmltime_dict["Completedby"] = Completedby.text
                for Startby in job.findall('app:states/app:ready/app:dueout', ns):
                    if Startby.text is not None:
                        time_value_found = True
                        xmltime_dict["Startby"] = Startby.text
                for DUEMIN_TIME in job.findall('app:max_min/app:min_time', ns):
                    if DUEMIN_TIME.text is not None:
                        time_value_found = True
                        xmltime_dict["DUEMIN_TIME"] = DUEMIN_TIME.text
                for DUEMAX_TIME in job.findall('app:max_min/app:max_time', ns):
                    if DUEMAX_TIME.text is not None:
                        time_value_found = True
                        xmltime_dict["DUEMAX_TIME"] = DUEMAX_TIME.text
                for timeaction in job.findall('app:time_actions/*', ns):
                    for schedule in timeaction.findall('*'):
                        if schedule.text is not None:
                            time_value_found = True
                            xmltime_dict[timeaction.tag.partition(
                                '}')[2]] = schedule.text
                if job.attrib.get('qualifier') is not None:
                    jobname = job.attrib.get(
                        'name') + '.' + job.attrib.get('qualifier')
                else:
                    jobname = job.attrib.get('name')
                xmltime_dict["JobName"] = jobname
                xmltime_dict["AppName"] = root.attrib.get('name')

                if time_value_found:
                    try:
                        csv_writer.writerow(xmltime_dict)
                    except Exception:
                        print('Failed to write :', file)
    xml_data_to_csv.close()


if __name__ == '__main__':
    main()
