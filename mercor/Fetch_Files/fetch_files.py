import requests
import re


def fetch_user_repositories(github_url):
    """
    Fetches the repositories of a user from GitHub using the GitHub API.

    Args:
        github_url (str): The GitHub URL of the user.

    Returns:
        repositories (list): List of user repositories in JSON format, or an empty list if an error occurred.
        
    """
    # Extracting username from GitHub URL
    username = github_url.split("/")[-1]

    # GitHub API endpoint for user repositories
    api_url = f"https://api.github.com/users/{username}/repos"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            repositories = response.json()
            return repositories
        else:
            print("Failed to retrieve repositories. Please check the user URL.")
            return []
    except requests.exceptions.RequestException as e:
        print("Error occurred while connecting to GitHub API:", e)
        return []


def fetch_files_from_github(repository_url):
    """
    Fetches the files from a GitHub repository using the GitHub API.

    Args:
        repository_url (str): The URL of the GitHub repository.

    Returns:
        file_urls (list): List of tuples containing the download URL and file path of each file.
    """
    # Extracting username and repository name from GitHub URL
    match = re.match(r"https://github.com/([^/]+)/([^/]+)", repository_url)
    if not match:
        print("Invalid GitHub URL.")
        return []

    username, repository_name = match.groups()
    api_url = f"https://api.github.com/repos/{username}/{repository_name}/contents"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            files = response.json()
            file_urls = []

            def extract_file_urls(items, path=""):
                for item in items:
                    if item['type'] == 'file':
                        file_urls.append((item['download_url'], path + item['name']))
                    elif item['type'] == 'dir':
                        subfolder_url = item['url']
                        subfolder_response = requests.get(subfolder_url)
                        if subfolder_response.status_code == 200:
                            subfolder_files = subfolder_response.json()
                            extract_file_urls(subfolder_files, path + item['name'] + "_")

            extract_file_urls(files)
            return file_urls
        else:
            print("Failed to retrieve files. Please check the repository URL.")
            return []
    except requests.exceptions.RequestException as e:
        print("Error occurred while connecting to GitHub API:", e)
        return []
