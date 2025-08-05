import requests
from datetime import datetime
from datetime import timedelta
from collections import defaultdict

#this token have access to : public repos, public user profiles, repository languages, public events.
GITHUB_TOKEN = "YOUR_GITHUB_API_TOKEN"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

#Function for getting user data.Username is a string with user data.
def get_user_data(username):
    #Here we create the url for the github api.
    url = f"https://api.github.com/users/{username}"
    #Here we make a http get request to the github api .
    response = requests.get(url, headers=HEADERS)
    #Here is the error handling for the reqest.
    if response.status_code == 200: #If the request is successful, we return the json data.
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        print("Response text:", response.text)
        #Here if the request is not successfull we raise an exception.
        raise Exception("GitHub API error:", response.status_code)

#Function for getting user repos.
def get_user_repos(username):
    url_repos = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url_repos, headers=HEADERS)
    #Error handling for the reqests.
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        print("Response text:", response.text)
        #Exeption for the error handling.
        raise Exception("GitHub API error:", response.status_code)

#Function for getting the languages of a repo.
def get_repo_languages(username, repo_name):
    #Here we gather access to the languages of a repo.We update the url adding {repo_name}/languages
    url_language = f"https://api.github.com/repos/{username}/{repo_name}/languages"
    response = requests.get(url_language, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        print("Response text:", response.text)
        #Exeption for the error handling.
        raise Exception("GitHub API error:", response.status_code)

#Function of getting uses's languages 
def get_user_languages_summary(username):
    #We create a dictionary to store the languages and bytes count.
    total_languages = {}
    #Here we take the repos of the user.
    repos = get_user_repos(username)
    #We check if the repos are none.
    if repos is None:
        return None
    #Loops throught the repos and take the language of each repo.
    for repo in repos:
        #Name of the repo
        repo_name = repo["name"]
        #Languages of the repo using the function for each one repo.
        languages = get_repo_languages(username, repo_name)
        #if the languages are none we move to the next repo using continue.
        if languages is None:
            continue
        #Loops throug the languages and bytes count.(Counting algorithm)
        #.Item() method is for returning the key and valuse of dictionary as tuple.
        for language, bytes_count in languages.items():
            #if the language is already in the dictionary we jsut add the bytes.
            if language in total_languages:
                total_languages[language] += bytes_count
            #if not we add the language and the bytes count of her to the dictionary.
            else:
                total_languages[language] = bytes_count

    return total_languages

#Function for getting user events. 
def get_user_events(username):
    url_events=f"https://api.github.com/users/{username}/events"
    events = requests.get(url_events, headers=HEADERS)
    # Make HTTP GET request to GitHub API with authentication headers
    # HEADERS contains our GitHub token for API access
    #We check if the request is successful.
    if events.status_code == 200:
        raw_events=events.json()
        #We create a list to store the filtered events.
        filtered_events=[]
        for event in raw_events:
            filtered_event = {
                "type": event["type"],
                "created_at": event["created_at"], 
                "repo_name": event["repo"]["name"]
            }
            filtered_events.append(filtered_event)
            #We return the filtered events.
        return filtered_events  

    #Error handling for the request.
    elif events.status_code == 404:
        return None
    #If the request is not successful we raise an exception.
    else:
        print("Response text:", events.text)
        raise Exception("GitHub API error:", events.status_code)
#This function is for analyzing the user's events
def analyze_user_event_types(username):
    #Here we gain access to the events of the user.
    events = get_user_events(username)
    #We create a dictionary to store the events count.
    event_counter={}
    if events is None:
        return None
    # This is the counting logic
    for event in events:
        #Here we take the type of the event.
        event_type=event["type"]
        # Check if we've seen this event type before.
        if event_type in event_counter:
            event_counter[event_type] += 1 #If yes we add 1 to the count.
        else:
            event_counter[event_type] = 1 #If not we add the event type and the count of 1.
    return event_counter    

#Function for getting the user's event created at.
def get_user_event_createdat(username):
    events = get_user_events(username) 
    #Here we create a dictionary to store the time of the events
    time_counter={
        "hours": {},
        "days": {},
        "months": {}
    }
    #We check if the events are none or empty
    if events is None or len(events) == 0:
        return None
    #Here we take the timestamp of the events
    for event in events:
        event_timestamp=event["created_at"] #This is a timestamp example of the event. 2025-07-05T01:46:53Z
        dt = datetime.fromisoformat(event_timestamp.replace('Z', '+00:00')) #We convert the string to a datetime object.
        hour = dt.hour #We access the hour of the event.
        day_name = dt.strftime('%A')  #%A = Full day name format
        month_name = dt.strftime('%B') #%B = Full month name format
        #We check if the hour, day and month is in the dictionary and if not we add it.
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

#Function for calculating the event stats and insights.
def calculate_event_stats(username):
    #Here we access the event types and the time of the events.
    event_types = analyze_user_event_types(username)    #This is a dictionary with the event types and the count of them.
    time_data = get_user_event_createdat(username)      #This is a dictionary with the time of the events.
    #We check if the event types or the time data are none or empty.
    if event_types is None or time_data is None:
        return None

    #Here we take the (A)most common event, (B)the max event count, 
    #(C)the most active hour, (D)the most active day and (E)the most active month.
    most_common_event = max(event_types, key=event_types.get)           #This is the most common event.
    max_event_count = max(event_types.values())                        #This is the max event count.
    most_active_hour = max(time_data["hours"], key=time_data["hours"].get)     #This is the most active hour.
    most_active_day = max(time_data["days"], key=time_data["days"].get)        #This is the most active day.
    most_active_month = max(time_data["months"], key=time_data["months"].get)  #This is the most active month.
    
    #Here we calculate the totals and percentages.
    total_events = sum(event_types.values()) #This is the total number of events.
    total_weekend = time_data["days"].get("Saturday", 0) + time_data["days"].get("Sunday", 0) #This is the total number of weekend events.
    total_weekday = sum(time_data["days"].get(day, 0) for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]) #This is the total number of weekday events.
    
    #Here we calculate the percentages of the event types.
    ''' 
    Ηow does it work:
    We get the number of the events of evry specific type(0 for none).Divides with total events to find the fraction
    and multiplies to find the percentage.We use an if statment to avoid division with 0.
    '''
    push_percentage = event_types.get("PushEvent", 0) / total_events * 100 if total_events > 0 else 0 #This is the percentage of push events.
    watch_percentage = event_types.get("WatchEvent", 0) / total_events * 100 if total_events > 0 else 0 #This is the percentage of watch events.
    create_percentage = event_types.get("CreateEvent", 0) / total_events * 100 if total_events > 0 else 0 #This is the percentage of create events.
    issues_percentage = event_types.get("IssuesEvent", 0) / total_events * 100 if total_events > 0 else 0#This is percentage of issues events.
    pr_percentage = event_types.get("PullRequestEvent", 0) / total_events * 100 if total_events > 0 else 0#THis is percentage of pull reqest events.
    
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

    #Developer type logic (time based)
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
    
    #Day patterns
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
    
    #Activity level categories
    if total_events >= 50:
        activity_level = "Coding Machine"
    elif total_events >= 20:
        activity_level = "Steady Developer"
    elif total_events >= 5:
        activity_level = "Casual Contributor"
    else:
        activity_level = "Occasional Coder"
    
    #Event type distribution 
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
    
    #Engagement levels
    if watch_percentage >= 40:
        engagement_type = "GitHub Explorer"
    elif push_percentage >= 80 and len(set(event_types.keys())) <= 2:
        engagement_type = "Solo Developer"
    elif pr_percentage + issues_percentage >= 40:
        engagement_type = "Team Player"
    else:
        engagement_type = "Independent Developer"
    
    #special(fun) pattern
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
    
    #It returns comprehensive stats.This is a dictionary with all analysis results
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