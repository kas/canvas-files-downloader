from decouple import config
import os
import requests
import urllib.request

ACCESS_TOKEN = config('ACCESS_TOKEN')

headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}

# TODO make psu.instructure.com changeable
# TODO refactor code

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
        group_directory = os.path.join(groups_directory, '{} {}'.format(group['name'].replace('/', '-'), group['id']))
        if not os.path.exists(group_directory):
            os.makedirs(group_directory)
        for f in files:
            print(f['display_name'], f['url'], f['id'])
            f_path = os.path.join(group_directory, f['display_name'])
            if not os.path.exists(f_path):
                urllib.request.urlretrieve(f['url'], f_path)
        group_users = []
        next_group_users_url = 'https://psu.instructure.com/api/v1/groups/{}/users'.format(group['id'])
        while next_group_users_url:
            response = requests.get(next_group_users_url, headers=headers)
            if not 'Link' in response.headers:
                break
            links = requests.utils.parse_header_links(response.headers['Link'].rstrip('>').replace('>,<', ',<'))
            next_group_users_url = None
            for link in links:
                if link['rel'] == 'next':
                    next_group_users_url = link['url']
                    break
            current_group_users = response.json()
            for current_group_user in current_group_users:
                group_users.append(current_group_user)
        group_users_file_path = os.path.join(group_directory, '{} {} users.txt'.format(group['name'].replace('/', '-'), group['id']))
        if not os.path.exists(group_users_file_path):
            group_users_file = open(group_users_file_path, 'w')
            for group_user in group_users:
                group_users_file.write('{} {}\n'.format(group_user['name'],  group_user['id']))
            group_users_file.close()

submissions_directory = os.path.join(files_directory, 'submissions')
if not os.path.exists(submissions_directory):
    os.makedirs(submissions_directory)

print('\n\n\n')

submissions = []

# get course submissions
next_url = 'https://psu.instructure.com/api/v1/users/self/folders'
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
    current_submissions = response.json()
    for current_submission in current_submissions:
        submissions.append(current_submission)
        print(current_submission['name'], current_submission['id'])

print('\n\n\n')

# download course submissions
for submission in submissions:
    next_url = 'https://psu.instructure.com/api/v1/folders/{}/files'.format(submission['id'])
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
        submission_directory = os.path.join(submissions_directory, submission['name'])
        if not os.path.exists(submission_directory):
            os.makedirs(submission_directory)
        for f in files:
            print(f['display_name'], f['url'], f['id'])
            f_path = os.path.join(submission_directory, f['display_name'])
            if not os.path.exists(f_path):
                urllib.request.urlretrieve(f['url'], f_path)
