from bs4 import BeautifulSoup
import requests
import json

TERM = 'fall'
YEAR = '2017'

base_url = 'https://courses.illinois.edu/cisapp/explorer/schedule/{}/{}'.format(YEAR, TERM)


def return_subjects():
    url = '{}.xml'.format(base_url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    subject_tags = soup.subjects.findAll()
    subjects = [subject.attrs['id'] for subject in subject_tags]
    return subjects


def get_courses_for_subject(subject):
    url = '{}/{}.xml'.format(base_url, subject)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    course_tags = soup.courses.findAll()
    courses = [course.attrs['id'] for course in course_tags]
    return courses


def get_sections_for_course(subject, course):
    url = '{}/{}/{}.xml'.format(base_url, subject, course)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    section_tags = soup.sections.findAll()
    sections = [int(section.attrs['id']) for section in section_tags]
    return sections


def create_json_blob():
    myD = dict()
    subjects = return_subjects()
    for idx, subject in enumerate(subjects):
        myD[subject] = {}
        for course in get_courses_for_subject(subject):
            myD[subject][course] = []
            for section in get_sections_for_course(subject, course):
                myD[subject][course].append(section)
        print "{}%: Finished {}".format(int(float(idx + 1) / float(len(subjects)) * 100), subject)

    data = json.dumps(myD)

    return data


if __name__ == '__main__':
    f = open('app/static/js/data.json', 'w')
    f.write(create_json_blob())
    f.close()
