# ==========================
#To activate (form the terminal, it doesn't work from the button) :
# 1.source venv/bin/activate  
# 2.streamlit run app.py

# ==========================


import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------------------
# Setup Session State to accumulate jobs
# ------------------------------------------
if "all_jobs_text" not in st.session_state:
    st.session_state.all_jobs_text = ""
if "job_count" not in st.session_state:
    st.session_state.job_count = 0

# ------------------------------------------
# Scraper Function
# ------------------------------------------
def scrape_linkedin_job(url):
    options = Options()
    options.add_argument("--headless") # MUST be headless for cloud deployment
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    # Initialize the driver (works locally and handles cloud nicely)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        # 1. Title
        try:
            h1_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            job_title = h1_element.text.strip()
        except:
            job_title = "Title not found"
        
        # 2. Stats
        try:
            stats_element = driver.find_element(By.CSS_SELECTOR, ".top-card-layout__entity-info, .topcard__flavor-row")
            stats = stats_element.text.strip().replace('\n', ' | ')
        except:
            stats = "Stats not found"

        # 3. Click Show More
        try:
            show_more_btn = driver.find_element(By.CSS_SELECTOR, "button[data-tracking-control-name='public_jobs_show-more-html-btn']")
            driver.execute_script("arguments[0].click();", show_more_btn)
            time.sleep(1)
        except:
            pass
            
        # 4. Description
        try:
            desc_element = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup, .description__text")
            description = desc_element.get_attribute("innerText").strip()
        except:
            description = "Description not found"
            
        # Format the job for the text file (Clean format for LLMs)
        formatted_job = (
            f"=== JOB {st.session_state.job_count + 1} ===\n"
            f"LINK: {url}\n"
            f"TITLE: {job_title}\n"
            f"STATS: {stats}\n"
            f"DESCRIPTION:\n{description}\n"
            f"{'='*50}\n\n"
        )
        return formatted_job
        
    except Exception as e:
        return f"❌ Error scraping {url}: {str(e)}\n\n"
    finally:
        driver.quit()

# ------------------------------------------
# Streamlit Web App Interface
# ------------------------------------------
st.set_page_config(page_title="LinkedIn Job Scraper", page_icon="💼", layout="centered")

st.title("💼 LinkedIn Job Scraper")
st.write("Paste links one by one. The app will save them all into a single text file that you can download and feed to an LLM.")

# Input Form
with st.form("job_form", clear_on_submit=True):
    job_link = st.text_input("🔗 Paste LinkedIn Job Link:")
    submitted = st.form_submit_button("Scrape & Add to List", type="primary")
    
if submitted:
    if "linkedin.com/jobs" not in job_link:
        st.error("Please enter a valid LinkedIn job URL.")
    else:
        with st.spinner("Scraping LinkedIn... 🕵️‍♂️"):
            job_data = scrape_linkedin_job(job_link)
            
        if "❌ Error" not in job_data:
            st.session_state.all_jobs_text += job_data
            st.session_state.job_count += 1
            st.success(f"✅ Job added! Total jobs ready: {st.session_state.job_count}")
        else:
            st.error(job_data)

st.write("---")

# Download Section
if st.session_state.job_count > 0:
    st.subheader(f"📄 Download Your Jobs ({st.session_state.job_count} scraped)")
    
    # The Download Button
    st.download_button(
        label="⬇️ Download Jobs for LLM (.txt)",
        data=st.session_state.all_jobs_text,
        file_name="scraped_linkedin_jobs.txt",
        mime="text/plain"
    )
    
    # Preview text box
    with st.expander("Preview Scraped Text"):
        st.text(st.session_state.all_jobs_text)
        
    # Clear button
    if st.button("🗑️ Clear List & Start Over"):
        st.session_state.all_jobs_text = ""
        st.session_state.job_count = 0
        st.rerun()