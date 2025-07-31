1st Section --> About evry file
A)main.py
This is a single terminal app that takes a username and displays users's info using GitHub API.
=========================================================================================================================================================
line 1 --> Here we import the get_user_data function from the github_api.py file.It makes a request at GitHub API , taking the user info and returns as a dictionary form.

line 3 --> We define a helper function that takes a GitHub user's data and displays it nicely. ".get('name', 'N/A')" is used to prevent the code from crashing if the information is missing.

Notes --> Lines that have user_data.get is nullable and that that dont have is not nullable.



B)github_api.py
Here we just call the API.
=========================================================================================================================================================
line 5 --> Is the API request and the username that we will fill it on the main.py 

line 8,10 --> Is about the code that returns. If its 200 everything is OK else its 404 smth is going on.