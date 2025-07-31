from github_api import get_user_data

def display_user_info(user_data):
    print(f"\nUsername: {user_data['login']}")
    print(f"Profile Url: {user_data['html_url']}")
    print(f"Name: {user_data.get('name', 'N/A')}")
    print(f"Bio: {user_data.get('bio', 'N/A')}")
    print(f"Company: {user_data.get('company', 'N/A')}")
    print(f"Location: {user_data.get('location', 'N/A')}")
    print(f"Public Repos: {user_data['public_repos']}")
    print(f"Followers: {user_data['followers']}")
    print(f"Following: {user_data['following']}")
    print(f"GitHub Profile: {user_data['html_url']}")
    print(f"Joined: {user_data['created_at'][:10]}")
    print(f"Avatar{user_data['avatar_url']}")
if __name__ == "__main__":
    username = input("Enter GitHub username: ")# Here we taking the user name 
    user_data = get_user_data(username)# Here we use the get_user_data from the github_api.py file

    if user_data:
        display_user_info(user_data)# Here we print the info
    else:
        print("❌ User not found.")
