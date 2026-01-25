from collections import Counter
import requests
from datetime import datetime, timedelta
import json
import glob

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
    filename = f"output_{timestamp}.json"
    with open(f"output/{filename}", "w") as f:
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


#     files_lst = files[:num]
#     all_data = []
#     for file in files_lst:
#         with open(file, "r") as f:
#             data = json.load(f)
#             all_data.append(data)
        
    
    
#     if len(files_lst) == len(set(files_lst)):
#         print("no new repos found")

#     else:
#         print("new repos found")

#     print(files_lst)

def github_commit_analyzer(json_data):
    all_commits = []

    for repo in json_data:
        url = repo["commits_url"].removesuffix("{/sha}")
        data = requests.get(url).json()
        all_commits.extend(data)
        break
        
    
        # print(all_commits)
        
    
    commit_message =[]
    for commit in all_commits:
        msg = commit["commit"]["message"]
        print(msg)
        commit_message.extend(msg)
        break
    print(commit_message)
    

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
    github_commit_analyzer(json_data)  # Skip to avoid more API calls
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

