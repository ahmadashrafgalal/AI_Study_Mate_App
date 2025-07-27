### 🧠 AI Study Mate

![alt text](<Study Mate.png>)


**AI Study Mate** is a smart study assistant platform that helps students revise better by:
- Automatically summarizing uploaded study materials (PDFs/images/notes)
- Generating quizzes based on the summarized content
- Tracking your results and progress via a dashboard
- Organizing summaries as **summary cards**
- Sharing summaries and quizzes via a **public link**

---

## ✨ Features

- 📄 Upload handwritten or digital notes and get clean summaries using AI
- 📝 Auto-generated quizzes to test your understanding
- 📊 Dashboard with analytics and performance tracking
- 🗂 Organize your materials into **Summary Cards**
- 🔗 Shareable links to send your summary or quiz to friends
- 🛠 Choose to add new content to existing cards or start a new one

---

## ⚙️ Tech Stack

- **Backend**: Django  
- **Frontend**: TailwindCSS  
- **Automation**: n8n  
- **Database**: SQLite (for development)

---

## 📁 Project Structure

```

App/
├── static/                     # Static files (CSS, JS, etc.)
├── templates/                 # HTML templates
├── views/                     # Separated Django views
│   ├── auth_views.py
│   ├── dashboard_views.py
│   ├── exam_views.py
│   ├── results_views.py
│   ├── share_views.py
│   └── summary_views.py
├── profile_images/            # User profile images (ignored in Git)
├── summary_images/            # Uploaded study images (ignored in Git)
├── models.py
├── urls.py
└── ...

````

---

## 🧪 Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/ai-study-mate.git
cd ai-study-mate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python manage.py runserver
````

---

## 🛡 .gitignore Highlights

```
__pycache__/
*.pyc
db.sqlite3
profile_images/
summary_images/
.env
/static/
```

---

## 📧 Contact

Developed by [Ahmad Ashraf](mailto:ahmadashrafglal@gmail.com)
[LinkedIn](https://www.linkedin.com/in/ahmadashrafgalal/)

---

> Built with 💙 to help students study smarter.
