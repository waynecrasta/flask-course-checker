import requests
import xml.etree.ElementTree as ET


def check_open(department, number, crn):
    url = 'http://courses.illinois.edu/cisapp/explorer/schedule/2017/fall/{}/{}/{}.xml'.format(department, number, crn)
    r = requests.get(url)
    xml = r.text
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return "not found"
    try:
        avail = root.find('enrollmentStatus').text
    except:
        return "unknown"
    if avail == "Closed" or avail == "UNKNOWN":
        return "closed"
    else:
        return 'open'


def return_subjects():
    url = 'http://courses.illinois.edu/cisapp/explorer/schedule/2016/fall.xml'
    r = requests.get(url)

    root = ET.fromstring(r.text)

    subjects = []

    for subject in root[2]:
        sname = subject.attrib['id']
        subjects.append(sname)

    return subjects
