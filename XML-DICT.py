import xmltodict
import pprint 
pp = pprint.PrettyPrinter(indent=4)
with open('SAMPLE.xml') as fd:
    doc = xmltodict.parse(fd.read())
    # print(doc)
    pp.pprint(doc)
    