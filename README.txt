# GitHub DevFinder 🔍

GitHub DevFinder is a web application built with **Flask** that allows you to search for GitHub users and visualize detailed statistics about their profiles using interactive charts and data summaries.

---

## 📸 Screenshots

## 📸 Screenshots

![Home Page](https://raw.githubusercontent.com/trif05/github-dev-finder/84122719a6cde127160768f74fb772a419ee362a/images/Screenshot1.png)
![Top part](https://raw.githubusercontent.com/trif05/github-dev-finder/66df70fabcdfc025089047e6e8b583aa658fe6d9/images/Screenshot2.png)
![Mid part](https://raw.githubusercontent.com/trif05/github-dev-finder/66df70fabcdfc025089047e6e8b583aa658fe6d9/images/Screenshot3.png)
![Lower part](https://raw.githubusercontent.com/trif05/github-dev-finder/66df70fabcdfc025089047e6e8b583aa658fe6d9/images/Screenshot4.png)

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
