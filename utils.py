from collections import Counter


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