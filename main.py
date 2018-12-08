from decouple import config
import os
import requests
import urllib.request

ACCESS_TOKEN = config('ACCESS_TOKEN')

FOLDERS_API_URL = 'https://psu.instructure.com/api/v1/users/self/folders'

headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}

# https://psu.instructure.com/files

# TODO also download my submissions for all courses
# get folders for courses i've submitted files to
# folders = requests.get(FOLDERS_API_URL, headers=headers).json()
# for folder in folders:
#     print(folder['name'], folder['id'])

root_directory = os.getcwd()
files_directory = os.path.join(root_directory, 'files')

courses_directory = os.path.join(files_directory, 'courses')
if not os.path.exists(courses_directory):
    os.makedirs(courses_directory)

print('\n\n\n')

courses = []

# get courses
next_url = 'https://psu.instructure.com/api/v1/courses'
while next_url:
    response = requests.get(next_url, headers=headers)
    if not 'Link' in response.headers:
        break
    links = requests.utils.parse_header_links(response.headers['Link'].rstrip('>').replace('>,<', ',<'))
    next_url = None
    for link in links:
        if link['rel'] == 'next':
            next_url = link['url']
            break
    current_courses = response.json()
    for current_course in current_courses:
        courses.append(current_course)
        print(current_course['name'], current_course['id'])

print('\n\n\n')

# download files for a course
for course in courses:
    next_url = 'https://psu.instructure.com/api/v1/courses/{}/files'.format(course['id'])
    while next_url:
        response = requests.get(next_url, headers=headers)
        if not 'Link' in response.headers:
            break
        links = requests.utils.parse_header_links(response.headers['Link'].rstrip('>').replace('>,<', ',<'))
        next_url = None
        for link in links:
            if link['rel'] == 'next':
                next_url = link['url']
                break
        files = response.json()
        course_directory = os.path.join(courses_directory, course['name'])
        if not os.path.exists(course_directory):
            os.makedirs(course_directory)
        for f in files:
            print(f['display_name'], f['url'], f['id'])
            f_path = os.path.join(course_directory, f['display_name'])
            if not os.path.exists(f_path):
                urllib.request.urlretrieve(f['url'], f_path)

# TODO download group members for each group

groups_directory = os.path.join(files_directory, 'groups')
if not os.path.exists(groups_directory):
    os.makedirs(groups_directory)

print('\n\n\n')

groups = []

# get groups
next_url = 'https://psu.instructure.com/api/v1/users/self/groups'
while next_url:
    response = requests.get(next_url, headers=headers)
    if not 'Link' in response.headers:
        break
    links = requests.utils.parse_header_links(response.headers['Link'].rstrip('>').replace('>,<', ',<'))
    next_url = None
    for link in links:
        if link['rel'] == 'next':
            next_url = link['url']
            break
    current_groups = response.json()
    for current_group in current_groups:
        groups.append(current_group)
        print(current_group['name'], current_group['id'])

print('\n\n\n')

# download files for a group
for group in groups:
    next_url = 'https://psu.instructure.com/api/v1/groups/{}/files'.format(group['id'])
    while next_url:
        response = requests.get(next_url, headers=headers)
        if not 'Link' in response.headers:
            break
        links = requests.utils.parse_header_links(response.headers['Link'].rstrip('>').replace('>,<', ',<'))
        next_url = None
        for link in links:
            if link['rel'] == 'next':
                next_url = link['url']
                break
        files = response.json()
        group_directory = os.path.join(groups_directory, '{} {}'.format(group['name'], group['id']))
        if not os.path.exists(group_directory):
            os.makedirs(group_directory)
        for f in files:
            print(f['display_name'], f['url'], f['id'])
            f_path = os.path.join(group_directory, f['display_name'])
            if not os.path.exists(f_path):
                urllib.request.urlretrieve(f['url'], f_path)
