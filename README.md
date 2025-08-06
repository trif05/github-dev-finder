# GitHub DevFinder 🔍

GitHub DevFinder is a full-featured web application designed to help you explore and analyze GitHub user profiles in depth. Built with the Flask web framework,
it enables you to search for any GitHub username and instantly retrieve live data from the GitHub API.When you search for a user, DevFinder fetches their public 
profile information, repositories, and recent activity. It then processes this data to generate insightful statistics and interactive visualizations. These include:

1)Profile Overview: Displays the user’s avatar, name, bio, company, location, and key GitHub stats (public repos, followers, following).
2)Recent Activity: Shows a table of the user’s latest GitHub events (such as pushes, stars, issues, and more), including the type of event, repository, and date.
3)Activity Patterns: Analyzes when the user is most active, highlighting their peak hours and days, and visualizes weekly activity distribution with bar charts.
4)Language Usage: Aggregates and visualizes the programming languages used across the user’s repositories with an interactive pie or donut chart.
5)Developer Insights: Calculates and displays custom insights, such as developer type (e.g., Night Owl, Weekend Warrior), activity level, and contribution style, based on the user’s event history.
6)Responsive Design: The interface is optimized for both desktop and mobile devices, ensuring a smooth experience everywhere.

In summary:
GitHub DevFinder is not just a simple profile viewer—it’s an analytics dashboard that helps you understand a developer’s 
habits, strengths, and coding patterns at a glance, all powered by real-time GitHub data.

---

## 📸 Screenshots


![Home Page](https://raw.githubusercontent.com/trif05/github-dev-finder/main/images/Screenshot1.png)

![Top part](https://raw.githubusercontent.com/trif05/github-dev-finder/main/images/Screenshot2.png)

![Mid part](https://raw.githubusercontent.com/trif05/github-dev-finder/main/images/Screenshot3.png)

![Lower part](https://raw.githubusercontent.com/trif05/github-dev-finder/main/images/Screenshot4.png)

---

## 🚀 Features

- **User Search**: Enter any GitHub username and retrieve live data from the GitHub API
- **Visual Stats**: View charts with contribution graphs, most used languages, and repository insights
- **Responsive Design**: Optimized UI for both desktop and mobile screens
- **Built with Flask**: A lightweight Python backend for efficient API handling
- **GitHub API Integration**: Authenticated requests for real-time user and repo data

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Jinja2
- **API**: GitHub REST API
- **Visualization**: Plotly / Chart.js *(depending on implementation)*
- **Authentication**: Personal GitHub token for secure API requests

---

## 📂 Project Structure

```
├── app.py              # Flask server file
├── main.py             # Routing and rendering logic
├── github_api.py       # Handles GitHub API requests
├── templates/
│   └── index.html      # Jinja2 HTML Template
├── static/
│   └── css/            # Styling
├── README.md           # Project documentation
```

## 🔧 Tools Used

- **VS Code**
- **Cursor**
- **Claude (AI Assistant)** – for styling and UI feedback

---

## ⚙️ Setup Instructions

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/trif05/github-devfinder.git
cd github-devfinder
```

### 2. Create a Virtual Environment (optional)
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add GitHub Token
In the `github_api.py` file, replace `"your_personal_github_token"` with your actual GitHub token:
```python
GITHUB_TOKEN = "your_personal_github_token"
```
⚠️ **Never share your GitHub token publicly. Use `.env` if you want better security.**

### 5. Run the Flask App
```bash
python app.py
```
Then go to: **http://127.0.0.1:5000**

---

## ⚠️ Disclaimer

- Make sure to respect GitHub's API rate limits
- Keep your personal access token secure and do not expose it in public repos

---

## 👤 Contact me

Created by **Thodoris Trifonopoulos** – feel free to reach out via [GitHub](https://github.com/trif05)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
