#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import openai
import streamlit as st


openai.api_key = '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'

def get_repo_complexity(repo):
    prompt = f"What is the technical complexity of the repository {repo['name']}?"

    # Use GPT to generate a complexity score
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )

    complexity_score = response.choices[0].text.strip()

    return complexity_score

def get_most_complex_repo(username):
    url = f"https://api.github.com/users/{username}/repos"

    # Fetch user's repositories
    response = requests.get(url)
    repos = response.json()

    if 'message' in repos and repos['message'] == 'Not Found':
        return None

    # Get complexity score for each repository
    complexities = []
    for repo in repos:
        complexity = get_repo_complexity(repo)
        complexities.append((repo['name'], complexity))

    # Sort repositories by complexity score
    complexities = sorted(complexities, key=lambda x: x[1], reverse=True)

    return complexities[0][0]



##Streamlit app start
st.title('GitHub Automated Analysis')

# Input field for GitHub username
username = st.text_input('Enter GitHub username')

if st.button('Analyze'):
    if username:
        try:
            repo_name = get_most_complex_repo(username)
            st.success(f"The most technically complex repository for user '{username}' is '{repo_name}'")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning('Please enter a GitHub username')




