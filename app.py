# The flask part, user does POST(username) it calls the get_user_data() and sends the data to the HTML file
from flask import Flask, render_template, request
from github_api import *
import plotly.express as px
import pandas as pd

# Create the Flask application instance
app = Flask(__name__)

# Define the main route that handles both GET and POST requests
@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize all variables to None so they exist in all contexts
    # These will be passed to the HTML template regardless of whether a search was performed
    user_data = None
    searched = False
    chart_html = None
    user_events = None
    user_createdat = None  
    user_insights = None
    
    # Check if the user submitted the search form using POST method
    if request.method == "POST":
        # Extract the username from the form data submitted by the user
        # This corresponds to the input field with name="username" in the HTML form
        username = request.form["username"]
        
        # Call the GitHub API function to fetch user data based on the provided username
        # This function is imported from github_api.py and returns user profile information
        user_data = get_user_data(username)
        
        # Set the searched flag to True so the template knows a search was performed
        # This controls the conditional rendering in the HTML template
        searched = True
        
        # Check if the API call was successful and user data was retrieved
        if user_data is None:
            # Print error message to console if user doesn't exist or API call failed
            print("User not found")
        else:
            # User was found successfully, now fetch additional data for comprehensive analysis
            # Get programming language statistics across all user repositories
            total_languages = get_user_languages_summary(username)
            
            # Fetch recent activity events from the user's GitHub timeline
            user_events = get_user_events(username)
            
            # Get timestamp data for activity pattern analysis
            user_createdat = get_user_event_createdat(username)
            
            # Calculate comprehensive statistics and insights about user behavior
            user_insights = calculate_event_stats(username)
            
            # Chart creation section for language usage visualization
            # Only proceed if language data was successfully retrieved
            if total_languages is not None:
                # Convert dictionary to list of tuples for easier sorting
                # Each tuple contains (language_name, bytes_count)
                language_data = list(zip(total_languages.keys(), total_languages.values()))
                
                # Sort languages by usage in descending order to show most used first
                sorted_data = sorted(language_data, key=lambda x: x[1], reverse=True)
                
                # Take only the top 5 most used languages for cleaner visualization
                top_5_data = sorted_data[:5]
                
                # Group all remaining languages into "Other" category to avoid cluttered chart
                other_data = sorted_data[5:]
                
                # Calculate total bytes for all languages not in top 5
                other_bytes = sum(item[1] for item in other_data)
                
                # Extract language names and byte counts for chart creation
                languages = [item[0] for item in top_5_data]
                bytes = [item[1] for item in top_5_data]
                
                # Add "Other" category if there are more than 5 languages total
                if len(sorted_data) > 5:
                    languages.append("Other")
                    bytes.append(other_bytes)
                    # Create pie chart with standard appearance for 6+ languages
                    fig = px.pie(names=languages, values=bytes, title="")
                    # Disable hover information for cleaner appearance
                    fig.update_traces(hoverinfo='none', hovertemplate=None)
                    # Convert chart to HTML string for embedding in template
                    chart_html = fig.to_html()    
                else:
                    # Create donut chart in center for 5 or fewer languages
                    fig = px.pie(names=languages, values=bytes)
                    # Add hole in center and disable hover for donut effect
                    fig.update_traces(hoverinfo='none', hovertemplate=None, hole=0.6)
                    # Convert to HTML for template rendering
                    chart_html = fig.to_html()
    
    # Render the HTML template with all collected data
    # All variables are passed to template regardless of search status for consistent rendering
    return render_template("index.html", 
                         user_data=user_data, 
                         searched=searched, 
                         chart_html=chart_html,
                         user_events=user_events,
                         user_createdat=user_createdat,
                         user_insights=user_insights) 

# Run the Flask application only if this file is executed directly
if __name__ == "__main__":
    # Start the Flask development server
    app.run()

# Thodoris Trifonopoulos dev finder