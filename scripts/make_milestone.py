import os
import sys
from github import Github

def main():
    # Authenticate using the GitHub token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not found in environment variables")
        sys.exit(1)

    github = Github(token)

    # Extract the repository and pull request number
    repository = os.getenv("GITHUB_REPOSITORY")
    if not repository:
        print("GITHUB_REPOSITORY not found in environment variables")
        sys.exit(1)

    owner, repo = repository.split("/")
    pr_number = int(os.getenv("PR_NUMBER"))  # Pass this as an environment variable

    # Fetch the repository
    repo = github.get_repo(f"{owner}/{repo}")

    # Fetch the PR details
    pr = repo.get_pull(pr_number)

    # Define the milestone name
    milestone_name = "Current Milestone"  # Replace with your milestone name

    # Fetch all milestones and find the correct one
    milestones = repo.get_milestones(state="open")
    milestone = next((m for m in milestones if m.title == milestone_name), None)

    if not milestone:
        print(f'Milestone "{milestone_name}" not found')
        sys.exit(1)

    # Add the PR to the milestone
    issue = repo.get_issue(pr_number)
    issue.edit(milestone=milestone)

    print(f'PR #{pr_number} added to milestone "{milestone_name}"')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
