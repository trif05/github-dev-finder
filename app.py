#The flask part, if the user do POST(username) it calls the get_user_data() and send the data on the HTML file
from flask import Flask, render_template, request
from github_api import *
import plotly.express as px
import pandas as pd


app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    user_data = None
    searched = False
    chart_html = None
    
    if request.method == "POST":
        username = request.form["username"]
        user_data = get_user_data(username)
        searched = True
        
        if user_data is None:
            print("User not found")
        else:
            # ← ΝΕΟ: Αν ο χρήστης βρέθηκε, φτιάξε και το chart
            total_languages = get_user_languages_summary(username)
            if total_languages is not None:
                language_data = list(zip(total_languages.keys(), total_languages.values()))
                sorted_data = sorted(language_data, key=lambda x: x[1], reverse=True)
                top_5_data = sorted_data[:5]
                other_data = sorted_data[5:]
                other_bytes = sum(item[1] for item in other_data)
                languages = [item[0] for item in top_5_data]
                bytes = [item[1] for item in top_5_data]
                if len(sorted_data) > 5:
                    languages.append("Other")
                    bytes.append(other_bytes)
                    fig = px.pie(names=languages, values=bytes, title="")
                    fig.update_traces(hoverinfo='none', hovertemplate=None)
                    chart_html = fig.to_html()    
                    return render_template("index.html", user_data=user_data, searched=searched, chart_html=chart_html) 
                fig = px.pie(names=languages, values=bytes)
                fig.update_traces(hoverinfo='none', hovertemplate=None, hole=0.6)
                chart_html = fig.to_html()    
    return render_template("index.html", user_data=user_data, searched=searched, chart_html=chart_html) 

if __name__ == "__main__":
    app.run(debug=True)
