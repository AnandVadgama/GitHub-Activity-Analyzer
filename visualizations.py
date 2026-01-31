import os
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from file_handler import compare_repo


def display_analysis_summary(repo_info, counts, months_counts, per_py, active_repos, 
                            max_lang_used, count_words, average_commit_per, most_active_hour):
    """Display comprehensive text-based analysis summary"""
    print("\n" + "=" * 60)
    print("📊 GITHUB ACTIVITY ANALYSIS".center(60))
    print("=" * 60)

    def print_section(title):
        print(f"\n{title}")
        print("-" * 60)

    print_section("📂 REPOSITORY OVERVIEW")
    print(f"Total Repos : {len(repo_info)}")
    print(f"Most Used Programming Language : {max_lang_used}")

    print_section("⭐ TOP REPOSITORIES")
    sorted_lst = sorted(repo_info, key=lambda x: x["stars"], reverse=True)[:5]
    for i, repo in enumerate(sorted_lst, 1):
        print(f"{i}. {repo['name']} - ⭐{repo['stars']} stars")

    print_section("📈 LANGUAGE BREAKDOWN")
    print(f"Languages Used Across all Repos : {dict(counts)}")
    print(f"Percentage of Python Used across all Repos : {per_py}%")

    print_section("📅 MONTHLY ACTIVITY")
    print(f"Monthly Activity : {dict(months_counts)}")

    print_section("🚀 RECENT ACTIVITY (30 days)")
    print(f"Most Recent Active Repos: {active_repos}")

    print_section("📈 REPOSITORY GROWTH")
    print(compare_repo())

    print_section("🔤 COMMIT MESSAGE ANALYSIS")
    print(f"Most Used Words in Commit Messages: {count_words}")

    print_section("📊 COMMIT STATISTICS")
    print(f"Average Commits Per Repository: {average_commit_per:.2f}")

    print_section("⏰ PEAK ACTIVITY TIME")
    if most_active_hour > 12:
        print(f"Most Active Hour: {most_active_hour}:00 PM")
    else:
        print(f"Most Active Hour: {most_active_hour}:00 AM")

    print("\n" + "=" * 60 + "\n")


def create_terminal_charts(counts, months_counts, commit_messages, repo_info):
    """Create ASCII/terminal-based charts"""
    print("\n" + "=" * 60)
    print("📊 TERMINAL-BASED VISUALIZATIONS".center(60))
    print("=" * 60)
    
    # Helper function to create bars
    def make_bar(value, max_value, symbol="█", max_length=30):
        if max_value == 0:
            return ""
        bar_length = int((value / max_value) * max_length)
        return symbol * bar_length
    
    # Language Distribution
    if counts:
        print("\n🔤 LANGUAGE DISTRIBUTION")
        print("-" * 40)
        max_count = max(counts.values())
        for lang, count in counts.most_common(5):
            if lang and lang != "Unknown":
                bar = make_bar(count, max_count)
                print(f"{lang:<12} {bar} {count}")
    
    # Monthly Activity
    if months_counts:
        print("\n📅 MONTHLY ACTIVITY")
        print("-" * 40)
        max_month = max(months_counts.values())
        for month, count in months_counts.most_common():
            bar = make_bar(count, max_month, "▓", 25)
            print(f"{month:<10} {bar} {count}")
    
    # Commit Hours (simplified - show peak hours only)
    if commit_messages:
        print("\n⏰ PEAK COMMIT HOURS")
        print("-" * 40)
        hour_counts = Counter(msg['hour'] for msg in commit_messages)
        max_hour = max(hour_counts.values()) if hour_counts else 1
        
        # Show only hours with activity
        for hour, count in hour_counts.most_common(6):
            bar = make_bar(count, max_hour, "▒", 20)
            time_str = f"{hour:02d}:00"
            print(f"{time_str} {bar} {count}")
    
    # Top Repos
    if repo_info:
        print("\n⭐ TOP REPOSITORIES")
        print("-" * 40)
        sorted_repos = sorted(repo_info, key=lambda x: x['stars'], reverse=True)[:5]
        if sorted_repos:
            max_stars = max(repo['stars'] for repo in sorted_repos)
            for repo in sorted_repos:
                stars = repo['stars']
                star_display = "⭐" * min(int(stars/max(max_stars/10, 1)), 10) if max_stars > 0 else ""
                print(f"{repo['name']:<20} {star_display} {stars}")


def create_image_charts(counts, months_counts, commit_messages, repo_info, username):
    """Create and save matplotlib charts"""
    os.makedirs("charts", exist_ok=True)
    
    # Create figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'GitHub Activity Analysis - {username}', fontsize=16, fontweight='bold')
    
    # 1. Language Pie Chart
    if counts and any(counts.values()):
        filtered_counts = {k: v for k, v in counts.items() if k and k != 'Unknown'}
        if filtered_counts:
            languages, values = zip(*list(filtered_counts.items())[:6])
            ax1.pie(values, labels=languages, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Language Distribution', fontweight='bold')
        else:
            ax1.text(0.5, 0.5, 'No Language Data', ha='center', va='center')
    else:
        ax1.text(0.5, 0.5, 'No Language Data', ha='center', va='center')
    ax1.set_title('Language Distribution', fontweight='bold')
    
    # 2. Monthly Activity
    if months_counts:
        months, values = zip(*months_counts.items())
        bars = ax2.bar(months, values, color='skyblue', alpha=0.7)
        ax2.set_title('Monthly Activity', fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        # Add value labels
        for bar, value in zip(bars, values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(value), ha='center', va='bottom')
    else:
        ax2.text(0.5, 0.5, 'No Monthly Data', ha='center', va='center')
    ax2.set_title('Monthly Activity', fontweight='bold')
    
    # 3. Commit Hours
    if commit_messages:
        hours = [msg['hour'] for msg in commit_messages]
        ax3.hist(hours, bins=24, range=(0, 24), color='lightcoral', alpha=0.7)
        ax3.set_title('Commit Hours', fontweight='bold')
        ax3.set_xticks(range(0, 24, 4))
    else:
        ax3.text(0.5, 0.5, 'No Commit Data', ha='center', va='center')
    ax3.set_title('Commit Hours', fontweight='bold')
    
    # 4. Top Repos
    if repo_info:
        sorted_repos = sorted(repo_info, key=lambda x: x['stars'], reverse=True)[:8]
        repo_names = [repo['name'][:15] + '...' if len(repo['name']) > 15 
                     else repo['name'] for repo in sorted_repos]
        stars = [repo['stars'] for repo in sorted_repos]
        
        ax4.barh(repo_names, stars, color='gold', alpha=0.7)
        ax4.set_title('Top Repositories', fontweight='bold')
    else:
        ax4.text(0.5, 0.5, 'No Repository Data', ha='center', va='center')
    ax4.set_title('Top Repositories', fontweight='bold')
    
    # Save
    plt.tight_layout()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"charts/github_analysis_{username}_{timestamp}.png"
    
    try:
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"\n📊 Charts saved as: {filename}")
    except Exception as e:
        print(f"❌ Error saving: {e}")
    
    plt.close()


def visualize_data(counts, months_counts, commit_messages, repo_info, username, 
                  per_py=0, active_repos=None, max_lang_used="Unknown", 
                  count_words=None, average_commit_per=0, most_active_hour=12):
    """Main function - creates comprehensive analysis with text summary, terminal and image visualizations"""
    
    # 1. Display comprehensive analysis summary
    display_analysis_summary(repo_info, counts, months_counts, per_py, active_repos or [], 
                            max_lang_used, count_words or {}, average_commit_per, most_active_hour)
    
    # 2. Create terminal-based charts  
    create_terminal_charts(counts, months_counts, commit_messages, repo_info)
    
    # 3. Create and save image charts
    create_image_charts(counts, months_counts, commit_messages, repo_info, username)
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE ANALYSIS & VISUALIZATION FINISHED".center(60))
    print("=" * 60)