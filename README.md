# 💼 AI-Enhanced Web Portal with Flask

## 📌 Overview

This project is a Flask-based web application that showcases a range of full-stack development skills, including:
	•	Dynamic routing and UI rendering
	•	Database integration with SQLite (basic CRUD)
	•	Integration with Google Gemini AI and Telegram API
	•	A lightweight AI FAQ system and ethical decision simulation
	•	Custom predictive modeling demo
	•	User logging and data handling

## 🚀 Features

| Feature | Description |
|--------|-------------|
| **User Registration Logging** | Tracks user interactions with timestamps and stores them in an SQLite database. |
| **AI-Powered FAQ** | Uses Google Gemini API to dynamically generate insights on financial or business topics. |
| **Telegram Bot Integration** | Users can input their salary and receive predictions. |
| **Ethical Test Module** | Simulates a simple ethics test for decision-making scenarios. |
| **Food Expense Prediction** | Implements a basic regression model for predicting food-related expenses. |
| **Admin Tools** | Provides log viewing and deletion via an admin dashboard. |

## 🧠 Tech Stack
- Backend: Python, Flask
- Database: SQLite
- API: Google Gemini via google.generativeai and Telegram API
- Frontend: HTML (via Jinja2 templates), served by Flask
- Environment: Configured with os.getenv for API key security

## 📁 Project Structure
<pre lang="markdown">
project/
│
├── statics/
│   ├── foodexp.js
│   └── styles.css
│
├── templates/
│   ├── FAQ.html
│   ├── FAQ1.html
│   ├── FAQinput.html
│   ├── deleteLog.html
│   ├── ethical_test.html
│   ├── fail.html
│   ├── foodexp.html
│   ├── foodexp1.html
│   ├── foodexp2.html
│   ├── foodexp_pred.html
│   ├── index.html
│   ├── main.html
│   ├── pass.html
│   └── userLog.html
│
├── app.py
├── requirements.txt
├── user.db
└── README.md
</pre>


## 🛠️ How to Run Locally

Follow the steps below to run the project on your local machine:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/limeylia-ng/AN6802-AY24.git
   cd AN6082-AY24
   ```

2. **Install the Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Telegram Bot**
   - Create a new bot on Telegram via BotFather.
   - Copy the Bot API Token you get from BotFather.

4. **API Configuration**
   > This app is configured to run seamlessly on [Render](https://render.com/).
   - Ensure the `makersuite` API key is added to your **Render Environment Variables**.
   - Ensure the `telegram` API key is added to your **Render Environment Variables**.
   - Change the 'chat_id' to your own.
   
   If you're testing locally and want to use the Gemini and Telegram APIs, set the environment variable manually:

   ```bash
   export makersuite="your_gemini_api_key"    # On Windows use: set makersuite=your_gemini_api_key
   export telegram="your_telegram_api_key"    # On Windows use: set telegram=your_telegram_api_key
   ```

5. **Run the Application**

   ```bash
   python app.py
   ```

6. **Open Your Browser and Visit**

   ```
   http://127.0.0.1:8000/
   ```
