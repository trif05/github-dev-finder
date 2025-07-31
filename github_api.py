import requests
from datetime import datetime

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}


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

def get_user_events(username):
    url_events=f"https://api.github.com/users/{username}/events"
    events = requests.get(url_events, headers=HEADERS)

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
    events = get_user_events(username) # Αυτο μας επιστρεφει filtered_events
    event_counter={}
    if events is None:
        return None
    for event in events:
        event_type=event["type"]
        if event_type in event_counter:
            event_counter[event_type] += 1  # Υπάρχει ήδη, πρόσθεσε 1
        else:
            event_counter[event_type] = 1 
    return event_counter    


def get_user_event_createdat(username):
    events = get_user_events(username)
    time_counter={
        "hours": {},
        "days": {},
        "months": {}
    }
    if events is None:
        return None
    for event in events:
        event_type=event["created_at"] #2025-07-05T01:46:53Z
        dt = datetime.fromisoformat(event_type.replace('Z', '+00:00'))
        hour = dt.hour
        day_name = dt.strftime('%A')  
        month_name = dt.strftime('%B')


    
def calculate_event_stats(username):
    pass