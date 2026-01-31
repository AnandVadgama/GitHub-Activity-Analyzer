import json
from datetime import datetime
import requests
from requests.exceptions import RequestException, HTTPError, Timeout
from file_handler import load_commits_from_file, save_commit_message_json

def fetch_github_repos(username):
    """Fetch all repositories for a user using pagination"""
    all_repos = []
    page = 1
    per_page = 100  # Maximum allowed per page
    
    print(f"🔍 Fetching repositories for {username}...")
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page={per_page}"
        print(f"📄 Fetching page {page}...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()

        except Timeout:
            print("⚠️ Request timed out — check your internet")
            return all_repos if all_repos else []

        except HTTPError as e:
            if response.status_code == 404:
                print(f"❌ Username '{username}' not found")
            elif response.status_code == 403:
                print("⚠️ GitHub rate limit hit — wait an hour or use token")
            else:
                print(f"API error {response.status_code}: {e}")
            return all_repos if all_repos else []

        except RequestException as e:
            print(f"🌐 Network error: {e}")
            return all_repos if all_repos else []

        try:
            json_data = response.json()
        except ValueError:
            print("❌ Invalid JSON from API")
            return all_repos if all_repos else []

        # Check if response is a list of repos
        if not isinstance(json_data, list):
            print(f"Unexpected API response format: {type(json_data)}")
            print(f"Response: {json_data}")
            return all_repos if all_repos else []

        # If we got no repos on this page, we've reached the end
        if not json_data:
            break
            
        # Add repos from this page
        all_repos.extend(json_data)
        print(f"✅ Got {len(json_data)} repositories from page {page}")
        
        # If we got less than per_page, this was the last page
        if len(json_data) < per_page:
            break
            
        page += 1

    print(f"🎉 Total repositories fetched: {len(all_repos)}")
    return all_repos

def github_commit_extractor(json_data, username):
    """Extract commit data with user-specific caching"""
    repo_count = len(json_data)
    all_commits = load_commits_from_file(username, repo_count)

    if all_commits is None:
        all_commits = []
        for repo in json_data:
            url = repo["commits_url"].removesuffix("{/sha}")
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

            except HTTPError as e:
                if response.status_code == 404:
                    print(f"❌ Commits URL '{url}' not found")
                elif response.status_code == 403:
                    print("⚠️ GitHub rate limit hit — wait an hour or use token")
                else:
                    print(f"API error {response.status_code}: {e}")
                continue  # Skip this repo instead of returning
                
            except RequestException as e:
                print(f"🌐 Network error: {e}")
                continue  # Skip this repo
                
            except ValueError as e:
                print(f"Invalid json from commit url and the error is {e}")
                continue  # Skip this repo

            # Validate that data is a list of commits
            if not isinstance(data, list):
                print(f"⚠️ Unexpected commit data format for {repo['name']}: {type(data)}")
                continue

            # Add repo name to each commit to preserve repo information
            for commit in data:
                if isinstance(commit, dict):  # Extra safety check
                    commit["repo_name"] = repo["name"]

            all_commits.extend(data)
            if len(data) > 0:
                print(f"✅ Fetched {len(data)} commits from {repo['name']}")
        
        save_commit_message_json(all_commits, username, repo_count)

    # Process commits to extract structured data
    commit_messages = []
    for commit in all_commits:
        try:
            # Parse the commit date
            commit_date = datetime.strptime(
                commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"
            )

            commit_info = {
                "repo_name": commit.get("repo_name", "unknown"),
                "author_name": commit["commit"]["author"]["name"],
                "message": commit["commit"]["message"],
                "date": commit["commit"]["author"]["date"],
                "hour": commit_date.hour,
                "day_of_week": commit_date.strftime("%A"),
                "month": commit_date.strftime("%B"),
            }
            commit_messages.append(commit_info)
        except (KeyError, ValueError) as e:
            print(f"Error processing commit: {e}")
            continue

    print(
        f"Processed {len(commit_messages)} commits from {len(set(c['repo_name'] for c in commit_messages))} repositories"
    )

    return commit_messages
