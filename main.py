from collections import Counter
from datetime import datetime
import json

# Import from our modular files
from github_api import fetch_github_repos, github_commit_extractor
from data_analyzer import analyze_languages, analyze_activity, extract_repo_info, github_commit_analyzer
from file_handler import save_json, compare_repo
from utils import average_commit_per_repo, most_active_time
from visualizations import visualize_data


def main():
    username = input("Enter the username to analyze: ")
    
    # Fetch repository data
    json_data = fetch_github_repos(username)
    if not json_data:
        print("⚠️ No data available - exiting")
        return None

    # Extract and analyze repository information
    repo_info = extract_repo_info(json_data)
    counts, max_lang_used, per_py = analyze_languages(json_data)
    months_counts, active_repos = analyze_activity(json_data)
    
    # Analyze commit data
    commit_data = github_commit_extractor(json_data, username)
    count_words = github_commit_analyzer(commit_messages=commit_data)
    average_commit_per = average_commit_per_repo(commit_messages=commit_data)
    most_active_hour = most_active_time(commit_data)
    
    # Create comprehensive analysis and visualizations (includes text summary, terminal charts, and image charts)
    visualize_data(counts, months_counts, commit_data, repo_info, username,
                  per_py, active_repos, max_lang_used, count_words, average_commit_per, most_active_hour)

    # Return analysis data for JSON export
    return {
        "username": username,
        "repo_info": repo_info,
        "language_counts": dict(counts),
        "most_used_language": max_lang_used,
        "python_percentage": per_py,
        "monthly_activity": dict(months_counts),
        "active_repos": active_repos,
        "words_pattern": count_words,
        "average_commit_percentage": average_commit_per,
        "most_active_hour": most_active_hour,
    }


if __name__ == "__main__":
    output = main()
    if output:
        save_json(output)