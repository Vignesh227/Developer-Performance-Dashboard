from data_collection.github_api import get_repo_data, get_user_data, get_commits_data, get_total_commits
from data_collection.github_api import get_pull_requests_data, get_deployments_data, get_languages_data

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import altair as alt


st.set_page_config(
    page_title="Developer Performance Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

flag = 0

# Main title for the page
st.title("Developer Performance Dashboard")


# Get input from the user
# maincol1, mc3, maincol2 = st.columns([2, 1,  2])
# with maincol1:
#     repo = st.text_input("Repository Name", "ecapture")
#     owner = st.text_input("Repo Owner Username", "gojue")

# with maincol2:
#     username = st.text_input("Search a User", "gojue")

# # # # # # #

maincol1, mc3, maincol2 = st.columns([2, 1,  2])
with maincol1:
    repo = st.text_input("Repository Name", "Plant-Disease-Prediction")
    owner = st.text_input("Repo Owner Username", "Vignesh227")

with maincol2:
    username = st.text_input("Search a User", "Vignesh227")

# # # # 

# Create columns for buttons to be on the same line
col1, col3, col2 = st.columns([2 ,1, 2])


with col1:
    st.write("")  # This adds space above the button
    if st.button("Search Repository" , use_container_width=True):

        # Fetch repo info using API
        response = get_repo_data(owner, repo)

        if response.status_code == 200:# Successfully fetched

            # Convert from response to JSON format
            repo_data = response.json()

            # Store as session state to display it as
            # a separate section from the button layout
            st.session_state.repo_data = repo_data  
            flag = 1

        elif response.status_code == 404:
            st.error("Repository not found. Please enter a valid repository owner and name.")
        else:
            st.error(f"An error occurred: {response.status_code}. {response.json().get('message', '')}")

with col2:

    st.write("")  # This adds space above the button
    
    if st.button("Search User", use_container_width=True):

        # Fetch user info using API
        response = get_user_data(username)

        if response.status_code == 200: # Successfully fetched

            # Convert from response to JSON format
            user_data = response.json()

            # Store as session state to display it as
            # a separate section from the button layout
            st.session_state.user_data = user_data  
            flag = 2


        elif response.status_code == 404:
            st.error("Repository not found. Please enter a valid repository owner and name.")
        else:
            st.session_state.user_data = {"error": f"An error occurred: {response.status_code}. {response.json().get('message', '')}"}


st.write("")
st.write("")
st.write("")
st.write("")

# If Get repo data button clicked,
# flag is set to 1
# To display repository details
if flag == 1:
    # st.write(st.session_state.repo_data)  

    repo_data = st.session_state.repo_data


    st.divider()

    # Display Repository  information (About)
    

    owner_data = repo_data.get('owner', {})

    col1, coll2 = st.columns([3.5,1])

    with col1:
        if owner_data:
            st.write("")
            st.subheader("Repository Overview")
            col1, col2, col3, col4 = st.columns(4)
        
            with col1:
                st.metric(label="Total Stars", value=repo_data['stargazers_count'] or 'N/A')
            with col2:
                st.metric(label="Forks", value=repo_data['forks_count'] or 'N/A')
            with col3:
                st.metric(label="Open Issues", value=repo_data['open_issues_count'] or 'N/A')
            with col4:
                total_commits = get_total_commits(owner, repo)
                st.metric(label="Total Commits", value=total_commits or 'N/A')


            # st.divider()    
            st.write("")
            st.write("")


            
            st.subheader("Repository Information")
            st.write(f"**Repository Owned by :** {owner_data['login'] or 'Not provided'}")
            st.write(f"**URL:** [View Repository]({owner_data['html_url'] or 'Not provided'})") 
            st.write(f"**Description:** {repo_data['description'] or 'Not provided'}")

            st.write("")
            
    with coll2:
        if owner_data:
            st.write("")
            st.write("")
            st.image(owner_data['avatar_url'], width=100 , use_column_width=True)


    


    st.divider()


    #                    #
    # Next Visualization #
    #                    #



    # Cards for repository features
    st.write("")
    st.subheader("Repository Features")

    col1, col2, col3, col4, col5 = st.columns(5)
        
    with col1:
        st.metric(label="Issues", value='✅' if repo_data['has_issues'] else '❌')

    with col2:
        st.metric(label="Downloads", value='✅' if repo_data['has_downloads'] else '❌')
    with col3:
        st.metric(label="Wiki", value='✅' if repo_data['has_wiki'] else '❌')
    with col4:
        st.metric(label="Github Pages", value='✅' if repo_data['has_pages'] else '❌')
    with col5:
        st.metric(label="Discussions", value='✅' if repo_data['has_discussions'] else '❌')

    st.write("")
    st.write("")

    # features = {
    #     'Has Issues': repo_data['has_issues'],
    #     'Has Projects': repo_data['has_projects'],
    #     'Has Downloads': repo_data['has_downloads'],
    #     'Has Wiki': repo_data['has_wiki'],
    #     'Has Pages': repo_data['has_pages'],
    #     'Has Discussions': repo_data['has_discussions']
    # }
    # fig = px.pie(names=list(features.keys()), values=[int(val) for val in features.values()], title="Repository Features")
    # st.plotly_chart(fig)


    st.divider()


    #                    #
    # Next Visualization #
    #                    #

   
    # Pie chart for Freq of programming languaes used
    st.write("")
    st.subheader("Most Used Languages")
    
    language_data = get_languages_data(owner, repo)

    if language_data:
        # Separate data as:
        # - Languages used
        # - Size(amount) of the languages used
        languages = list(language_data.keys())
        sizes = list(language_data.values())

        sizes = [int(int(size)/1024) for size in sizes]

        fig = px.bar(
            x=languages,
            y=sizes,
            title=f"Languages Used",
            labels={'x': 'Languages', 'y': 'Size (Kilo Bytes)'},
            text=sizes  # Add size labels on the bars
        )

        fig.update_traces(
            # Display values on the bars
            texttemplate='%{text:.0f} KB',
            textposition='outside',
            # Hover to display both language and value
            hovertemplate='<b>%{x}</b><br>Size: %{y} KB<extra></extra>'
        )

        # Display the bar graph in Streamlit
        st.plotly_chart(fig)
    else:
        st.error("No data available for the repository.")
    st.write("")

    st.divider()


    #                    #
    # Next Visualization #
    #                    #


    # Line graph for commits over time
    st.write("")
    st.subheader("Commits Over Time")

    # Fetch commit data using API
    commits_response = get_commits_data(owner, repo)


    if commits_response.status_code == 200: # If fetched successfull
        
        # Convert from response to JSON format
        commits_data = commits_response.json()

        # Split X and Y
        dates = [commit['commit']['author']['date'][:10] for commit in commits_data]
        counts = [dates.count(date) for date in sorted(set(dates))]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sorted(set(dates)), y=counts, mode='lines+markers', name='Commits'))
        fig.update_layout(title="Commits Over Time", xaxis_title='Date', yaxis_title='Number of Commits')
        st.plotly_chart(fig)
    else:
        st.write("Commits data not available.")

    st.write("")


    st.divider()


    #                    #
    # Next Visualization #
    #                    #


    # Scatter plot for pull requests vs deployments
    st.write("")
    st.subheader("Pull Requests vs Deployments")

    pull_requests_response = get_pull_requests_data(owner, repo)
    deployments_response = get_deployments_data(owner, repo)

    if pull_requests_response.status_code == 200 and deployments_response.status_code == 200:
        pull_requests_data = pull_requests_response.json()
        deployments_data = deployments_response.json()

        pull_requests_count = len(pull_requests_data)
        deployments_count = len(deployments_data)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1], y=[pull_requests_count], mode='markers', name='Pull Requests'))
        fig.add_trace(go.Scatter(x=[2], y=[deployments_count], mode='markers', name='Deployments'))
        fig.update_layout(title="Pull Requests vs Deployments", xaxis_title='Category', yaxis_title='Count',
                            xaxis=dict(tickvals=[1, 2], ticktext=['Pull Requests', 'Deployments']))
        st.plotly_chart(fig)
    else:
        st.write("Pull requests or deployments data not available.")

    st.write("")
    
    st.divider()


    #                    #
    # Next Visualization #
    #                    #


    # Additional Metrics
    st.write("")
    st.subheader("Additional Metrics")
    st.write(f"Repository Size: {repo_data.get('size', 'N/A')} KB")
    st.write(f"Default Branch: {repo_data.get('default_branch', 'N/A')}")
    # st.write(f"License: {repo_data.get('license', {}).get('name', 'N/A')}")
    st.write(f"Visibility: {repo_data.get('visibility', 'N/A')}")


# If Get user data button clicked,
# flag is set to 2
# To display user details
if flag == 2:

    # user_data = st.session_state.user_data
    # st.write(user_data)
    st.divider()

    # Define layout using columns
    col1, col2 = st.columns([3.3, 1])

    # Display user avatar 
    with col2:
        st.write("")
        st.image(user_data['avatar_url'], width=90 , use_column_width=True)

    # Display basic info about the user
    with col1:
        st.header(user_data['name'])
        st.write(f"**Username :** {user_data['login']}")
        st.write(f"**Bio :** {user_data['bio'] or 'No bio available'}")
        st.write(f"**Work / Study :** {user_data['company'] or 'Not specified'}")
        st.write(f"**Location :** {user_data['location'] or 'Not specified'}")
        st.write(f"**Email :** {user_data['email'] or 'Not specified'}")
        st.write(f"**Personal Portfolio :** [Visit Portfolio]({user_data['blog']})" if user_data['blog'] else 'No blog available')
        st.write(f"**Profile URL :** [Visit Profile]({user_data['html_url']})")

    st.write("")

    # Use expander(open/collapse) for detailed statistics
    with st.expander("Other Statistics"):
        st.write(f"**Public Repositories:** {user_data['public_repos']}")
        st.write(f"**Public Gists:** {user_data['public_gists']}")
        st.write(f"**Followers:** {user_data['followers']}")
        st.write(f"**Following:** {user_data['following']}")
        st.write(f"**Created At:** {user_data['created_at'][:10]}")
        st.write(f"**Updated At:** {user_data['updated_at'][:10]}")
