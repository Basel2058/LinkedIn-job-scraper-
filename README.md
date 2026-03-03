# 💼 LinkedIn Job Scraper for LLMs

A streamlined **Streamlit** web application designed to scrape job descriptions from LinkedIn and compile them into a clean, structured `.txt` file. 

This tool is specifically built to help users gather job data to feed into **Large Language Models (LLMs)** like ChatGPT, Claude, or Gemini for resume tailoring, cover letter generation, and career analysis.

---

## ✨ Key Features

* **Session Persistence:** Add multiple jobs one by one; the app accumulates them into a single session.
* **LLM-Optimized Output:** Formats data (Title, Stats, Description) into a clean structure that AI models parse easily.
* **Headless Scraping:** Uses Selenium in headless mode for a background process that doesn't interrupt your workflow.
* **Auto-Driver Management:** Uses `webdriver-manager` to automatically handle Chrome driver updates.
* **Clear UI:** Simple interactive interface built with Streamlit.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
