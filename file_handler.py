from datetime import datetime
import os
import json
from glob import glob


def compare_repo():
    """
    Load prev analysis and compare that am i getting better ?
    gives you 2 recent files analysis
    """
    files = glob("output/output_*.json")
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


def save_json(output):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"output_{timestamp}.json"
    try:
        with open(f"output/{file_name}", "w") as f:
            json.dump(output, f, indent=4)

    except (PermissionError, OSError) as e:
        print(f"❌ Couldn't save file: {e}")

def save_commit_message_json(all_commits, username, repo_count):
    """Save commits with user-specific filename and metadata"""
    file_name = f"commit_message_{username}.json"
    cache_data = {
        "username": username,
        "repo_count": repo_count,
        "cached_at": datetime.now().isoformat(),
        "commits": all_commits
    }
    
    try:
        with open(file_name, "w") as f:
            json.dump(cache_data, f, indent=2)
        print(f"💾 Saved {len(all_commits)} commits to {file_name}")
    except FileNotFoundError as e:
        print(f"❌ Error saving cache: {e}")


def load_commits_from_file(username, repo_count):
    """Load commits with validation for user and repo count"""
    file_name = f"commit_message_{username}.json"
    
    if not os.path.exists(file_name):
        print(f"📂 No cache found for {username}")
        return None
        
    try:
        with open(file_name) as f:
            cache_data = json.load(f)
            
        # Validate cache data structure
        if not isinstance(cache_data, dict) or "commits" not in cache_data:
            print(f"⚠️ Invalid cache format for {username}, refreshing...")
            return None
            
        # Validate username matches
        if cache_data.get("username") != username:
            print(f"⚠️ Username mismatch in cache, refreshing...")
            return None
            
        # Validate repo count (allow some flexibility for minor changes)
        cached_repo_count = cache_data.get("repo_count", 0)
        if abs(cached_repo_count - repo_count) > 5:  # Allow 5 repo difference
            print(f"📊 Repo count changed significantly ({cached_repo_count} → {repo_count}), refreshing...")
            return None
            
        cached_at = cache_data.get("cached_at", "")
        print(f"✅ Using cached commits for {username} (cached: {cached_at})")
        return cache_data["commits"]
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error loading cache for {username}: {e}")
        return None