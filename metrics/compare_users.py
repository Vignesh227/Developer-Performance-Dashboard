import streamlit as st
import requests
import pandas as pd
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


# Function to get user data
def get_user_data(username):
    
    # Fetch commits count
    commits_url = f"https://api.github.com/users/{username}/repos"
    repos = requests.get(commits_url, headers=headers).json()
    
    total_commits = 0
    for repo in repos:
        commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits"
        commits = requests.get(commits_url, headers=headers).json()
        total_commits += len(commits)
    
    # Fetch stars received
    total_stars = sum(repo['stargazers_count'] for repo in repos)
    
    return {
        'username': username,
        'commits_count': total_commits,
        'total_stars_received': total_stars
    }

# Main function for the Streamlit page
def main():
    st.title("Compare GitHub Users")

    # Input: Number of users
    num_users = st.number_input("Enter the number of GitHub users:", min_value=1, value=1)

    # Initialize session state for usernames if not present
    if 'usernames' not in st.session_state or len(st.session_state.usernames) != num_users:
        st.session_state.usernames = [''] * num_users

    # Display text boxes for each username
    for i in range(num_users):
        st.session_state.usernames[i] = st.text_input(f"GitHub Username {i+1}:", value=st.session_state.usernames[i])
    
    # Button to add more text boxes
    if st.button("Add User"):
        st.session_state.usernames.append('')
    
    # Button to compare users
    if st.button("Compare"):
        user_data_list = []
        for username in st.session_state.usernames:
            username = username.strip()
            if username:
                data = get_user_data(username)
                user_data_list.append(data)
        
        if user_data_list:
            df = pd.DataFrame(user_data_list)
            
            # Plot Commits Count vs Users
            st.subheader("Commits Count vs Users")
            fig_commits = px.bar(df, x='username', y='commits_count', title='Commits Count vs Users')
            st.plotly_chart(fig_commits)
            
            # Plot Total Stars Received vs Users
            st.subheader("Total Stars Received vs Users")
            fig_stars = px.bar(df, x='username', y='total_stars_received', title='Total Stars Received vs Users')
            st.plotly_chart(fig_stars)
        else:
            st.warning("No user data found.")
