import os
import requests
from datetime import datetime

# Hardcoded dates for issue creation (format: 'MM-DD')
hardcoded_dates = ['09-15', '10-05', '12-25']  # Add your desired dates here

# Get today's date
today = datetime.now().strftime('%m-%d')

# Check if today is in the list of hardcoded dates
if today in hardcoded_dates:
    repo = os.getenv('GITHUB_REPOSITORY')
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'}

    date_str = datetime.now().strftime('%B %d, %Y')
    issue_title = f"Automated Issue for Edge"
    issue_body = "This is an automated issue created on " + date_str

    labels = ['service-request']  # Replace with your desired labels

    edge_issue = {
        "title": issue_title,
        "body": issue_body,
        "labels": labels
    }

    response = requests.post(f'https://api.github.com/repos/{repo}/issues', json=edge_issue, headers=headers)

    if response.status_code == 201:
        print('Issue created successfully')
    else:
        print(f'Failed to create issue: {response.content}')
else:
    print(f"No issue created today. Today is {today}, not one of the hardcoded dates.")
