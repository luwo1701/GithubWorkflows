import os
from github import Github

# Set your GitHub repo details
def get_latest_tag(repo):
    tags = repo.get_tags()
    latest_tag = next(tags, None)
    return latest_tag.name if latest_tag else None

def get_current_milestone(repo):
    milestones = repo.get_milestones(state="open")
    return next(milestones, None)

def close_and_rename_milestone(milestone, new_name):
    milestone.edit(title=new_name, state="closed")
    return milestone

def create_new_milestone(repo, name="current milestone"):
    return repo.create_milestone(title=name)

def main():
    token = os.getenv("GITHUB_TOKEN")    
    repo = os.getenv("GITHUB_REPOSITORY")
    latest_tag = get_latest_tag(repo)
    if not latest_tag:
        print("No tags found in the repository.")
        return

    current_milestone = get_current_milestone(repo)
    if current_milestone:
        print(f"Current milestone: {current_milestone.title}")
        close_and_rename_milestone(current_milestone, latest_tag)
        print(f"Closed milestone renamed to: {latest_tag}")
    else:
        print("No open milestones found.")

    new_milestone = create_new_milestone(repo)
    print(f"New milestone created: {new_milestone.title}")

if __name__ == "__main__":
    main()
