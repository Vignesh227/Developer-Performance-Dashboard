# Developer-Performance-Dashboard
 A Streamlit-based dashboard that provides insights into developer performance using data from an open-source GitHub repository. This focuses on collecting and analyzing GitHub data, calculating performance metrics, and implements a natural language interface for querying these metrics

## Prerequisites
Before you begin, ensure you have the following installed:

- Python 3.9 or above
- GitHub Personal Access Token (PAT) (with access to the GitHub API)

## How to Get a GitHub API Key (Personal Access Token)?

1. **Log in to GitHub:**
   - Go to [github.com](https://github.com) and sign in to your account.

2. **Navigate to Settings:**
   - In the top-right corner of any GitHub page, click your profile photo, then click **Settings**.

3. **Access Developer Settings:**
   - In the left sidebar, scroll down and click **Developer settings**.

4. **Create a Personal Access Token:**
   - In the **Developer settings** page, click **Personal access tokens** on the left sidebar.
   - Click the **Generate new token** button.

5. **Configure Your Token:**
   - Give your token a descriptive **Note** (e.g., "GitHub Developer Dashboard").
   - Set the **Expiration** date based on how long you want the token to be valid.
   - Under **Select scopes**, choose the necessary permissions. For this project, at minimum, select:
     - `repo` (for repository access)
     - `read:user` (for user data)
     - `read:org` (for organizational data if applicable)
   
6. **Generate and Save the Token:**
   - Click **Generate token**.
   - **Important:** Copy your token immediately. You won’t be able to see it again. 

<hr> 

# Installation 

## 1. Download
- Download the repository as ZIP file
- Unzip the package, and store in your desired location

## 2. Create Virtual Environment
```
python -m venv .venv
```

## 3. Activate the Virtual Environment
> For Mac/Linux
```
source .venv/bin/activate
```
> For Windows
```
.\.venv\Scripts\activate
```    

## 4. Install Dependencies
```
pip install -r requirements.txt
```

## 5. Add Your GitHub API Key
- Create a .env file in the root of your project folder (if not already present).
- Add your GitHub Personal Access Token (PAT) to the .env file in the following format:
```
GITHUB_API_KEY = your_github_api_key_here
```

## 6. Update .gitignore
Ensure .env is listed in your .gitignore file to avoid accidentally uploading sensitive information:
```
.env
```

## 7. Run the Application
Open command prompt and type the following to run the app:
```
streamlit run main.py
```

## 8. Access the App
Once the application is running, you can access it in your web browser by visiting:
```
http://localhost:8501
```

<hr>

# Future Work
- Add natural language querying using NLP or LLMs to generate visualizations based on user questions.
- Improve the performance for large-scale data processing.




























