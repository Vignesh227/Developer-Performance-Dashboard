import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Function to bar  graph (Languages used)
def plot_languages_used_graph(language_data):
    # Separate data as:
    # - Languages used
    # - Size(amount) of the languages used
    languages = list(language_data.keys())
    sizes = list(language_data.values())

    sizes = [int(int(size)/1024) for size in sizes]

    # Bar graph
    fig = px.bar(
        x=languages,
        y=sizes,
        # title=f"Languages Used",
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




# Function to plot Line graph (Commits against time)
def plot_commits_linegraph(commits_data):
    # Convert from response to JSON format

    # Split X and Y
    dates = [commit['commit']['author']['date'][:10] for commit in commits_data]
    counts = [dates.count(date) for date in sorted(set(dates))]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted(set(dates)), y=counts, mode='lines+markers', name='Commits'))
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of Commits')

    # Display the graph
    st.plotly_chart(fig)



def plot_pr_vs_merge_graph(created_counts, merged_counts):
    """
    Plot a line graph between pull requests and merge requests (date-wise).
    """
    fig = go.Figure()

    # Plot Pull Requests
    fig.add_trace(go.Scatter(
        x=created_counts.index, 
        y=created_counts.values, 
        mode='lines+markers', 
        name='Pull Requests',
        line=dict(color="#3461c9")
    ))

    # Plot Merged Requests
    fig.add_trace(go.Scatter(
        x=merged_counts.index, 
        y=merged_counts.values, 
        mode='lines+markers', 
        name='Merged Requests',
        line=dict(color="#a1cef7")
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Count',
        template='plotly_dark'
    )

    # Show the graph in Streamlit
    st.plotly_chart(fig)

