
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

    tipo_sesion = tree.find('.//tipo_sesion').text
    organo = tree.find('.//organo').text
    presidente = tree.find('.//presidente').text
    dia = tree.find('.//dia').text
    mes = tree.find('.//mes').text
    anio = tree.find('.//anio').text
    tipo_epigrafe = tree.find('.//tipo_epigrafe').text

    print(tipo_epigrafe)
    exit()
    # text = .find('.//parrafo/text()')
    # print(text)