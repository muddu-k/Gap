import xml.etree.ElementTree as ET
import csv
import os
ns = {'app': 'http://dto.wa.ca.com/application'}
xmlfilepath = input("Enter the file path: ")
outpath = input("Enter the outfile path: ")
outfile = input("Enter the outfile name: ")
csv_out_file = outpath + '\\' + outfile
xml_data_to_csv = open(csv_out_file, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(xml_data_to_csv)
header = ["Aplication Name", "Script Name", "Script"]
csv_writer.writerow(header)
os.chdir(xmlfilepath)
files = os.listdir(xmlfilepath)
for file in files:
    tree = ET.parse(file)
    root = tree.getroot()
    for script in root.findall('./app:script_lib/app:script_definition', ns):
        if script.text is not None:
            xml_data = []
            xml_data.append(root.attrib.get('name'))
            xml_data.append(script.attrib.get('name'))
            xml_data.append(script.text)
            try:
                csv_writer.writerow(xml_data)
            except Exception:
                print('Failed to write :', file)
xml_data_to_csv.close()
