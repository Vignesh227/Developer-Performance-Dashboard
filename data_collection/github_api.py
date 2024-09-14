import requests


# Github Personal Access Token
TOKEN = ""

# Authorize the token for further processing
headers = { "Authorization": f"token {TOKEN}" }

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
def get_commits_data(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url, headers=headers)
    return response

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





# Function to fetch the total number of commits
# made for that particular repo
def get_total_commits(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    total_commits = 0
    page = 1
    
    while True:
        response = requests.get(url, headers=headers, params={'page': page, 'per_page': 100} , timeout=100)
        if response.status_code == 200:
            commits = response.json()
            if not commits:
                break
            total_commits += len(commits)
            page += 1
        else:
            print(f"Error: {response.status_code} - {response.json().get('message', '')}")
            return None
    
    return total_commits


