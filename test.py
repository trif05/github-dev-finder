from github_api import get_user_events
items=[1,2,3]

for item in items:
    print (item)
for i in range(10):
    print ("test")
    if i == "test":
        for i in range(10):
            print ("passed")
# events = get_user_events("trif05")
# print(events[:2]) 
#what it returns is that below
#[{'type': 'WatchEvent', 'created_at': '2025-07-05T01:46:53Z', 'repo_name': 'chgogos/big_data'}]