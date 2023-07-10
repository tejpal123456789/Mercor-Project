import streamlit as st
import streamlit as st

from Fetch_Files.fetch_files import fetch_user_repositories
from Backend.main import GPT_call
import pandas as pd



# Streamlit app
st.title("Top Repositories and Complexity")
github_link = st.text_input("Enter GitHub profile link")
submit_button = st.button("Submit")

if submit_button and github_link:
    # Replace the code below with your own implementation to fetch the repository data
    # Ensure that repo_data is a list of dictionaries
    
    repositories = fetch_user_repositories(github_link)
    repo = {}
    for repository in repositories:
        repo[repository["name"]] = repository["html_url"]

    df_sorted = GPT_call(repo)

    reason_of_the_complexity = df_sorted['reason']

    df_sorted.drop(columns=['reason'], inplace=True)

    st.title("Top 5 Repositories with their Complexity Complexity")
    st.table(df_sorted.head(5))

    # Display the name and link of each repository
    # Display the name and link of each repository
    st.title("Repository Details")
    for index, row in df_sorted.head(5).iterrows():
        repo_name = row.iloc[0]
        repo_link = repo.get(repo_name, "Not available")
        st.write(f"**Repository Name:** {repo_name}")
        st.write(f"**Repository Link:** {repo_link}")
        st.write('---')

    st.title("Repository Details:")
    for i in range(5):
        repo_name = df_sorted.iloc[i]['repo_name']
        reason = reason_of_the_complexity.iloc[i]
        st.write(f"Repo Name: **{repo_name}**")
        st.write(f"Reason: {reason}")


