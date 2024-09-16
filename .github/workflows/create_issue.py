import os
import requests
from datetime import datetime

# Hardcoded dates for issue creation (format: 'MM-DD')
hardcoded_dates = ['09-16', '09-18', '10-02','10-16', '10-30']  # Add your desired dates here

# Get today's date
today = datetime.now().strftime('%m-%d')

# Set up your issue details in a dictionary or list
issues = [
    {
        "title": "Edge Issue",
        "body": "Edge issue body content",
        "labels": ["service-request"],
        "assignees": ["butlerbt"]
    },
    {
        "title": "Cloud Issue",
        "body": "Cloud issue body content",
        "labels": ["service-request"],
        "assignees": ["butlerbt"]
    },
    {
        "title": "Web Issue",
        "body": "Web issue body content",
        "labels": ["service-request"],
        "assignees": ["butlerbt"]
    },
    {
        "title": "Mobile Issue",
        "body": "Mobile issue body content",
        "labels": ["service-request"],
        "assignees": ["butlerbt"]
    }
]

# Check if today is in the list of hardcoded dates
if today in hardcoded_dates:
    repo = os.getenv('GITHUB_REPOSITORY')
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'}

    date_str = datetime.now().strftime('%B %d, %Y')
    issue_title = f"Automated Issue for Edge"
    issue_body = "This is an automated issue created on " + date_str

    labels = ['service-request']  # Replace with your desired labels

    for issue in issues:
        response = requests.post(f'https://api.github.com/repos/{repo}/issues', json=issue, headers=headers)

        if response.status_code == 201:
            print(f'Successfully created issue: {issue["title"]}')
        else:
            print(f'Failed to create issue: {issue["title"]}. Response: {response.content}')
else:
    print(f"No issue created today. Today is {today}, not one of the hardcoded dates.")
