# JIRO Sandbox

import requests
import certifi
import json
import os
from datetime import datetime


def fetch_jira_issues(url, auth, start_at=0, max_results=50):
    paginated_url = f"{url}&startAt={start_at}&maxResults={max_results}"
    response = requests.get(paginated_url, auth=auth, verify=False)
    print(f"Response lenth: {len(response.text)}")
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        response.raise_for_status()
        exit

def find_names(issue, path='', issue_key=None, name_dict=None, ignore_names=None):
    '''This recursive method traverses the JIRA Issue JSON content looking for the attribute 'name' and stores it in the dictionary along with the 'path' to that name'''
    if name_dict is None:
        name_dict = {}

    # Update the issue key if we're at the root of an issue
    if path == '' and 'key' in issue:
        issue_key = issue['key']

    if isinstance(issue, dict):
        for key, value in issue.items():
            new_path = f"{path}/{key}" if path else key
            if key == 'name' and '@' in value and not new_path.startswith("fields/customfield"):
                if value not in name_dict:
                    name_dict[value] = []
                name_dict[value].append({'issue_key': issue_key, 'path': new_path})
            find_names(value, new_path, issue_key, name_dict, ignore_names)

    elif isinstance(issue, list):
        for i, item in enumerate(issue):
            find_names(item, f"{path}[{i}]", issue_key, name_dict, ignore_names)

    return name_dict
            
def process_issues(issues_json):
    '''Traverse provided JSON based compound collection of JIRA issues and collect the names with some details about each name'''
    # Ensure that 'issues_json' is a dictionary containing an 'issues' key
    if 'issues' not in issues_json:
        raise ValueError("Invalid input: JSON does not contain 'issues' key")
    
    names_dict = {}
    # traverse issues and collect the names with some details about each name
    for issue in issues_json['issues']:
        names_dict.update(find_names(issue))

    #region Iterate over all the collected names, printing the details about each name
    for name, details in names_dict.items():
        print(f"\nName: {name}")
        for detail in details:
            print(f"  Issue Key: {detail['issue_key']}")
            print(f"  Path: {detail['path']}")
    #endregion

    # Iterate over the issues
    for issue in issues_json['issues']:
        # Check if the issue has a 'changelog' and 'histories'
        if 'changelog' in issue and 'histories' in issue['changelog']:
            histories = issue['changelog']['histories']
            # Print the number of histories
            #print(f'Number of histories: {len(histories)}')
        else:
            print(f"No changelog or histories available for the issue {issue}.")

    return names_dict

def save_to_file(data, filename):
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time into a string (e.g., "20231228_153045" for Dec 28, 2023, 15:30:45)
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

    # Use the formatted date-time in the filename
    filename_with_timestamp = f'{filename}_{formatted_datetime}.json'

    # Save the combined results to the file
    with open(filename_with_timestamp, 'w') as file:    
        json.dump(data, file)

def analyze_contributors(contributors, my_team):
    team_contributions = {member: {} for member in my_team}

    for name, details in contributors.items():
        if name in my_team:
            for detail in details:
                path_parts = detail['path'].split('/')
                role = path_parts[-2] if len(path_parts) > 1 else 'unknown'
                team_contributions[name][role] = team_contributions[name].get(role, 0) + 1

    # Highlighting team members with no roles played
    for member in my_team:
        if not team_contributions[member]:
            team_contributions[member]['No roles played'] = 'Not applicable'

    return team_contributions

def main():

    # https://jira.ceteracorp.com/rest/api/2/search?jql=Sprint='Sprint 153'
    sprint = "Sprint 153"
    jira_url = f"https://jira.ceteracorp.com/rest/api/2/search?jql=Sprint='{sprint}'&expand=changelog"
    #jira_url = "https://jira.ceteracorp.com/rest/api/2/search"
    auth = (
'..........', '..............'        ) 
    
    desired_data = 'Issues_20231229_040031.json'  # Replace with your desired file name

    if os.path.exists(desired_data):
        with open(desired_data, 'r') as file:
            all_issues = json.load(file)
    else:
        all_issues = []
        start_at = 0
        max_results = 50
        total_issues = None

        while total_issues is None or start_at < total_issues:

            try:
                response = fetch_jira_issues(jira_url, auth, start_at, max_results)
                all_issues.extend(response['issues'])
                start_at += len(response['issues'])
                total_issues = response['total']
            except Exception as e:
                print(f"An error occurred: {e}")
                exit
        save_to_file(all_issues, 'Issues')

    contributors = process_issues({'issues': all_issues})
    print(f"The total contributors: {len(contributors)}")
    
    my_team = {
        "slava.lu@dumb.com", 
        "Natalia.Zaricinii@cetera.com",
        "Cody.Watson@cetera.com",
        "Ilia.Cibotari@cetera.com",
        "Siva.Krishna@cetera.com",
        }  # Add more team members as needed

    team_report = analyze_contributors(contributors, my_team)

    # Print the report
    for member, roles in sorted(team_report.items()):
        print(f"\nMember: {member}")
        for role, count in roles.items():
            print(f"  {role.title()}: {count} times")

    # # Creating the set of names from contributors
    # my_team = {name for name in contributors.keys()}

    # # Printing the names in the desired format
    # print("my_team = {")
    # for name in my_team:
    #     print(f"    \"{name}\",")
    # print("}")

if __name__ == "__main__":
    main()
