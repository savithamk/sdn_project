from datetime import datetime

import requests
import json
import os

# Git repository information
repo_path = '/home/student/Downloads/sdn'
repo_name = 'sdn_project'
repo_url = 'https://github.com/savithamk/sdn_project.git'


# REST API endpoint for opendaylight
headers = {'Content-Type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4='}
url = 'http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/'

# Make the REST API request
response = requests.get(url, headers=headers)
print("Response code: ", response.status_code)

# Check if the request was successful
if response.status_code == 200:

    # Parse the response JSON
    topology_data = response.json()

    # Change to the Git repository directory
    if not os.path.exists(repo_path + '/' + repo_name):
        os.chdir(repo_path)
        os.system(f'git clone {repo_url}')
    os.chdir(repo_path + '/' + repo_name)
    
    
    fileName = 'sdn_info_' + datetime.now().strftime("%d-%m-%Y%H:%M:%S") + '.json'

    # Save the topology data to a file
    with open(fileName, 'w') as f:
        json.dump(topology_data, f)

    # Add the topology data file to the Git repository
    os.system('git add --all')

    # Commit the topology data file to the Git repository
    os.system('git commit -m "Captured opendaylight inventory"')

    # Push the changes to the Git repository
    os.system(f'git push {repo_url} main')
else:
    print(f'Error: Could not retrieve opendaylight inventory data (status code {response.status_code})')
