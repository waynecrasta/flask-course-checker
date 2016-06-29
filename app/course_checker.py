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


def return_numbers(department):
    url = 'http://courses.illinois.edu/cisapp/explorer/schedule/2016/fall/{}.xml'.format(department)
    r = requests.get(url)

    root = ET.fromstring(r.text)

    rv = []

    courses = root[12]

    for course in courses:
        numname = course.attrib['id']
        rv.append((numname, numname))

    return rv


def return_crn(department, number):
    url = 'http://courses.illinois.edu/cisapp/explorer/schedule/2016/fall/{}/{}.xml'.format(department, number)
    r = requests.get(url)

    root = ET.fromstring(r.text)

    rv = []

    courses = root[5]

    for course in courses:
        numname = course.attrib['id']
        rv.append(numname)

    return rv
