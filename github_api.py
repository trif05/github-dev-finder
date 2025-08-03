import requests
from datetime import datetime

GITHUB_TOKEN = "YOUR_GITHUB_API_TOKEN"  
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

#Phase 1 
def get_user_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        print("Response text:", response.text)
        raise Exception("GitHub API error:", response.status_code)


def get_user_repos(username):
    url_repos = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url_repos, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        print("Response text:", response.text)
        raise Exception("GitHub API error:", response.status_code)


def get_repo_languages(username, repo_name):
    url_language = f"https://api.github.com/repos/{username}/{repo_name}/languages"
    response = requests.get(url_language, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        print("Response text:", response.text)
        raise Exception("GitHub API error:", response.status_code)


def get_user_languages_summary(username):
    total_languages = {}
    repos = get_user_repos(username)
    if repos is None:
        return None

    for repo in repos:
        repo_name = repo["name"]
        languages = get_repo_languages(username, repo_name)
        if languages is None:
            continue
        for language, bytes_count in languages.items():
            if language in total_languages:
                total_languages[language] += bytes_count
            else:
                total_languages[language] = bytes_count

    return total_languages

#Phase 2 (User events)
# Construct the GitHub API URL for user events
# This endpoint returns the last 90 public events for a user
def get_user_events(username):
    url_events=f"https://api.github.com/users/{username}/events"
    events = requests.get(url_events, headers=HEADERS)
    # Make HTTP GET request to GitHub API with authentication headers
    # HEADERS contains our GitHub token for API access

    if events.status_code == 200:
        raw_events=events.json()
        filtered_events=[]
        for event in raw_events:
            filtered_event = {
                "type": event["type"],
                "created_at": event["created_at"], 
                "repo_name": event["repo"]["name"]
            }
            filtered_events.append(filtered_event)
        return filtered_events  

    elif events.status_code == 404:
        return None
    else:
        print("Response text:", events.text)
        raise Exception("GitHub API error:", events.status_code)
    
def analyze_user_event_types(username):
    # Call get_user_events() to fetch filtered event data
    # This returns a list of dictionaries: [{"type": "WatchEvent", "created_at": "...", "repo_name": "..."}]
    events = get_user_events(username) # This is returning filtered_events
    # Initialize empty dictionary to store our counts
    # Key = event type (string), Value = count (integer)
    # Example result: {"WatchEvent": 5, "PushEvent": 12, "CreateEvent": 2}
    event_counter={}
    if events is None:
        return None
    for event in events:
        event_type=event["type"]
        # Check if we've seen this event type before.
        # This is the counting logic
        if event_type in event_counter:
            event_counter[event_type] += 1
        else:
            event_counter[event_type] = 1 
    return event_counter    


def get_user_event_createdat(username):
    events = get_user_events(username) 
    #Παίρνω τα filtered events από τη function που φτιάξαμε
    #Δημιουργώ dictionary με 3 κενά sub-dictionaries για counting
    time_counter={
        "hours": {},
        "days": {},
        "months": {}
    }
    if events is None or len(events) == 0:
        return None
    # παίρνω το timestamp από κάθε event
    for event in events:
        event_timestamp=event["created_at"] #2025-07-05T01:46:53Z
        dt = datetime.fromisoformat(event_timestamp.replace('Z', '+00:00')) # Μετατρέπω string σε datetime object/Αλλάζω "Z" σε "+00:00" (GitHub format → Python format)
        hour = dt.hour
        day_name = dt.strftime('%A')  #%A = Full day name format
        month_name = dt.strftime('%B') #%B = Full month name format
        if hour in time_counter["hours"]:
            time_counter["hours"][hour] += 1
        else:
            time_counter["hours"][hour] = 1 
        if day_name in time_counter["days"]:
            time_counter["days"][day_name] += 1
        else:
            time_counter["days"][day_name] = 1 
        if month_name in time_counter["months"]:
            time_counter["months"][month_name] += 1
        else:
            time_counter["months"][month_name] = 1
    return time_counter


    
def calculate_event_stats(username):
    event_types = analyze_user_event_types(username)    # {"PushEvent": 15, "WatchEvent": 7}
    time_data = get_user_event_createdat(username)      # {"hours": {14: 8, 18: 5}, "days": {...}}
    
    if event_types is None or time_data is None:
        return None
    #=================================================Data-Calculation================================================
    # Basic max values
    most_common_event = max(event_types, key=event_types.get)           # "PushEvent"
    max_event_count = max(event_types.values())                        # 15
    most_active_hour = max(time_data["hours"], key=time_data["hours"].get)     # 14
    most_active_day = max(time_data["days"], key=time_data["days"].get)        # "Saturday"
    most_active_month = max(time_data["months"], key=time_data["months"].get)  # "July"
    
    # Calculate totals and percentages
    total_events = sum(event_types.values())
    total_weekend = time_data["days"].get("Saturday", 0) + time_data["days"].get("Sunday", 0)
    total_weekday = sum(time_data["days"].get(day, 0) for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    
    # Event type percentages
    push_percentage = event_types.get("PushEvent", 0) / total_events * 100 if total_events > 0 else 0
    watch_percentage = event_types.get("WatchEvent", 0) / total_events * 100 if total_events > 0 else 0
    create_percentage = event_types.get("CreateEvent", 0) / total_events * 100 if total_events > 0 else 0
    issues_percentage = event_types.get("IssuesEvent", 0) / total_events * 100 if total_events > 0 else 0
    pr_percentage = event_types.get("PullRequestEvent", 0) / total_events * 100 if total_events > 0 else 0
    
    # Weekend percentage
    weekend_percentage = total_weekend / total_events * 100 if total_events > 0 else 0
    weekday_percentage = total_weekday / total_events * 100 if total_events > 0 else 0
    
    # Mid-week activity (Tuesday-Thursday)
    midweek_activity = sum(time_data["days"].get(day, 0) for day in ["Tuesday", "Wednesday", "Thursday"])
    
    # Time-specific activity counts
    midnight_activity = sum(time_data["hours"].get(hour, 0) for hour in [0, 1, 2, 3])
    coffee_hour_activity = sum(time_data["hours"].get(hour, 0) for hour in [9, 10, 11])
    lunch_activity = sum(time_data["hours"].get(hour, 0) for hour in [12, 13, 14])
    after_hours_activity = sum(time_data["hours"].get(hour, 0) for hour in range(18, 24))
    #===================================================================================================================
    # --- DEVELOPER TYPE LOGIC (Time-based) ---
    if most_active_hour in [0, 1, 2, 3, 4, 5]:
        developer_type = "Night Owl"
    elif most_active_hour in [6, 7, 8]:
        developer_type = "Early Bird"
    elif most_active_hour in [9, 10, 11, 12, 13, 14, 15, 16, 17]:
        developer_type = "9-to-5 Developer"
    elif most_active_hour in [18, 19, 20, 21]:
        developer_type = "Evening Coder"
    elif most_active_hour in [22, 23]:
        developer_type = "Late Night Coder"
    else:
        developer_type = "Varied Schedule"
    
    # --- DAY PATTERNS ---
    if weekend_percentage >= 50:
        day_pattern = "Weekend Warrior"
    elif weekday_percentage >= 80:
        day_pattern = "Weekday Focused"
    elif most_active_day in ["Tuesday", "Wednesday", "Thursday"]:
        day_pattern = "Mid-week Crusher"
    elif most_active_day == "Monday":
        day_pattern = "Monday Starter"
    elif most_active_day == "Friday":
        day_pattern = "Friday Finisher"
    else:
        day_pattern = "Balanced Schedule"
    
    # --- ACTIVITY LEVEL CATEGORIES ---
    if total_events >= 50:
        activity_level = "Coding Machine"
    elif total_events >= 20:
        activity_level = "Steady Developer"
    elif total_events >= 5:
        activity_level = "Casual Contributor"
    else:
        activity_level = "Occasional Coder"
    
    # --- EVENT TYPE DISTRIBUTION ---
    if push_percentage >= 70:
        event_style = "Heavy Committer"
    elif watch_percentage + issues_percentage >= 50:
        event_style = "Community Contributor"
    elif create_percentage >= 30:
        event_style = "Project Creator"
    elif pr_percentage >= 30:
        event_style = "Collaborator"
    elif issues_percentage >= 30:
        event_style = "Issue Hunter"
    else:
        event_style = "Balanced Contributor"
    
    # --- ENGAGEMENT LEVELS ---
    if watch_percentage >= 40:
        engagement_type = "GitHub Explorer"
    elif push_percentage >= 80 and len(set(event_types.keys())) <= 2:
        engagement_type = "Solo Developer"
    elif pr_percentage + issues_percentage >= 40:
        engagement_type = "Team Player"
    else:
        engagement_type = "Independent Developer"
    
    # --- SPECIAL/FUN PATTERNS ---
    special_pattern = None
    if midnight_activity >= total_events * 0.3:
        special_pattern = "Midnight Debugger"
    elif coffee_hour_activity >= total_events * 0.3:
        special_pattern = "Coffee Hour Coder"
    elif lunch_activity >= total_events * 0.25:
        special_pattern = "Lunch Break Builder"
    elif after_hours_activity >= total_events * 0.4:
        special_pattern = "After Hours Hacker"
    elif weekend_percentage >= 60:
        special_pattern = "Weekend Wizard"
    
    # --- RETURN COMPREHENSIVE STATS, Επιστρέφει ένα μεγάλο dictionary με όλα τα analysis results ---
    return {
        "total_events": total_events,
        "most_active_hour": most_active_hour,
        "most_active_day": most_active_day,
        "most_active_month": most_active_month,
        "most_common_event": most_common_event,
        "developer_type": developer_type,
        "day_pattern": day_pattern,
        "activity_level": activity_level,
        "event_style": event_style,
        "engagement_type": engagement_type,
        "special_pattern": special_pattern,
        "percentages": {
            "weekend": round(weekend_percentage, 1),
            "weekday": round(weekday_percentage, 1),
            "push_events": round(push_percentage, 1),
            "watch_events": round(watch_percentage, 1),
            "create_events": round(create_percentage, 1),
            "issues_events": round(issues_percentage, 1),
            "pr_events": round(pr_percentage, 1)
        }
    }
