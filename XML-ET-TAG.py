import xml.etree.ElementTree as ET
import os

# fileline = 'JOBNAME,AGENT,SUBAPPLICATION,'
# #outfile = open('out.txt', 'w')
# path = input("Enter the path of your file: ")
path = "C:\\Users\\mu6g8mn\\Documents\\1SCEDULING\\Extract"
os.chdir(path)
# appnm = input("Enter XML name: ")
appnm = 'SAMPLE.xml'
ns = {'app': 'http://dto.wa.ca.com/application'}
tree = ET.parse(appnm)
my_root = tree.getroot()
print("Root Element : ", my_root.tag)
# tag of first child of the root element
print("First Child Of Root Element : ", my_root[0].tag)

# print all the tags
print("\nAll Tags : ")
for a in my_root[4]:
    print(a.tag)
for applopts in my_root.findall('app:applopts', ns):
    print(applopts.tag)
