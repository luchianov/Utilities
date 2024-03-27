''' ## Team contribution analysis via JIRA API.py

The script "Team contribution analysis via JIRA API.py" is a comprehensive utility designed to analyze team contributions in a JIRA project, particularly focusing on a specified sprint. The script operates by fetching issue data from JIRA and processing it to determine the activity levels and contributions of team members. Key features and usage instructions include:

1. **Data Fetching**: Connects to the JIRA API and retrieves all issues associated with a specified sprint. For efficiency and offline access, it also stores this data locally with a timestamp in the file name. This allows for re-analysis or additional reporting later without needing to re-fetch data from JIRA.

2. **Contributor Analysis**: The script inverts the issue data to create a list of contributors, mapping each team member to their activities and roles within the sprint. This includes roles like assignee, author, creator, and reporter.

3. **Story Points Allocation**: One of the critical aspects of the script is how it deals with story points:
   - It identifies whether a task is an 'issue' or a 'sub-task' based on the issue type in the JIRA data.
   - Story points are proportionally allocated to contributors based on their role in the issue. If an issue is assigned to multiple people during its lifecycle, the script calculates each person's share of the story points. This is done by dividing the total story points by the number of times the issue was assigned.
   - The proportional story points are then added to the contributors' total, offering a more nuanced view of each member's contribution.

4. **Output**: The script generates a CSV file that includes a detailed breakdown of each team member's contributions. The columns include:
   - **Name**: The contributor's name.
   - **Roles**: Separate columns for each role (assignee, author, creator, reporter) indicating the count of activities in each role.
   - **Total Story Points**: The cumulative story points associated with the contributor, calculated as per the proportional allocation method.
   - **Issues/Subtasks**: Specific issues and subtasks the contributor worked on, along with the allocated story points.

5. **Usage**: To use the script, you need to specify the sprint for which you want to analyze contributions. Run the script, and it will automatically fetch the data, process it, and output the CSV file for analysis.

6. **Auditing and Local Repository**: The locally stored data can serve as an audit trail and a repository for conducting further analyses without additional API calls.

7. **Flexibility**: The script is adaptable and can be modified to suit different sprint configurations or to focus on different aspects of team contributions.

This description captures the script's functionality and provides guidance on how to use it effectively for analyzing team contributions within a JIRA sprint.
'''

import requests
import certifi
import json
import os
import csv
from collections import Counter
from datetime import datetime

Sprint = "Sprint 123"
'''#### Sprint Identifier
This variable defines the specific Sprint for which the JIRA issues will be fetched.
Replace "Sprint 123" with the actual Sprint ID you are interested in.
'''

base_filename = 'Issues_20231229_040031'
'''#### Base Filename for Data Storage
This variable sets the base name for any files that will be created or read.
'Issues_20231229_040031' is an example filename; change it to reflect your desired filename,
ideally indicating the date and time of the data snapshot.
'''

JIRA_URL = f"https://jira.your_company_domain.com/rest/api/2/search?jql=Sprint='{Sprint}'&expand=changelog"
'''#### JIRA API URL
This URL is used to make API requests to JIRA. It includes a JQL (JIRA Query Language) query
that specifies which issues to retrieve - in this case, all issues associated with the specified Sprint.
The 'expand=changelog' parameter requests additional changelog data for each issue.
Replace 'your_company_domain.com' with your actual JIRA instance's domain.
''' 
AUTH_INFO = ('username', 'password')
'''#### Authentication Information
These are the credentials used for authenticating with the JIRA API.
Replace 'username' and 'password' with your actual JIRA credentials.
'''

MY_TEAM = frozenset({
    "member.one@your_company_domain.com",
    "member.two@your_company_domain.com",
    "member.three@your_company_domain.com",
    "member.four@your_company_domain.com",
    "member.five@your_company_domain.com",
})
'''#### Team Members Set
This set contains the email addresses of team members whose contributions are to be analyzed.
These email addresses should match those used in JIRA. Add or remove members as needed for your team analysis.
'''

issue_subtask_status = {}
'''### Dictionary to track whether a JIRA issue is a sub-task or not
Key: Issue Key (e.g., "ABC-123"), Value: Boolean indicating if it's a sub-task'''

# all_candidates = {}

def fetch_jira_issues(start_at=0, max_results=50):
    '''Fetches JIRA issues from the API with pagination. 
    Takes the start index and maximum results to fetch as parameters.'''

    paginated_url = f"{JIRA_URL}&startAt={start_at}&maxResults={max_results}"
    response = requests.get(paginated_url, auth=AUTH_INFO, verify=False)
    print(f"Response lenth: {len(response.text)}")
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        response.raise_for_status()
        exit

def find_names_with_issue_keys_and_story_points(json_fragment, path='', issue_key=None, name_dict=None, story_points=None):
    ''' Recursively finds names in the single JIRA issue JSON and stores them in a dictionary, along with the 'Issue Key', 'Story Points' and the 'path' to that name. '''
    global issue_subtask_status
    global all_candidates

    if name_dict is None:
        name_dict = {}

    # Update the issue key if we're at the root of an issue
    if path == '' and 'key' in json_fragment:
        issue_key = json_fragment['key']

    # Process histories for assignee changes
    if isinstance(json_fragment, dict):        
        if 'changelog' in json_fragment and 'histories' in json_fragment['changelog']:
            for history in json_fragment['changelog']['histories']:
                for item in history.get('items', []):
                    if item.get('field') == 'assignee':
                        prev_assignee = item.get('from')
                        if prev_assignee and '@' in prev_assignee and prev_assignee in MY_TEAM:
                            # Add previous assignee to the dictionary
                            if prev_assignee not in name_dict:
                                name_dict[prev_assignee] = []
                            name_dict[prev_assignee].append({'issue_key': issue_key, 'path': 'changelog/histories/assignee/name', 'story_points': story_points})
    
    if isinstance(json_fragment, dict):
        for key, value in json_fragment.items():
            new_path = f"{path}/{key}" if path else key
            if not new_path.startswith("fields/customfield") :
                if key == 'name':
                    # if value and '@' in value and not all_candidates.get(value):
                    #     all_candidates[value] = True
                    if path == 'fields/issuetype' and value == 'Sub-task':
                        issue_subtask_status[issue_key] = True
                    elif value and '@' in value and value in MY_TEAM :
                        if value not in name_dict:
                            name_dict[value] = []
                        name_dict[value].append({'issue_key': issue_key, "story_points":story_points, 'path': new_path})
                    
                find_names_with_issue_keys_and_story_points(value, new_path, issue_key, name_dict, story_points)

    elif isinstance(json_fragment, list):
        for i, item in enumerate(json_fragment):
            find_names_with_issue_keys_and_story_points(item, f"{path}[{i}]", issue_key, name_dict, story_points)

    return name_dict
            
def process_issues(issues_json: dict) -> dict[str, list[dict]]:
    '''Traverse provided JSON based compound collection of JIRA issues 
    and collect the names with some details about each name'''

    # Ensure that 'issues_json' is a dictionary containing an 'issues' key
    if 'issues' not in issues_json:
        raise ValueError("Invalid input: JSON does not contain 'issues' key")
    
    names_dict = {}
    # Traverse issues and collect the names
    for issue in issues_json['issues']:
        story_points = issue["fields"].get("customfield_10002", None)
        new_names = find_names_with_issue_keys_and_story_points(issue, story_points=story_points)

        # Merge new_names into names_dict
        for name, details in new_names.items():
            if name in names_dict:
                names_dict[name].extend(details)  # Append new details to existing list
            else:
                names_dict[name] = details  # Add new name and details

    #region Iterate over all the collected names, printing the details about each name
    # for name, details in names_dict.items():
    #     if name in MY_TEAM :
    #         print(f"\nName: {name}")
    #         for detail in details: print(detail)
    #endregion

    # Flag the issues without changelog or history
    for issue in issues_json['issues']:
        # Check if the issue has a 'changelog' and 'histories'
        if 'changelog' in issue and 'histories' in issue['changelog']:
            histories = issue['changelog']['histories']
            # Print the number of histories
            #print(f'Number of histories: {len(histories)}')
        else:
            print(f"No changelog or histories available for the issue {issue}.")

    return names_dict

def get_filename_with_timestamp(basename):
    '''Generates a filename with a timestamp. 
    Takes the base name of the file as a parameter and appends the current date and time to it.'''


    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time into a string (e.g., "20231228_153045" for Dec 28, 2023, 15:30:45)
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

    # Construct the filename with the base and the formatted date-time
    filename_with_timestamp = f'{basename}_{formatted_datetime}'

    return filename_with_timestamp

def save_to_file(data, filename):
    '''Saves the provided data into a JSON file. 
    The file name is determined by appending a timestamp to the given filename.'''

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time into a string (e.g., "20231228_153045" for Dec 28, 2023, 15:30:45)
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

    # Use the formatted date-time in the filename
    filename_with_timestamp = f'{filename}_{formatted_datetime}.json'

    # Save the combined results to the file
    with open(filename_with_timestamp, 'w') as file:    
        json.dump(data, file)

def write_to_csv(team_report, all_roles, base_filename, alternative_filename=None):
    # Determine the CSV file name
    json_filename = f"{base_filename}.json"
    csv_filename = f"{base_filename}.csv"

    if not os.path.exists(json_filename) and alternative_filename:
        json_filename = f"{alternative_filename}.json"
        csv_filename = f"{alternative_filename}.csv"

    # Arrange the roles columns, 'No roles played' before the last and 'Issues' as the last column
    sorted_roles = sorted(role for role in all_roles if role not in ['No roles played', 'Issues', 'Total Story Points', 'SubTasks'])
    if 'No roles played' in all_roles:
        sorted_roles.append('No roles played')
    if 'Total Story Points' in all_roles:
        sorted_roles.append('Total Story Points')
    if 'Issues' in all_roles:
        sorted_roles.append('Issues')
    if 'SubTasks' in all_roles:
        sorted_roles.append('SubTasks')

    # Write to CSV
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name'] + sorted_roles)
        for member, roles in sorted(team_report.items()):
            row = [member] + [roles.get(role, '') for role in sorted_roles]
            writer.writerow(row)

def analyze_contributors(contributors: dict):
    '''Analyzes contributors based on team membership.'''
    global issue_subtask_status

    team_contributions = {member: {'Total Story Points': 0, 'SubTasks': '', 'Issues': ''} for member in MY_TEAM}
    role_count = {member: 0 for member in MY_TEAM}

    # Count the usage of each issue in the assignee role
    issue_usage_count = {}
    for details in contributors.values():
        for detail in details:
            if 'assignee' in detail['path']:
                issue_key = detail['issue_key']
                issue_usage_count[issue_key] = issue_usage_count.get(issue_key, 0) + 1

    for name, details in contributors.items():
        for detail in details:
            issue_key = detail['issue_key']
            path_parts = detail['path'].split('/')
            role = path_parts[-2] if len(path_parts) > 1 else 'unknown'
            team_contributions[name].setdefault(role, 0)
            team_contributions[name][role] += 1
            role_count[name] += 1  # Increment role count for the member
            if role == 'assignee':
                key_type = 'SubTasks' if issue_subtask_status.get(issue_key) else 'Issues'
                if detail["story_points"] is not None:
                    issue_count = issue_usage_count[issue_key]
                    proportional_points = round(detail['story_points'] / issue_count, 2)
                    if issue_count == 1:
                        team_contributions[name][key_type] += f"{issue_key} ({int(detail['story_points'])})  "
                    else:
                        team_contributions[name][key_type] += f"{issue_key} ({detail['story_points']}/{issue_count}={proportional_points})  "
                    team_contributions[name]['Total Story Points'] += proportional_points
                else: team_contributions[name][key_type] += f"{issue_key} (None)  "

    # Highlighting team members with no roles played
    for member in MY_TEAM:
        if role_count[member] == 0:
            team_contributions[member]['No roles played'] = 1

    return team_contributions

def get_desired_data(base_filename, alternative_filename):
    '''Gets required data from either the local file or from JIRA API'''

    base_file_with_ext = f"{base_filename}.json"
    alternative_file_with_ext = f"{alternative_filename}.json"

    # Check if the base file exists
    if os.path.exists(base_file_with_ext):
        with open(base_file_with_ext, 'r') as file:
            data = json.load(file)
    else:
        # Fetch data from the API and save it to the alternative file
        data = []
        start_at = 0
        max_results = 50
        total_issues = None

        while total_issues is None or start_at < total_issues:
            try:
                response = fetch_jira_issues(start_at, max_results)
                data.extend(response['issues'])
                start_at += len(response['issues'])
                total_issues = response['total']
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        # Save the fetched data to the alternative file
        with open(alternative_file_with_ext, 'w') as file:
            json.dump(data, file)

    return data

def main():
    '''Main function of the script. 
    Handles the overall process flow including data fetching, processing, and report generation.'''

    alternative_filename = get_filename_with_timestamp('Issues')  # Add a timestamp to the filename

    all_issues = get_desired_data(base_filename, alternative_filename)

    contributors = process_issues({'issues': all_issues})
    team_report = analyze_contributors(contributors)
    print(f"My team contributors number: {len(contributors)}")

    # Determine all possible roles for the header
    all_roles = set().union(*(d.keys() for d in team_report.values()))

    # Call to write data to CSV
    write_to_csv(team_report, all_roles, base_filename, alternative_filename)

    # Print the report
    # for member, roles in sorted(team_report.items()):
    #     print(f"\nMember: {member}")
    #     for role, count in roles.items():
    #         print(f"  {role.title()}: {count} times")

    # Printing the names in the desired format
    # print("team_candidates = {")
    # for name in sorted({name for name in all_candidates.keys()}):
    #     print(f"    \"{name}\",")
    # print("}")

if __name__ == "__main__":
    main()
