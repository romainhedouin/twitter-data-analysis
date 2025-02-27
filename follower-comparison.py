import json
import os

def extract_followers(file_path):
    """Extract follower profile URLs from a Twitter data file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().replace("window.YTD.follower.part0 = ", "").strip()

        # Ensure valid JSON by removing trailing semicolon
        if content.endswith(";"):
            content = content[:-1]

        try:
            followers = json.loads(content)
            return {f["follower"]["userLink"] for f in followers}
        except json.JSONDecodeError as e:
            print(f"JSON decoding error in {file_path}: {e}")
            return set()

def get_date_from_path(file_path):
    """Extracts the date from the file path (assumes format: data/YYYY-MM-DD/follower.js)."""
    return os.path.basename(os.path.dirname(file_path))  # Extracts 'YYYY-MM-DD'

def print_list(title, items):
    """Prints a list in a clean format, each item on a new line."""
    print(f"\n{title} ({len(items)}):\n" + "\n".join(items) if items else f"\n{title}: None")

# File paths (hardcoded for now)
file_old = "data/2025-02-18/follower.js"
file_new = "data/2025-02-27/follower.js"

# Extract followers from both files (now using URLs instead of IDs)
followers_old = extract_followers(file_old)
followers_new = extract_followers(file_new)

# Find gained and lost followers
gained_followers = followers_new - followers_old
lost_followers = followers_old - followers_new

# Get readable dates
date_old = get_date_from_path(file_old)
date_new = get_date_from_path(file_new)

# Print results cleanly
print_list(f"Followers gained between {date_old} → {date_new}", sorted(gained_followers))
print_list(f"Followers lost between {date_old} → {date_new}", sorted(lost_followers))
