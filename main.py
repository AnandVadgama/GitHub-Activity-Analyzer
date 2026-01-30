from collections import Counter
import requests
from datetime import datetime, timedelta
import json
import glob
import os

def fetch_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    data = requests.get(url)
    
    if data.status_code != 200:
        print(f"API Error: {data.status_code}")
        print(f"Response: {data.text}")
        return []
    
    json_data = data.json()
    
    # Debug: Check if response is a list of repos
    if not isinstance(json_data, list):
        print(f"Unexpected API response format: {type(json_data)}")
        print(f"Response: {json_data}")
        return []
    
    return json_data

def extract_repo_info(json_data):
    repo_info = [
        {'name' : repo['name'],
        'language' : repo["language"],
        'stars' : repo['stargazers_count'],
        'updated' : repo['updated_at'],
        'description' : repo['description']}
        for repo in json_data
    ]
    return repo_info

def analyze_languages(json_data):
    # Move your Counter logic here
    # Return: counts, max_language, python_percentage
    if not json_data:
        return Counter(), "No data", 0
        
    counts = Counter(repo['language'] for repo in json_data)
    if not counts:
        return Counter(), "No data", 0
        
    max_lang_used_2 = max(counts, key=counts.get)
    max_lang_used = counts.most_common(1)

    python_count = counts.get("Python", 0)
    total_count = sum(counts.values())
    per_py = (python_count * 100 / total_count) if total_count > 0 else 0
        
    return counts, max_lang_used, round(per_py, 4)

def analyze_activity(json_data):
    # Move your datetime logic here
    # Return: months_counts, active_repos list
    if not json_data:
        return Counter(), []
        
    months = []
    active_repos = []
    for repo in json_data:
        dt = datetime.strptime(repo['pushed_at'],"%Y-%m-%dT%H:%M:%SZ")
        months.append(dt.strftime("%B"))
        if dt > datetime.now() - timedelta(days=30):
                active_repos.append(repo["name"])

        months_counts = Counter(months)
    return months_counts, active_repos

def save_json(output):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"output_{timestamp}.json"
    with open(f"output/{file_name}", "w") as f:
        json.dump(output, f, indent=4)

def compare_repo():
    """
    Load prev analysis and compare that am i getting better ?
    gives you 2 recent files analysis
    """
    files = glob.glob("output/output_*.json")
    files.sort(reverse=True)
    
    if len(files) < 2:
        return "Need 2+ files"

    with open(files[0], 'r') as f:
        current_data = json.load(f)
    with open(files[1], 'r') as f:
        older_data = json.load(f)

    current_repos = len(current_data['repo_info'])
    older_repos = len(older_data['repo_info'])

    repo_growth = ((current_repos - older_repos)/older_repos) * 100

    return f"{repo_growth:+.1f}%"

def save_commit_message_json(all_commits, file_name= "commit_message.json"):
    with open(file_name, "w") as f:
        json.dump(all_commits, f, indent=2)
    

def load_commits_from_file(file_name="commit_message.json"):
    if os.path.exists(file_name):
        with open(file_name) as f:
            all_commits = json.load(f)
            return all_commits

def github_commit_extractor(json_data):
    
    all_commits = load_commits_from_file()

    if all_commits is None:
        all_commits = []
        for repo in json_data:
            url = repo["commits_url"].removesuffix("{/sha}")
            data = requests.get(url).json()

            # Add repo name to each commit to preserve repo information
            for commit in data:
                commit['repo_name'] = repo['name']
            
            all_commits.extend(data)
            if len(data) > 0:
                print(f"Sample commit from {repo['name']}:")
                print(json.dumps(data[0], indent=2)) # Print first commit to see structure
        save_commit_message_json(all_commits)
    
    # Process commits to extract structured data
    commit_messages = []
    for commit in all_commits:
        try:
            # Parse the commit date
            commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
            
            commit_info = {
                "repo_name": commit.get('repo_name', 'unknown'),
                "author_name": commit["commit"]["author"]["name"],
                "message": commit["commit"]["message"], 
                "date": commit["commit"]["author"]["date"],
                "hour": commit_date.hour,
                "day_of_week": commit_date.strftime("%A"),
                "month": commit_date.strftime("%B")
            }
            commit_messages.append(commit_info)
        except (KeyError, ValueError) as e:
            print(f"Error processing commit: {e}")
            continue
    
    print(f"Processed {len(commit_messages)} commits from {len(set(c['repo_name'] for c in commit_messages))} repositories")

    return commit_messages

def github_commit_analyzer(commit_messages):
    # Convert commit messages to lowercase for analysis
    lower_split_msg = []
    for message in commit_messages:
        lm = message['message'].lower().split()  # Access the 'message' key and convert to lowercase
        lower_split_msg.extend(lm)
    
    # print(lower_split_msg)
    count_list = ["fixed", "upgraded", "added", "bug", "fix"]
    counts = Counter(lower_split_msg)

    count_words = {w: counts[w] for w in count_list}
    return count_words

def average_commit_per_repo(commit_messages):
    count_commits = Counter(commit["repo_name"] for commit in commit_messages)
    average_commit_per = ( sum(count_commits.values()) / len(count_commits ) )
    return average_commit_per

def most_active_time(commit_messages):
    hour = [commit["hour"] for commit in commit_messages]
    count_most_hour = Counter(hour)
    most_active_hour = max(count_most_hour, key= count_most_hour.get)
    return most_active_hour
    


def display_analysis(repo_info, counts, months_counts, per_py, active_repos, max_lang_used):
    print("\n" + "="*60)
    print("📊 GITHUB ACTIVITY ANALYSIS".center(60))
    print("="*60)
    
    # Section headers:
    def print_section(title):
        print(f"\n{title}")
        print("-"*60)
    
    # Your logic goes here:
    print_section("📂 REPOSITORY OVERVIEW")
    # YOUR CODE: print total repos, languages, etc
    print(f"Total Repos : {len(repo_info)}")
    print(f"Most Used Programming Language : {max_lang_used}")


    
    print_section("⭐ TOP REPOSITORIES")
    # YOUR CODE: sort and print top repos
    print(f"Most Stared Repos : {sorted(repo_info, key=lambda x : x['stars'], reverse=True)[:5]}")
    
    print_section("📈 LANGUAGE BREAKDOWN")
    # YOUR CODE: print language percentages
    print(f"Languages Used Across all Repos : {counts}")
    print(f"Percentage of Python Used in across all Repos : {per_py}")
    
    print_section("📅 MONTHLY ACTIVITY")
    # YOUR CODE: print months data
    print(f"Monthly Activity : {months_counts}")
    
    print_section("🚀 RECENT ACTIVITY (30 days)")
    # YOUR CODE: print active repos
    print(f"Most Recent Active Repos: {active_repos}")

    print_section("Repo change 📈 or 📉 or 0%")
    print(compare_repo())
    
    print("\n" + "="*60 + "\n")

def main():
    username = "AnandVadgama"
    # Call all functions in order
    # Pass data between them
    json_data = fetch_github_repos(username)
    
    if not json_data:
        print("⚠️  No data available - using existing analysis files only")
        return None
        
    repo_info = extract_repo_info(json_data)
    counts, max_lang_used, per_py = analyze_languages(json_data)
    months_counts, active_repos = analyze_activity(json_data)
    commit_data = github_commit_extractor(json_data)  # Skip to avoid more API calls
    github_commit_analyzer(commit_messages=commit_data)
    average_commit_per_repo(commit_messages=commit_data)
    most_active_time(commit_data)
    display_analysis(repo_info, counts, months_counts, per_py, active_repos, max_lang_used)
    
    # Return analysis data for JSON export
    return {
        "username": username,
        "repo_info": repo_info,
        "language_counts": dict(counts),
        "most_used_language": max_lang_used,
        "python_percentage": per_py,
        "monthly_activity": dict(months_counts),
        "active_repos": active_repos
    }

if __name__ == "__main__": 
    output = main()
    # save_json(output)
    

