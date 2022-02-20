import xml.etree.ElementTree as ET
import os


def eventtime():
    ns = {'e' : 'http://dto.wa.ca.com/event'}
    xmlfilepath = input("Enter the file path: ")
    outpath = input("Enter the outfile path: ")
    outfile = input("Enter the outfile name: ")
    files = os.listdir(xmlfilepath)
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        for name in root.findall('e:eventsch/e:description/e:name',ns):
            schedname =name.text
        sch=[]
        for scheduleelement in root.findall('e:eventsch/e:schedule/e:scheduleelement',ns):
            sch.append(scheduleelement.attrib.get('original'))
        if len(sch) > 0:
            print(schedname,sch)



def main():
    eventtime()


if __name__ == '__main__':
    main()
