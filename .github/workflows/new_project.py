import requests
import os
import datetime
import json
import argparse

# GitHub API Config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Use GitHub Actions secret
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")  # "owner/repo"
GITHUB_API_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
            

def get_existing_projects():
    """Fetch existing repository projects."""
    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/projects"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching projects: {response.text}")
        return []


def close_old_project(sprint_number, start_date, end_date):
    """Close the previous project board."""
    projects = get_existing_projects()
    if projects:
        last_project_id = projects[0]["id"]
        url = f"{GITHUB_API_URL}/projects/{last_project_id}"
        response = requests.patch(url, headers=HEADERS, json={"state": "closed"})
        if response.status_code == 200:
            print(f"Closed previous project: {projects[0]['name']}")
        else:
            print(f"Failed to close project: {response.text}")


def create_project(sprint_number, start_date, end_date):
    """Create a new project board."""
    project_title = f"Sprint {sprint_number}: {start_date} - {end_date}"
    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/projects"
    payload = {"name": project_title, "body": "Sprint project board for tracking progress"}
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 201:
        project_id = response.json()["id"]
        print(f"Project '{project_title}' created with ID: {project_id}")
        return project_id
    else:
        print(f"Failed to create project: {response.text}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a new sprint project')
    parser.add_argument('sprint_number', type=int, help='Sprint number')
    parser.add_argument('start_date', type=str, help='Sprint start date (YYYY-MM-DD)')
    parser.add_argument('end_date', type=str, help='Sprint end date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # Convert string dates to datetime objects
    start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d').date()
    
    close_old_project(args.sprint_number, start_date, end_date)
    create_project(args.sprint_number, start_date, end_date)
