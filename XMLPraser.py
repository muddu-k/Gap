import xml.etree.ElementTree as ET

class xmlparser():
    def __init__(self,filename) -> None:
        self.filename = filename
    
    def appparser(self):
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
        tree = ET.parse(self.filename)
        root = tree.getroot()
        for job in root.findall('*'):
            tag = job.tag.partition('}')[2]
            if tag in job_type:
                if job.attrib.get('qualifier') is not None:
                    jobname = job.attrib.get(
                        'name') + '.' + job.attrib.get('qualifier')
                else:
                    jobname = job.attrib.get('name')
                job_dict = dict()
                job_dict(type)=tag
                job_dict()
                
        
    