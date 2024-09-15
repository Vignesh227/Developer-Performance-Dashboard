import requests
import pandas as pd
from datetime import datetime
import streamlit as st

# Github Personal Access Token
# TOKEN = "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"

# # Authorize the token for further processing
# headers = { "Authorization": f"token {TOKEN}" }

import os
from dotenv import load_dotenv # type: ignore

# Specify the path to the .env file (one level above)
load_dotenv(dotenv_path='../.env')

# Access the API key from the environment variable
GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')

# Set up headers for GitHub API
headers = {
    "Authorization": f"Bearer {GITHUB_API_KEY}"
}


# Func to get the details about a particular repository
def get_repo_data(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)
    return response

# Func to get details about a particular user
def get_user_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)
    return response





# Func to fetch commits data for a repo
def get_all_commits(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    all_commits = []
    params = {"per_page": 1000, "page": 1}

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        commits = response.json()
        if not commits:
            break  # No more commits to fetch
        
        all_commits.extend(commits)
        params["page"] += 1  # Go to the next page

    return all_commits

# Func to fetch pull requests data for a repo
def get_pull_requests_data(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all"
    response = requests.get(url, headers=headers)
    return response

# Func to fetch deployments data for a repo
def get_deployments_data(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/deployments"
    response = requests.get(url, headers=headers)
    return response


# Func to fetch deployments data for a repo
def get_languages_data(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    response = requests.get(url, headers=headers)
    return response.json()






# Preprocess Pull requests data (for plotting Pr vs Mr graph)
def extract_pr_data(pull_requests):
    """
    Extract pull request creation and merge dates.
    """
    pr_data = []
    
    for pr in pull_requests:
        created_at = pr['created_at'][:10]  # YYYY-MM-DD format
        merged_at = pr['merged_at'][:10] if pr['merged_at'] else None  # If merged
        
        pr_data.append({
            'created_at': created_at,
            'merged_at': merged_at
        })
    
    return pr_data

# Preprocess Merge requests data (for plotting Pr vs Mr graph)
def prepare_pr_date_data(pr_data):
    """
    Prepare date-wise data for pull requests and merge requests.
    """
    created_dates = [pr['created_at'] for pr in pr_data]
    merged_dates = [pr['merged_at'] for pr in pr_data if pr['merged_at']]

    # Count occurrences of each date
    created_counts = pd.Series(created_dates).value_counts().sort_index()
    merged_counts = pd.Series(merged_dates).value_counts().sort_index()

    return created_counts, merged_counts






#   -   -   -   -   -   # 
# Get info about a user #
#   -   -   -   -   -   #

# Helper function to handle pagination
# This iterates page by page,
# Thus fetches info from all pages 
# Base URL for GitHub API
def get_all_pages(url, params={}):
    all_results = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None

        all_results.extend(response.json())
        # Check if there's a "next" page
        url = response.links.get("next", {}).get("url")
    return all_results


# 1. Fetch all repositories of the user
def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    return get_all_pages(url)


# 2. Pull Requests Count
def get_pull_requests(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {'state': 'all', 'author': owner}
    pull_requests = get_all_pages(url, params)
    return pull_requests


# 3. Merged Pull Requests Count
def get_merged_pull_requests_count(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {'state': 'closed', 'author': owner}
    pull_requests = get_all_pages(url, params)

    # Count merged PRs
    merged_count = sum(1 for pr in pull_requests if pr.get('merged_at'))
    return merged_count


# 4. Issues Opened Count
def get_issues_opened_count(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {'state': 'all', 'creator': owner}
    issues = get_all_pages(url, params)
    return len(issues)


# 5. Total Contributions (Commits) Count
def get_total_commits_count(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {'author': owner}
    commits = get_all_pages(url, params)
    return len(commits)


# 6. Fetch overall stats across all repos
def fetch_user_contributions(owner):
    repos = get_user_repos(owner)

    total_pull_requests = 0
    total_merged_pull_requests = 0
    total_issues_opened = 0
    total_commits = 0

    if repos:
        for repo in repos:
        
            repo_name = repo['name']

            # Count of Pull Requests 
            total_pull_requests = len(get_pull_requests(owner, repo_name))

            # Count of total merged pull requests
            total_merged_pull_requests += get_merged_pull_requests_count(owner, repo_name)

            # Count of Issues Opened
            total_issues_opened += get_issues_opened_count(owner, repo_name)

            # Total Commits(Contributions) made by the user
            total_commits += get_total_commits_count(owner, repo_name)

    return { "Pull Requests" : total_pull_requests, 
            "Merged Pull Requests" : total_merged_pull_requests,
            "Issues Opened" : total_issues_opened,
            "Contributions (Commits)" : total_commits
    }





# Function to fetch all repositories for a given user/organization
def get_user_repositories(owner):
    url = f"https://api.github.com/users/{owner}/repos?per_page=100"
    repos = []
    page = 1

    while True:
        response = requests.get(f"{url}&page={page}", headers=headers)
        if response.status_code != 200:
            st.write(f"Failed to fetch repositories: {response.status_code}")
            return None

        repo_page = response.json()
        if not repo_page:
            break

        repos.extend(repo_page)
        page += 1

    return repos

# Function to fetch issues opened by a specific user for a given repository
def get_user_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=100"
    user_issues = []
    page = 1

    while True:
        response = requests.get(f"{url}&page={page}", headers=headers)
        if response.status_code != 200:
            st.write(f"Failed to fetch issues: {response.status_code}")
            return None

        issues = response.json()
        if not issues:
            break

        # Filter issues created by the specific user and exclude pull requests
        for issue in issues:
            # if 'pull_request' not in issue:  # Ignore pull requests
            user_issues.append(issue)
        
        page += 1

    return user_issues

# Function to calculate average issue resolution time for all repositories of a user
def calculate_average_resolution_time(owner):
    repos = get_user_repositories(owner)
    
    if not repos:
        return None

    all_resolution_times = []

    for repo in repos:
        repo_name = repo['name']
        issues = get_user_issues(owner, repo_name)
        
        if not issues:
            continue

        resolution_times = []

        for issue in issues:
            if issue['state'] == 'closed':
                created_at = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                closed_at = datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
                resolution_time = (closed_at - created_at).total_seconds() / 3600  # Convert to hours
                resolution_times.append(resolution_time)

        if resolution_times:
            all_resolution_times.extend(resolution_times)

    if all_resolution_times:
        average_resolution_time = sum(all_resolution_times) / len(all_resolution_times)
        return average_resolution_time
    else:
        return None