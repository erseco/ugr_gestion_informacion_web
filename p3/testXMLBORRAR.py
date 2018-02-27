
import sys
import glob

from xml.etree import ElementTree as ET


documentsDirectoryName="iniciativas08"


for filename in glob.iglob(documentsDirectoryName+'/*.xml'):

    print('/foobar/%s' % filename)

    tree = ET.parse(filename)
    root = tree.getroot()
    elements = tree.findall('.//parrafo')
    result = ""
    for text in elements:
        result = result + text.text + " "

    print(result)
    exit()
    # text = .find('.//parrafo/text()')
    # print(text)