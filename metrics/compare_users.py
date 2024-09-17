import streamlit as st
import requests
import pandas as pd
from io import StringIO
import plotly.express as px


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


# Fetch user data from GitHub API
def get_total_commits_stars_and_pull_requests(username):

    # Initialize totals
    total_commits = 0
    total_stars = 0
    total_pull_requests = 0

    # Initialize pagination for repos
    page = 1
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"

    while True:
        repos_response = requests.get(repos_url, headers=headers)
        repos = repos_response.json()

        # Break if no more repositories
        if len(repos) == 0:
            break

        # Loop through each repository to count commits, stars, and pull requests
        for repo in repos:
            # Fetch commits for each repository with pagination
            commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits?per_page=100&page="
            commits_page = 1

            while True:
                paginated_commits_url = commits_url + str(commits_page)
                commits_response = requests.get(paginated_commits_url, headers=headers, timeout=1000)
                commits = commits_response.json()

                # Break if no more commits
                if len(commits) == 0:
                    break

                # Add the number of commits from this page
                total_commits += len(commits)
                commits_page += 1

            # Fetch pull requests for each repository with pagination
            pull_requests_url = f"https://api.github.com/repos/{username}/{repo['name']}/pulls?state=all&per_page=100&page="
            pull_requests_page = 1

            while True:
                paginated_prs_url = pull_requests_url + str(pull_requests_page)
                pr_response = requests.get(paginated_prs_url, headers=headers, timeout=1000)
                pull_requests = pr_response.json()

                # Break if no more pull requests
                if len(pull_requests) == 0:
                    break

                # Add the number of pull requests from this page
                total_pull_requests += len(pull_requests)
                pull_requests_page += 1

            # Add the stargazers count for the repository
            total_stars += repo['stargazers_count']

        # Move to the next page of repos
        page += 1
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"

    return {
        'username': username,
        'commits_count': total_commits,
        'total_stars_received': total_stars,
        'total_pull_requests': total_pull_requests
    }




# Main function for the Streamlit page
def main():
    st.title("Compare Multiple GitHub Users")

    # Input: GitHub usernames
    st.write("")
    usernames = st.text_area("Enter GitHub usernames separated by commas:", "").split(',')
    st.write("")


    if st.button("Compare", use_container_width=True):
        st.write("")


        with st.spinner('Fetching User Data...'):
            user_data_list = []

            for username in usernames:
                username = username.strip()
                
                if username:
                    data = get_total_commits_stars_and_pull_requests (username)
                    user_data_list.append(data)
            
            if user_data_list:
                df = pd.DataFrame(user_data_list)
                
                # Plot Commits Count vs Users
                st.divider()
                
                col1, col3, col2 = st.columns([2 ,1,  2])

                with col1:
                    st.subheader("Commits Count vs Users")
                    fig_commits = px.bar(df, x='username', y='commits_count')
                    st.plotly_chart(fig_commits)

                
                with col2:
                    # Plot Total Stars Received vs Users
                    st.subheader("Total Stars Received vs Users")
                    fig_stars = px.bar(df, x='username', y='total_stars_received')
                    st.plotly_chart(fig_stars)

                st.divider()

                # Display metrics in Streamlit
                st.write("")
                st.subheader("Total Pull Requests Made")
                st.write("")

                cols = st.columns(len(user_data_list))
                for i, user_data in enumerate(user_data_list):
                    with cols[i]:
                        st.metric(label=f"{user_data['username']} ", value=user_data['total_pull_requests'])

                st.divider()

                # Create DataFrame from the fetched user data
                df = pd.DataFrame(user_data_list)

                # Display the DataFrame in Streamlit
                st.subheader("Fetched Data")
                st.dataframe(df)

                # Export the CSV inside the 'data_collection' folder
                csv_file_path = os.path.join('data_collection', 'Multiple_users_data.csv')
                df.to_csv(csv_file_path, index=False)

                # Prepare CSV for download via Streamlit
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)

                # Add a button to download the DataFrame as CSV
                st.download_button(
                    label="Export CSV",
                    data=csv_buffer.getvalue(),
                    file_name='Multiple_users_data.csv',
                    mime='text/csv'
                )

                st.divider()

            else:
                st.warning("No user data found.")
