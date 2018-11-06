import json
import random
from lxml import etree as ET
import datagen_module as DGM

numTypes = DGM.getTypeSize()
colIndex = 0
samplesDict = {}
nodes = []
namespaces = {}
uris = []

class Node:
    """A node in the example data to assign a value to"""

    def __init__(self, n, t, r):
        global samplesDict
        self.name = n
        self.type = t
        self.root = r
        if n == "nested":
            self.text = None
            return
        if t not in samplesDict:
            templist = []
            for i in range(40):
                templist.append(str(DGM.runGenFunction(t)))
            samplesDict[t] = templist

    def tostring(self):
        return self.name + " " + str(self.text)

def initNSMap():
    SQLCORE_NS = "http://www.marklogic.com/tde/els/sqlcore"
    uris.append("{%s}" % SQLCORE_NS)
    namespaces.update({"sqlcore" : SQLCORE_NS})
    ELS_NS = "http://www.marklogic.com/tde/els"
    uris.append("{%s}" % ELS_NS)
    namespaces.update({"els" : ELS_NS})
    TDE_NS = "http://www.marklogic.com/tde"
    uris.append("{%s}" % TDE_NS)
    namespaces.update({"tde" : TDE_NS})

def createRandomDataElement(root):
    global colIndex
    temp = random.randint(0, numTypes - 1)
    colName = "t" + str(tableNum) + "_col" + str(colIndex) + "_" + DGM.getType(temp)
    child = ET.SubElement(root, uris[random.randint(0, len(uris)-1)] + colName, \
              type=str(DGM.getType(temp)), id=str(colIndex))
    nodes.append(Node(colName, temp, child))
    colIndex = colIndex + 1
    return child

def createSubElements(root):
    child = ET.SubElement(root, uris[random.randint(0, len(uris)-1)] + "nested")
    nodes.append(Node("nested", None, child))
    while random.randint(0, 100) > 15:
        newchild = createRandomDataElement(child)
    while random.randint(0, 100) > 50:
        newnested = createSubElements(child)
    return root

def assignData():
    for node in nodes:
        if node.type == None:
            continue
        node.root.text = str(samplesDict[node.type][random.randint(0, len(samplesDict[node.type])) - 1])
        if random.randint(0, 100) > 90:
            node.root.set("top-secret", "yes")
        else:
            node.root.set("top-secret", "no")

def genXMLTemplate():
    template = ET.Element("template", xmlns="http://marklogic.com/xdmp/tde")
    ET.SubElement(template, "context").text = "/root" + str(tableNum)
    rows = ET.SubElement(template, "rows")
    row = ET.SubElement(rows, "row")
    ET.SubElement(row, "schema-name").text = "main"
    ET.SubElement(row, "view-name").text = "view" + str(tableNum)
    columns = ET.SubElement(row, "columns")
    for node in nodes:
        if random.randint(0, 100) > 25 and node.type is not None:
            column = ET.SubElement(columns, "column")
            ET.SubElement(column, "name").text = node.name
            ET.SubElement(column, "scalar-type").text = DGM.getType(node.type)
            ET.SubElement(column, "val").text = "//*:" + node.name + "/text()"
            ET.SubElement(column, "nullable").text = "true"
            ET.SubElement(column, "invalid-values").text = "reject"
    tree = ET.ElementTree(template)
    indent(template)
    tree.write("templates/table" + str(tableNum) + "-tde.xml", xml_declaration=False, encoding='utf-8', method='xml')

'''
copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
it basically walks your tree and adds spaces and newlines so the tree is
printed in a nice way
'''
def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def XMLgen(numDocs):
    initNSMap()
    baseDoc = ET.Element("root" + str(tableNum), nsmap=namespaces)
    while random.randint(0, 100) > 10:
        createSubElements(baseDoc)
    tree = ET.ElementTree(baseDoc)
    indent(baseDoc)
    for i in range(numDocs):
        assignData()
        tree.write("table" + str(tableNum) + "/table" + str(tableNum) + "doc" + str(i) + ".xml", xml_declaration=True, encoding='utf-8', method="xml")

def createRandomDataDict():
    global colIndex
    temp = random.randint(0, numTypes - 1)
    colName = "t" + str(tableNum) + "_col" + str(colIndex) + "_" + DGM.getType(temp)
    child = {colName: DGM.runGenFunction(temp)}
    # nodes.append(Node(colName, temp, child))
    colIndex = colIndex + 1
    return child

def createSubDict():
    nested = {}
    while random.randint(0, 100) > 15:
        newchild = createRandomDataDict()
        nested.update(newchild)
    while random.randint(0, 100) > 50:
        newnested = createSubDict()
        nested.update(newnested)
    return nested

def JSONgen():
    data = {"root" + str(tableNum): createSubDict()}
    with open('tableJS' + str(tableNum) + "/table" + str(tableNum) + ".json", "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

# tableNum = x will generate docs into tablex/ directory
# Make sure tablex dir is created
# A TDE template will be generated and sent to templates/tablex-tde.xml

tableNum = 1
JSONgen()