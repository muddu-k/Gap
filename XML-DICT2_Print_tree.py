import xmltodict
import json
with open('C:\\Users\\mu6g8mn\\Documents\\1SCEDULING\\Extract\\SAMPLE.xml') as fd:
    doc = xmltodict.parse(fd.read())
    tree_str = json.dumps(doc, indent=4)
    tree_str = tree_str.replace("\n    ", "\n")
    tree_str = tree_str.replace('"', "")
    tree_str = tree_str.replace(',', "")
    tree_str = tree_str.replace("{", "")
    tree_str = tree_str.replace("}", "")
    tree_str = tree_str.replace("    ", " | ")
    tree_str = tree_str.replace("  ", " ")

    print(tree_str)



