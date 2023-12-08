from decouple import config
import os
import requests
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ACCESS_TOKEN = config('ACCESS_TOKEN')
BASE_URL = config('BASE_URL')

def get_thread_count():
    default_multiplier = 4  # Default multiplier for I/O-bound tasks
    cpu_cores = os.cpu_count() or 1  # Fallback to 1 if os.cpu_count() returns None
    thread_workers = cpu_cores * default_multiplier
    return thread_workers

headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}

# Function to download a file
def download_file(file_info):
    f_path, url = file_info
    if not os.path.exists(f_path):
        urllib.request.urlretrieve(url, f_path)
        print(f"Downloaded {f_path}")

root_directory = os.getcwd()
files_directory = os.path.join(root_directory, 'files')

courses_directory = os.path.join(files_directory, 'courses')
if not os.path.exists(courses_directory):
    os.makedirs(courses_directory)

print('\n\n\n')

courses = []

# get courses
next_url = BASE_URL + '/api/v1/courses'
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

print('\n\n\n')

# Function to process files for a course or group
def process_files(files, directory):
    with ThreadPoolExecutor(max_workers=get_thread_count()) as executor:  # Adjust the number of workers as needed
        for f in files:
            print(f['display_name'], f['url'], f['id'])
            f_path = os.path.join(directory, f['display_name'])
            executor.submit(download_file, (f_path, f['url']))

# download files for a course
for course in courses:
    next_url = BASE_URL + '/api/v1/courses/{}/files'.format(course['id'])
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
        process_files(files, course_directory)

groups_directory = os.path.join(files_directory, 'groups')
if not os.path.exists(groups_directory):
    os.makedirs(groups_directory)

print('\n\n\n')

groups = []

# get groups
next_url = BASE_URL + '/api/v1/users/self/groups'
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
    next_url = BASE_URL + '/api/v1/groups/{}/files'.format(group['id'])
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
        process_files(files, group_directory)

        group_users = []
        next_group_users_url = BASE_URL + '/api/v1/groups/{}/users'.format(group['id'])
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
            with open(group_users_file_path, 'w') as group_users_file:
                for group_user in group_users:
                    group_users_file.write('{} {}\n'.format(group_user['name'],  group_user['id']))

submissions_directory = os.path.join(files_directory, 'submissions')
if not os.path.exists(submissions_directory):
    os.makedirs(submissions_directory)

print('\n\n\n')

submissions = []

# get course submissions
next_url = BASE_URL + '/api/v1/users/self/folders'
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
    next_url = BASE_URL + '/api/v1/folders/{}/files'.format(submission['id'])
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
        process_files(files, submission_directory)
