from collections import Counter
from datetime import datetime, timedelta


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
