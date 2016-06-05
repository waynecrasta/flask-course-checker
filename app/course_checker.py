import requests
import xml.etree.ElementTree as ET


def check_open(department, number, crn):
    url = 'http://courses.illinois.edu/cisapp/explorer/schedule/2016/fall/{}/{}/{}.xml'.format(department, number, crn)
    r = requests.get(url)
    xml = r.text

    # For testing with localXML #
    # with open('test.xml', 'r') as xml:
    #     xml = xml.read()

    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return "not found"
    avail = root.find('enrollmentStatus').text
    if avail == "Closed" or avail == "UNKNOWN":
        return "closed"
    else:
        return 'open'
