from data_collection.github_api import get_repo_data, get_user_data, get_all_commits, fetch_user_contributions
from data_collection.github_api import get_pull_requests, get_languages_data, extract_pr_data
from data_collection.github_api import prepare_pr_date_data, calculate_average_resolution_time
from visualization.charts import plot_languages_used_graph, plot_commits_linegraph, plot_pr_vs_merge_graph

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

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("What info do you want?", ["Single User/Repo", "Multiple Users"])


if page == "Single User/Repo":
    flag = 0

    # Main title for the page
    st.title("Developer Performance Dashboard")

    st.write("")

    # Get input from the user
    # maincol1, mc3, maincol2 = st.columns([2, 1,  2])
    # with maincol1:
    #     repo = st.text_input("Repository Name", "ecapture")
    #     owner = st.text_input("Repo Owner Username", "gojue")

    # with maincol2:
    #     username = st.text_input("Search a User", "gojue")

    # # # # # # #

    maincol1, mc3, maincol2 = st.columns([2, 0.5,  2])
    with maincol1:
        repo = st.text_input("Repository Name", "Plant-Disease-Prediction")
        owner = st.text_input("Repo Owner Username", "Vignesh227")

    with maincol2:
        username = st.text_input("Search a User", "Vignesh227")

    # # # # 

    # Create columns for buttons to be on the same line
    col1, col3, col2 = st.columns([2 ,0.5   , 2])


    with col1:
        st.write("")  # This adds space above the button
        if st.button("Search Repository" , use_container_width=True):

            # Fetch repo info using API
            response = get_repo_data(owner, repo)
            # st.write(response)
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

        # Drop down box to notify the search
        # st.toast('Repository search is in progress', icon='🔎')

        # st.write(st.session_state.repo_data)  
        with st.spinner('Searching Repository & Processing Data . . .'):
            try:
                repo_data = st.session_state.repo_data


                st.divider()

                # Display Repository  information (About)
                

                owner_data = repo_data.get('owner', {})

                col1, coll2 = st.columns([3.5,1])

                # Fetching commits data
                # made on a particular repository
                total_commits = get_all_commits(owner, repo)

                with col1:
                    if owner_data:
                        st.write("")
                        st.subheader("Repository Overview")
                        col1, col2, col3, col4 = st.columns(4)

                        

                        with col1:
                            
                            st.metric(label="Total Commits", value=len(total_commits) or 'N/A')
                        with col2:
                            st.metric(label="Forks", value=repo_data['forks_count'] or '0')
                        with col3:
                            st.metric(label="Open Issues", value=repo_data['open_issues_count'] or '0')
                        with col4:
                            st.metric(label="Total Stars", value=repo_data['stargazers_count'] or '0')

                            

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
                st.write("")    

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


                # Line graph for commits over time
                st.write("")
                st.subheader("Commits Over Time")

                # Store total commits
                commits_response = total_commits

                if commits_response: # If fetched successfull
                    #Func call to plot the line graph
                    plot_commits_linegraph(commits_response)
                else:
                    st.write("Commits data not available.")

                st.write("")


                st.divider()

                #                    #
                # Next Visualization #
                #                    #

            
                # Bar graph for Freq of programming languaes used
                st.write("")
                st.subheader("Most Used Languages")
                
                # Func to fetch languages used data using API
                language_data = get_languages_data(owner, repo)

                if language_data:
                    # Func call to plot the bar graph
                    plot_languages_used_graph(language_data)

                else:
                    st.error("No data available for the repository.")

                st.write("")

                st.divider()


                #                    #
                # Next Visualization #
                #                    #


                # Scatter plot for pull requests vs Merge Requests
                st.write("")

                st.subheader("Pull Requests vs Merged Requests over Time")
                pull_requests = get_pull_requests(owner, repo)
                    
                if pull_requests:
                    pr_data = extract_pr_data(pull_requests)
                    created_counts, merged_counts = prepare_pr_date_data(pr_data)
                    plot_pr_vs_merge_graph(created_counts, merged_counts)

                else:
                    st.error("Pull requests / Merged Request data not available for this repository.")

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

            except:
                st.success("Done!")



    # If Get user data button clicked,
    # flag is set to 2
    # To display user details
    if flag == 2:

        # Drop down box to notify the search
        # st.toast('User search is in progress', icon='🔎')


        # user_data = st.session_state.user_data
        # st.write(user_data)
        with st.spinner('Searching User & Processing Data . . .'):
            st.divider()

            # Define layout using columns
            col1, col2 = st.columns([3.3, 1])


            # Display basic info about the user
            with col1:
                # Function to retrieve the user Contributions
                # Contributions returned as a list here 
                user_contributions = fetch_user_contributions(username)
                
                st.header(user_data['name'])

                cols = st.columns(4)

                # Iterate over the user contributions and display them in the columns
                for i, (metric, value) in enumerate(user_contributions.items()):
                    col = cols[i % 4]  # Cycle through the 4 columns (for 4 values)
                    with col:
                        st.metric(label=metric, value=value, delta_color="inverse")

                st.divider()
                        
                
                st.write(f"**Username :** {user_data['login']}")
                st.write(f"**Bio :** {user_data['bio'] or 'No bio available'}")
                st.write(f"**Work / Study :** {user_data['company'] or 'Not specified'}")
                st.write(f"**Location :** {user_data['location'] or 'Not specified'}")
                st.write(f"**Email :** {user_data['email'] or 'Not specified'}")
                st.write(f"**Personal Portfolio :** [Visit Portfolio]({user_data['blog']})" if user_data['blog'] else 'No blog (personal site )available')
                st.write(f"**Profile URL :** [Visit Profile]({user_data['html_url']})")
                st.write("")
        
            # Display user avatar 
            with col2:
                
                st.write("")
                st.write("")
                st.image(user_data['avatar_url'], width=90 , use_column_width=True)


            st.divider()

            st.write("")


            # Use expander(open/collapse) for detailed statistics
            with st.expander("Other Statistics"):
                st.write(f"**Public Repositories:** {user_data['public_repos']}")
                st.write(f"**Public Gists:** {user_data['public_gists']}")
                st.write(f"**Followers:** {user_data['followers']}")
                st.write(f"**Following:** {user_data['following']}")

                avg_resolution_time = calculate_average_resolution_time(username)
                if avg_resolution_time:
                    st.write(f"**Average Issue Resolution Time (in hours)** {round(avg_resolution_time, 2)}")
                else:
                    st.write(f"**Issues :** No Issues found")

                st.write(f"**Created At:** {user_data['created_at'][:10]}")
                st.write(f"**Updated At:** {user_data['updated_at'][:10]}")
        

else:
    # Import and run the compare_users.py script
    from metrics.compare_users import main as compare_users_main
    compare_users_main()