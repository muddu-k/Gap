import xmltodict
import pprint 
pp = pprint.PrettyPrinter(indent=4)
with open('C:\\Users\\mu6g8mn\\Documents\\1SCEDULING\\Extract\\SAMPLE.xml') as fd:
    doc = xmltodict.parse(fd.read())
    # print(doc)
    pp.pprint(doc)