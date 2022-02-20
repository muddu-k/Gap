import csv
import os
import xml.etree.ElementTree as ET


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
    xmlfilepath = input("Enter the file path: ")
    outpath = input("Enter the outfile path: ")
    outfile = input("Enter the outfile name: ")
    # csv_out_file = outpath + '\\' + outfile
    csv_out_file = os.path.join(outpath, outfile)

    xml_data_to_csv = open(csv_out_file, 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(xml_data_to_csv)
    header = ["Aplication Name", "Job Name", "Job Type", "LoadScript", "RunScript"]
    csv_writer.writerow(header)
    os.chdir(xmlfilepath)
    files = os.listdir(xmlfilepath)
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        for job in root.findall('*'):
            tag = job.tag.partition('}')[2]
            if tag in job_type:
                xml_data = []
                loadscript = None
                runscript = None
                jobname = None
                for load_script in job.findall('app:on_load/app:script_definition', ns):
                    loadscript = load_script.text
                # for run_script in job.findall('.//*/app:on_enter/app:script_definition', ns):
                for run_script in job.findall('app:states/app:ready/app:on_enter/app:script_definition', ns):
                    runscript = run_script.text
                # if (loadscript is not None or runscript is not None):
                if any([loadscript, runscript]):
                    xml_data.append(root.attrib.get('name'))
                    if job.attrib.get('qualifier') is not None:
                        jobname = job.attrib.get('name') + '.' + job.attrib.get('qualifier')
                    else:
                        jobname = job.attrib.get('name')
                    xml_data.append(jobname)
                    xml_data.append(tag)
                    xml_data.append(loadscript)
                    xml_data.append(runscript)
                    try:
                        csv_writer.writerow(xml_data)
                    except Exception:
                        print('Failed to write :', file)
    xml_data_to_csv.close()


if __name__ == '__main__':
    main()
