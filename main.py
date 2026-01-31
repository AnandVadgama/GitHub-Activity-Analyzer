from collections import Counter
import requests
from requests.exceptions import RequestException, HTTPError, Timeout
from datetime import datetime, timedelta
import json
import glob
import os
import matplotlib.pyplot as plt


def fetch_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    try:
        data = requests.get(url)
        data.raise_for_status()

    except Timeout:
        print("⚠️ Request timed out — check your internet")
        return []

    except HTTPError as e:
        if data.status_code == 404:
            print(f"❌ Username '{username}' not found")

        elif data.status_code == 403:
            print("⚠️ GitHub rate limit hit — wait an hour or use token")

        else:
            print(f"API error {data.status_code}: {e}")

        return []

    except RequestException as e:
        print(f"🌐 Network error: {e}")
        return []
    try:
        json_data = data.json()

    except ValueError:
        print("❌ Invalid JSON from API")
        return []

    # Debug: Check if response is a list of repos
    if not isinstance(json_data, list):
        print(f"Unexpected API response format: {type(json_data)}")
        print(f"Response: {json_data}")
        return []

    return json_data


def extract_repo_info(json_data):
    repo_info = []
    try:
        for repo in json_data:
            try:
                repo_info.append(
                    {
                        "name": repo.get("name", "Unknown"),
                        "language": repo.get("language", "Unknown"),
                        "stars": repo.get("stargazers_count", 0),
                        "updated": repo.get("updated_at", ""),
                        "description": repo.get("description", "No description"),
                    }
                )
            except KeyError as e:
                print(f"the error: {e}")
    except KeyError as e:
        print(f"error of finding the key in the json data {e}")

    return repo_info


def analyze_languages(json_data):
    # Move your Counter logic here
    # Return: counts, max_language, python_percentage
    if not json_data:
        return Counter(), "No data", 0

    counts = Counter(repo["language"] for repo in json_data)
    if not counts:
        return Counter(), "No data", 0

    max_lang_used = max(counts, key=counts.get)
    # max_lang_used = counts.most_common(1)[0]

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
        try:
            dt = datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            months.append(dt.strftime("%B"))
            if dt > datetime.now() - timedelta(days=30):
                active_repos.append(repo["name"])
        except (KeyError, ValueError) as e:
            print(f"Error parsing date for repo {repo.get('name', 'unknown')}: {e}")
            continue

        months_counts = Counter(months)
    return months_counts, active_repos


def save_json(output):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"output_{timestamp}.json"
    try:
        with open(f"output/{file_name}", "w") as f:
            json.dump(output, f, indent=4)

    except (PermissionError, OSError) as e:
        print(f"❌ Couldn't save file: {e}")


def compare_repo():
    """
    Load prev analysis and compare that am i getting better ?
    gives you 2 recent files analysis
    """
    files = glob.glob("output/output_*.json")
    files.sort(reverse=True)

    if len(files) < 2:
        return "Need 2+ files"

    try:
        with open(files[0], "r") as f:
            current_data = json.load(f)
    except OSError as e:
        print(f"file is currupted or not found the error is {e}")
        return "Error loading current file"

    try:
        with open(files[1], "r") as f:
            older_data = json.load(f)
    except OSError as e:
        print(f"file is currupted or not found the error is {e}")
        return "Error loading older file"

    current_repos = len(current_data["repo_info"])
    older_repos = len(older_data["repo_info"])

    repo_growth = ((current_repos - older_repos) / older_repos) * 100

    return f"{repo_growth:+.1f}%"


def save_commit_message_json(all_commits, file_name="commit_message.json"):
    try:
        with open(file_name, "w") as f:
            json.dump(all_commits, f, indent=2)

    except FileNotFoundError as e:
        print(f"the error is : {e}")


def load_commits_from_file(file_name="commit_message.json"):
    if os.path.exists(file_name):
        try:
            with open(file_name) as f:
                all_commits = json.load(f)
            return all_commits
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading commit file: {e}")
            return None
    return None


def github_commit_extractor(json_data):
    all_commits = load_commits_from_file()

    if all_commits is None:
        all_commits = []
        for repo in json_data:
            url = repo["commits_url"].removesuffix("{/sha}")
            try:
                data = requests.get(url).json()

            except HTTPError as e:
                if data.status_code == 404:
                    print(f"❌ url '{url}' not found")

                elif data.status_code == 403:
                    print("⚠️ GitHub rate limit hit — wait an hour or use token")

                else:
                    print(f"API error {data.status_code}: {e}")
                return []
            except RequestException as e:
                print(f"🌐 Network error: {e}")
                return []
            except ValueError as e:
                print(f"Invalid json from commit url and the error is {e}")
                return []

            # Add repo name to each commit to preserve repo information
            for commit in data:
                commit["repo_name"] = repo["name"]

            all_commits.extend(data)
            if len(data) > 0:
                print(f"Sample commit from {repo['name']}:")
                print(
                    json.dumps(data[0], indent=2)
                )  # Print first commit to see structure
        save_commit_message_json(all_commits)

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


def github_commit_analyzer(commit_messages):
    # Convert commit messages to lowercase for analysis
    lower_split_msg = []
    for message in commit_messages:
        lm = (
            message["message"].lower().split()
        )  # Access the 'message' key and convert to lowercase
        lower_split_msg.extend(lm)

    # print(lower_split_msg)
    count_list = ["fixed", "upgraded", "added", "bug", "fix"]
    counts = Counter(lower_split_msg)

    count_words = {w: counts[w] for w in count_list}
    return count_words


def average_commit_per_repo(commit_messages):
    count_commits = Counter(commit["repo_name"] for commit in commit_messages)
    try:
        average_commit_per = sum(count_commits.values()) / len(count_commits)
    except ZeroDivisionError as e:
        print(f"No commits found for average calculation: {e}")
        return 0

    return average_commit_per


def most_active_time(commit_messages):
    hour = [commit["hour"] for commit in commit_messages]
    count_most_hour = Counter(hour)
    try:
        most_active_hour = max(count_most_hour, key=count_most_hour.get)
    except ValueError as e:
        print(f"No commit times found: {e}")
        return 12  # Default to noon

    return most_active_hour


def create_terminal_charts(counts, months_counts, commit_messages, repo_info):
    """Create ASCII/terminal-based charts"""
    print("\n" + "=" * 60)
    print("📊 TERMINAL-BASED VISUALIZATIONS".center(60))
    print("=" * 60)
    
    # 1. Language Distribution Bar Chart
    print("\n🔤 LANGUAGE DISTRIBUTION")
    print("-" * 40)
    if counts:
        max_count = max(counts.values())
        for lang, count in counts.most_common(5):
            if lang:  # Skip None values
                bar_length = int((count / max_count) * 30)
                bar = "█" * bar_length
                print(f"{lang:<12} {bar} {count}")
    
    # 2. Monthly Activity Chart
    print("\n📅 MONTHLY ACTIVITY")
    print("-" * 40)
    if months_counts:
        max_month = max(months_counts.values())
        for month, count in months_counts.most_common():
            bar_length = int((count / max_month) * 25)
            bar = "▓" * bar_length
            print(f"{month:<10} {bar} {count}")
    
    # 3. Commit Hour Pattern
    print("\n⏰ COMMIT HOUR PATTERN")
    print("-" * 40)
    if commit_messages:
        hour_counts = Counter(msg['hour'] for msg in commit_messages)
        max_hour = max(hour_counts.values()) if hour_counts else 1
        
        for hour in range(0, 24, 2):  # Show every 2 hours
            count = hour_counts.get(hour, 0)
            bar_length = int((count / max_hour) * 20)
            bar = "░" * bar_length
            time_str = f"{hour:02d}:00"
            print(f"{time_str} {bar} {count}")
    
    # 4. Top Repositories
    print("\n⭐ TOP REPOSITORIES BY STARS")
    print("-" * 40)
    if repo_info:
        sorted_repos = sorted(repo_info, key=lambda x: x['stars'], reverse=True)[:5]
        max_stars = max(repo['stars'] for repo in sorted_repos) if sorted_repos else 1
        
        for repo in sorted_repos:
            stars = repo['stars']
            bar_length = int((stars / max_stars) * 25) if max_stars > 0 else 0
            bar = "⭐" * min(bar_length, 25)  # Limit to 25 stars max
            print(f"{repo['name']:<20} {bar} {stars}")


def save_visual_charts(counts, months_counts, commit_messages, repo_info, username):
    """Create and save matplotlib charts as images"""
    
    # Create charts directory
    os.makedirs("charts", exist_ok=True)
    
    # Create a figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'GitHub Activity Analysis - {username}', fontsize=16, fontweight='bold')
    
    # 1. Language Distribution Pie Chart
    if counts and any(counts.values()):
        # Filter out None and empty languages
        filtered_counts = {k: v for k, v in counts.items() if k and k != 'Unknown'}
        if filtered_counts:
            languages = list(filtered_counts.keys())[:6]  # Top 6 languages
            values = list(filtered_counts.values())[:6]
            colors = plt.cm.Set3(range(len(languages)))
            
            ax1.pie(values, labels=languages, autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.set_title('Language Distribution', fontweight='bold')
        else:
            ax1.text(0.5, 0.5, 'No Language Data', ha='center', va='center')
            ax1.set_title('Language Distribution', fontweight='bold')
    
    # 2. Monthly Activity Bar Chart
    if months_counts:
        months = list(months_counts.keys())
        values = list(months_counts.values())
        bars = ax2.bar(months, values, color='skyblue', alpha=0.7)
        ax2.set_title('Monthly Repository Activity', fontweight='bold')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Number of Repositories')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(value), ha='center', va='bottom')
    else:
        ax2.text(0.5, 0.5, 'No Monthly Data', ha='center', va='center')
        ax2.set_title('Monthly Repository Activity', fontweight='bold')
    
    # 3. Commit Hour Heatmap/Histogram
    if commit_messages:
        hours = [msg['hour'] for msg in commit_messages]
        ax3.hist(hours, bins=24, range=(0, 24), color='lightcoral', alpha=0.7, edgecolor='black')
        ax3.set_title('Commit Hour Distribution', fontweight='bold')
        ax3.set_xlabel('Hour of Day')
        ax3.set_ylabel('Number of Commits')
        ax3.set_xticks(range(0, 24, 4))
        ax3.grid(True, alpha=0.3)
    else:
        ax3.text(0.5, 0.5, 'No Commit Data', ha='center', va='center')
        ax3.set_title('Commit Hour Distribution', fontweight='bold')
    
    # 4. Top Repositories by Stars
    if repo_info:
        sorted_repos = sorted(repo_info, key=lambda x: x['stars'], reverse=True)[:8]
        repo_names = [repo['name'][:15] + '...' if len(repo['name']) > 15 
                     else repo['name'] for repo in sorted_repos]
        stars = [repo['stars'] for repo in sorted_repos]
        
        bars = ax4.barh(repo_names, stars, color='gold', alpha=0.7)
        ax4.set_title('Top Repositories by Stars', fontweight='bold')
        ax4.set_xlabel('Stars')
        
        # Add value labels
        for bar, value in zip(bars, stars):
            ax4.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    str(value), ha='left', va='center')
    else:
        ax4.text(0.5, 0.5, 'No Repository Data', ha='center', va='center')
        ax4.set_title('Top Repositories by Stars', fontweight='bold')
    
    # Adjust layout and save
    plt.tight_layout()
    
    try:
        # Save as high-quality PNG
        chart_filename = f"charts/github_analysis_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"\n📊 Charts saved as: {chart_filename}")
        
        # Also save as PDF
        pdf_filename = chart_filename.replace('.png', '.pdf')
        plt.savefig(pdf_filename, bbox_inches='tight', facecolor='white')
        print(f"📊 Charts also saved as: {pdf_filename}")
        
    except Exception as e:
        print(f"❌ Error saving charts: {e}")
    
    # Don't show the plot in terminal, just save it
    plt.close()


def visualization(counts, months_counts, commit_messages, repo_info, username):
    """Main visualization function that creates both terminal and image charts"""
    
    # Create terminal-based visualizations
    create_terminal_charts(counts, months_counts, commit_messages, repo_info)
    
    # Create and save image-based visualizations
    save_visual_charts(counts, months_counts, commit_messages, repo_info, username)
    
    print("\n" + "=" * 60)
    print("✅ VISUALIZATION COMPLETE".center(60))
    print("=" * 60)


def display_analysis(
    repo_info,
    counts,
    months_counts,
    per_py,
    active_repos,
    max_lang_used,
    count_words,
    average_commit_per,
    most_active_hour,
):
    print("\n" + "=" * 60)
    print("📊 GITHUB ACTIVITY ANALYSIS".center(60))
    print("=" * 60)

    # Section headers:
    def print_section(title):
        print(f"\n{title}")
        print("-" * 60)

    # Your logic goes here:
    print_section("📂 REPOSITORY OVERVIEW")
    # YOUR CODE: print total repos, languages, etc
    print(f"Total Repos : {len(repo_info)}")
    print(f"Most Used Programming Language : {max_lang_used}")

    print_section("⭐ TOP REPOSITORIES")
    # YOUR CODE: sort and print top repos
    sorted_lst = sorted(repo_info, key=lambda x: x["stars"], reverse=True)[:5]

    print(f"Most Stared Repos : {sorted_lst}")

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

    print_section("Most Used Words in the Commit messeges")
    print(count_words)

    print_section("Average Commit Per Repository ")
    print(average_commit_per)

    print_section("Most Active Time for Commiting All over")
    if most_active_hour > 12:
        print(f"{most_active_hour} PM")
    else:
        print(f"{most_active_hour} AM")

    print("\n" + "=" * 60 + "\n")


def main():
    username = input("Enter the name of the user you want analyse github profile")
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
    count_words = github_commit_analyzer(commit_messages=commit_data)
    average_commit_per = average_commit_per_repo(commit_messages=commit_data)
    most_active_hour = most_active_time(commit_data)
    display_analysis(
        repo_info,
        counts,
        months_counts,
        per_py,
        active_repos,
        max_lang_used,
        count_words,
        average_commit_per,
        most_active_hour,
    )
    
    # Create visualizations
    visualization(counts, months_counts, commit_data, repo_info, username)

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
    # save_json(output)
